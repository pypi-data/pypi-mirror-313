"""
Functions for interacting with Amazon Web Services.

This module supports management of AWS accounts, S3 buckets, and objects in S3 buckets. It uses Amazon's boto3 library
behind the scenes.

In order for HEA to access AWS accounts, buckets, and objects, there must be a volume accessible to the user through
the volumes microservice with an AWSFileSystem for its file system. Additionally, credentials must either be stored
in the keychain microservice and associated with the volume through the volume's credential_id attribute,
or stored on the server's file system in a location searched by the AWS boto3 library. Users can only see the
accounts, buckets, and objects to which the provided AWS credentials allow access, and HEA may additionally restrict
the returned objects as documented in the functions below. The purpose of volumes in this case is to supply credentials
to AWS service calls. Support for boto3's built-in file system search for credentials is only provided for testing and
should not be used in a production setting. This module is designed to pass the current user's credentials to AWS3, not
to have application-wide credentials that everyone uses.

The request argument to these functions is expected to have a OIDC_CLAIM_sub header containing the user id for
permissions checking. No results will be returned if this header is not provided or is empty.

In general, there are two flavors of functions for getting accounts, buckets, and objects. The first expects the id
of a volume as described above. The second expects the id of an account, bucket, or bucket and object. The latter
attempts to match the request up to any volumes with an AWSFileSystem that the user has access to for the purpose of
determine what AWS credentials to use. They perform the
same except when the user has access to multiple such volumes, in which case supplying the volume id avoids a search
through the user's volumes.
"""
import asyncio
import orjson
import logging
from concurrent.futures import ThreadPoolExecutor
from enum import Enum, auto
from aiohttp import web, hdrs
from heaobject.aws import S3StorageClass

from heaobject.awss3key import KeyDecodeException, decode_key, is_folder, split, replace_parent_folder, parent, display_name, is_object_in_folder

from ..util import queued_processing
from .. import response
from ..heaobjectsupport import RESTPermissionGroup, new_heaobject_from_type
from ..oidcclaimhdrs import SUB
from ..appproperty import HEA_DB, HEA_BACKGROUND_TASKS
from ..uritemplate import tvars
from typing import Any, Optional, Callable, AsyncIterator, NamedTuple
from collections.abc import Awaitable, Mapping
from aiohttp.web import Request, Response, Application, HTTPError
from heaobject.volume import AWSFileSystem
from heaobject.user import NONE_USER, ALL_USERS
from heaobject.root import ShareImpl
from heaobject.folder import Folder, AWSS3Folder
from heaobject.project import AWSS3Project
from heaserver.service.activity import DesktopObjectActionLifecycle
from heaserver.service import aiohttp
from heaobject.activity import DesktopObjectAction
from heaobject.aws import S3Object
from heaobject.error import DeserializeException
from heaobject.activity import Status
from asyncio import gather, AbstractEventLoop
from functools import partial
from urllib.parse import unquote
from botocore.exceptions import ClientError as BotoClientError, ParamValidationError

from ..sources import HEA
from mypy_boto3_s3.client import S3Client
from .aws import S3ClientContext, client_error_status, CLIENT_ERROR_404
from aiohttp.web import HTTPException
from yarl import URL

"""
Available functions
AWS object
- get_account
- post_account                    NOT TESTED
- put_account                     NOT TESTED
- delete_account                  CANT https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_accounts_close.html
                                  One solution would be to use beautiful soup : https://realpython.com/beautiful-soup-web-scraper-python/

- users/policies/roles : https://www.learnaws.org/2021/05/12/aws-iam-boto3-guide/

- change_storage_class            TODO
- copy_object
- delete_bucket_objects
- delete_bucket
- delete_folder
- delete_object
- download_object
- download_archive_object         TODO
- generate_presigned_url
- get_object_meta
- get_object_content
- get_all_buckets
- get all
- opener                          TODO -> return file format -> returning metadata containing list of links following collection + json format
-                                         need to pass back collection - json format with link with content type, so one or more links, most likely
- post_bucket
- post_folder
- post_object
- post_object_archive             TODO
- put_bucket
- put_folder
- put_object
- put_object_archive              TODO
- transfer_object_within_account
- transfer_object_between_account TODO
- rename_object
- update_bucket_policy            TODO

TO DO
- accounts?
"""
MONGODB_BUCKET_COLLECTION = 'buckets'

ROOT_FOLDER = Folder()
ROOT_FOLDER.id = 'root'
ROOT_FOLDER.name = 'root'
ROOT_FOLDER.display_name = 'Root'
ROOT_FOLDER.description = "The root folder for an AWS S3 bucket's objects."
_root_share = ShareImpl()
_root_share.user = ALL_USERS
_root_share.permissions = RESTPermissionGroup.POSTER_PERMS._perms_internal
ROOT_FOLDER.shares = [_root_share]
ROOT_FOLDER.source = HEA


async def create_object(request: web.Request, type_: type[S3Object] | None = None, activity_cb: Optional[
                            Callable[[Application, DesktopObjectAction], Awaitable[None]]] = None) -> web.Response:
    """
    Creates a new file or folder in a bucket. The volume id must be in the volume_id entry of the request.match_info
    dictionary. The bucket id must be in the bucket_id entry of request.match_info. The folder or file id must be in
    the id entry of request.match_info. The body must contain a heaobject.folder.AWSS3Folder or
    heaobject.data.AWSS3FileObject dict.

    :param request: the HTTP request (required).
    :param type_: the expected type of S3Object, or None if it should just parse the type that it finds.
    :param activity_cb: optional coroutine that is called when potentially relevant activity occurred.
    :return: the HTTP response, with a 201 status code if successful with the URL to the new item in the Location
    header, 403 if access was denied, 404 if the volume or bucket could not be found, or 500 if an internal error
    occurred.
    """
    if not issubclass(type_ or S3Object, S3Object):
        raise TypeError(f'Invalid type_ parameter {type_}, must be S3Object or a subclass of it.')
    try:
        try:
            folder_or_file: S3Object = await new_heaobject_from_type(request, type_ or S3Object)
        except TypeError:
            return response.status_bad_request(f'Expected type {type_ or S3Object}; actual object was {await request.text()}')
    except (DeserializeException, TypeError) as e:
        return response.status_bad_request(f'Invalid new object: {e}')

    try:
        volume_id = request.match_info['volume_id']
        bucket_id = request.match_info['bucket_id']
    except KeyError as e:
        return response.status_bad_request(f'{e} is required')
    folder_or_file_key = folder_or_file.key
    if folder_or_file_key is None:
        return response.status_bad_request(f'The object {folder_or_file.display_name} must have a key')

    async with DesktopObjectActionLifecycle(request=request,
                                            code='hea-create',
                                            description=f'Creating {_activity_object_display_name(bucket_id, folder_or_file_key)}',
                                            activity_cb=activity_cb) as activity:
        async with S3ClientContext(request=request, volume_id=volume_id) as s3_client:
            response_ = await _create_object(s3_client, bucket_id, folder_or_file_key)

            def type_part():
                if isinstance(folder_or_file, AWSS3Folder):
                    return 'awss3folders'
                elif isinstance(folder_or_file, AWSS3Project):
                    return 'awss3projects'
                else:
                    return 'awss3files'

            if response_.status == 201:
                return await response.post(request, folder_or_file.id, f'volumes/{volume_id}/buckets/{bucket_id}/{type_part()}')
            elif 400 <= response_.status < 500:
                activity.status = Status.FAILED
                return await response.post(request, folder_or_file.id, f'volumes/{volume_id}/buckets/{bucket_id}/{type_part()}')
            else:
                activity.status = Status.FAILED
                raise ValueError


async def copy_object(request: Request,
                      activity_cb: Callable[[Application, DesktopObjectAction], Awaitable[None]] | None = None,
                      copy_object_completed_cb: Callable[[str, str, str, str], Awaitable[None]] | None = None) -> Response:
    """
    copy/paste (duplicate), throws error if destination exists, this so an overwrite isn't done
    throws another error is source doesn't exist
    https://medium.com/plusteam/move-and-rename-objects-within-an-s3-bucket-using-boto-3-58b164790b78
    https://stackoverflow.com/questions/47468148/how-to-copy-s3-object-from-one-bucket-to-another-using-python-boto3

    :param request: the aiohttp Request, with the body containing the target bucket and key, and the match_info
    containing the source volume, bucket, and key (required). The key may be a file or a folder, and in the latter
    case the entire folder's contents are copied.
    :param activity_cb: optional coroutine that is called when potentially relevant activity occurred.
    :param copy_object_completed_cb: called after successfully completing the copy of each object (optional). The
    callable must be reentrant. Its four parameters are source bucket name, source key, target bucket name, and target
    key.
    :return: the HTTP response. If successful, the response will have status code 201, and a Location header will be
    set with the URL for the copy target.
    :raises HTTPBadRequest: if preflight fails.
    """
    logger = logging.getLogger(__name__)
    volume_id = request.match_info['volume_id']
    try:
        source_bucket_name, source_key_name = await _extract_source(request.match_info)
        target_url, target_bucket_name, target_folder_name, _ = await _copy_object_extract_target(await request.json())
    except (web.HTTPBadRequest, orjson.JSONDecodeError, ValueError) as e:
        logger.exception(e)
        return response.status_bad_request(str(e))

    async with DesktopObjectActionLifecycle(request=request,
                                            code='hea-duplicate',
                                            description=f'Copying {_activity_object_display_name(source_bucket_name, source_key_name)} to {_activity_object_display_name(target_bucket_name, target_folder_name)}',
                                            activity_cb=activity_cb) as activity:
        async with S3ClientContext(request=request, volume_id=volume_id) as s3_client:
            logger.debug('Copy requested from %s/%s to %s/%s', source_bucket_name, source_key_name, target_bucket_name,
                         target_folder_name)

            resp = await _copy_object(s3_client, source_bucket_name, source_key_name, target_bucket_name,
                                      target_folder_name, copy_completed_cb=copy_object_completed_cb)
            if resp.status == 201:
                resp.headers[hdrs.LOCATION] = target_url
            else:
                activity.status = Status.FAILED
            return resp

async def copy_object_async(request: Request, status_location: URL | str,
                            activity_cb: Callable[[Application, DesktopObjectAction], Awaitable[None]] | None = None,
                            done_cb: Callable[[Response], Awaitable[None]] | None = None,
                            copy_object_completed_cb: Callable[[str, str, str, str], Awaitable[None]] | None = None) -> Response:
    """
    copy/paste (duplicate), throws error if destination exists, this so an overwrite isn't done
    throws another error is source doesn't exist
    https://medium.com/plusteam/move-and-rename-objects-within-an-s3-bucket-using-boto-3-58b164790b78
    https://stackoverflow.com/questions/47468148/how-to-copy-s3-object-from-one-bucket-to-another-using-python-boto3

    :param request: the aiohttp Request, with the body containing the target bucket and key, and the match_info
    containing the source volume, bucket, and key. (required).
    :param activity_cb: optional coroutine that is called when potentially relevant activity occurred.
    :param done_cb: called after successfully completing the entire copy operation (optional).
    :param copy_object_completed_cb: called after successfully completing the copy of each object (optional). The
    callable must be reentrant. Its four parameters are source bucket name, source key, target bucket name, and target
    key.
    :return: the HTTP response.
    """
    sub = request.headers.get(SUB, NONE_USER)
    logger = logging.getLogger(__name__)
    volume_id = request.match_info['volume_id']
    try:
        source_bucket_name, source_key_name = await _extract_source(request.match_info)
        target_url, target_bucket_name, target_folder_name, _ = await _copy_object_extract_target(await request.json())
    except (web.HTTPBadRequest, orjson.JSONDecodeError, ValueError) as e:
        logger.exception(e)
        return response.status_bad_request(str(e))

    if status_location is None:
        raise ValueError('status_location cannot be None')

    async def coro(app: Application):
        async with DesktopObjectActionLifecycle(request=request,
                                                code='hea-duplicate',
                                                user_id=sub,
                                                description=f'Copying {_activity_object_display_name(source_bucket_name, source_key_name)} to {_activity_object_display_name(target_bucket_name, target_folder_name)}',
                                                activity_cb=activity_cb) as activity:
            async with S3ClientContext(request=request, volume_id=volume_id) as s3_client:
                logger.debug('Copy requested from %s/%s to %s/%s', source_bucket_name, source_key_name, target_bucket_name,
                             target_folder_name)

                resp = await _copy_object(s3_client, source_bucket_name, source_key_name, target_bucket_name,
                                          target_folder_name, copy_completed_cb=copy_object_completed_cb)
                if resp.status == 201:
                    resp.headers[hdrs.LOCATION] = target_url
                else:
                    activity.status = Status.FAILED
                try:
                    if done_cb:
                        await done_cb(resp)
                except:
                    logger.exception('done_cb raised exception')
                return resp
    task_name = f'{sub}^{status_location}'
    await request.app[HEA_BACKGROUND_TASKS].add(coro, name=task_name)
    return response.status_see_other(status_location)


async def archive_object(request: Request,
                         activity_cb: Optional[Callable[[Application, DesktopObjectAction], Awaitable[None]]] = None) -> web.Response:
    """
    Archives object by performing a copy and changing storage class. This function is synchronous.
    :param request:
    :param activity_cb: optional coroutine that is called when potentially relevant activity occurred.
    :return: The HTTP response. If successful, the response will have a 201 status code, and a Location header will be
    set with the URL of the archived object.
    """
    logger = logging.getLogger(__name__)
    volume_id = request.match_info['volume_id']
    try:
        source_bucket_name, source_key = await _extract_source(request.match_info)
        request_json = await request.json()
        storage_class = S3StorageClass[next(item['value'] for item in request_json['template']['data'] if item['name'] == 'storage_class')]
    except (web.HTTPBadRequest, orjson.JSONDecodeError, KeyError, ValueError) as e:
        logger.exception(e)
        return response.status_bad_request(str(e))

    async with DesktopObjectActionLifecycle(request,
                                            code='hea-archive',
                                            description=f'Archiving {_activity_object_display_name(source_bucket_name, source_key)} to {storage_class.name}',
                                            activity_cb=activity_cb) as activity:
        async with S3ClientContext(request=request, volume_id=volume_id) as s3_client:
            resp = await _archive_object(s3_client, source_bucket_name, source_key, storage_class.name)
            if resp.status != 201:
                activity.status = Status.FAILED
            else:
                resp.headers[hdrs.LOCATION] = str(request.url)
            return resp


_archive_lock = asyncio.Lock()
async def archive_object_async(request: Request, status_location: URL | str,
                               activity_cb: Optional[Callable[[Application, DesktopObjectAction], Awaitable[None]]] = None) -> web.Response:
    """
    Archives object by performing a copy and changing storage class. This function is synchronous.
    :param request:
    :param activity_cb: optional coroutine that is called when potentially relevant activity occurred.
    :return: The HTTP response. If successful, the response will have a 201 status code, and a Location header will be
    set with the URL of the archived object.
    """
    logger = logging.getLogger(__name__)
    sub = request.headers.get(SUB, NONE_USER)
    volume_id = request.match_info['volume_id']
    try:
        source_bucket_name, source_key = await _extract_source(request.match_info)
        request_json = await request.json()
        storage_class = next(
            item['value'] for item in request_json['template']['data'] if item['name'] == 'storage_class')

        if storage_class is None:
            raise ValueError('Null value recieved - storage_class must be a string')
        if not isinstance(storage_class, str):
            raise ValueError('storage_class must be a string')

    except (web.HTTPBadRequest, orjson.JSONDecodeError, KeyError, ValueError) as e:
        logger.exception(e)
        return response.status_bad_request(str(e))

    if status_location is None:
        raise ValueError('status_location cannot be None')

    task_name = f'{sub}^{status_location}'

    async def coro(app: Application):
        async with DesktopObjectActionLifecycle(request,
                                                code='hea-archive',
                                                description=f'Archiving {_activity_object_display_name(source_bucket_name, source_key)} to {storage_class}',
                                                activity_cb=activity_cb) as activity:
            async with S3ClientContext(request=request, volume_id=volume_id) as s3_client:
                resp = await _archive_object(s3_client, source_bucket_name, source_key, storage_class)
                if resp.status != 201:
                    activity.status = Status.FAILED
                else:
                    resp.headers[hdrs.LOCATION] = str(request.url)
                return resp
    async with _archive_lock:
        if request.app[HEA_BACKGROUND_TASKS].in_progress(task_name):
            return response.status_conflict(f'Archiving {_activity_object_display_name(source_bucket_name, source_key)} is already in progress')
        await request.app[HEA_BACKGROUND_TASKS].add(coro, name=task_name)
    return response.status_see_other(status_location)


async def unarchive_object(request: Request,
                           activity_cb: Optional[Callable[[Application, DesktopObjectAction], Awaitable[None]]] = None) -> web.Response:
    """
    This method will initiate the restoring of object to s3 and copy it back into s3. This function is asynchronous

    :param request: The aiohttp web request
    :param activity_cb: optional coroutine that is called when potentially relevant activity occurred.
    :return: the HTTP response.
    """
    logger = logging.getLogger(__name__)
    volume_id = request.match_info['volume_id']
    bucket_name = request.match_info['bucket_id']
    source_key_name = decode_key(request.match_info['id']) if 'id' in request.match_info else None
    unarchive_info = await _extract_unarchive_params(await request.json())

    async with DesktopObjectActionLifecycle(request=request,
                                            code='hea-unarchive',
                                            description=f'Unarchiving {_activity_object_display_name(bucket_name, source_key_name)}',
                                            activity_cb=activity_cb) as activity:
        async with S3ClientContext(request=request, volume_id=volume_id) as s3_client:
            try:
                loop = asyncio.get_running_loop()

                async def gen():
                    async for obj_sum in list_objects(s3_client, bucket_id=bucket_name, prefix=source_key_name):
                        if obj_sum['Key'].endswith('/'):
                            continue
                        if obj_sum['StorageClass'] in (S3StorageClass.GLACIER.name, S3StorageClass.DEEP_ARCHIVE.name) and obj_sum.get('RestoreStatus') is None:
                            yield obj_sum

                async def item_processor(obj_sum):
                    logger.debug('Initiating restore of obj: %s', obj_sum['Key'])
                    r_params = {'Days': unarchive_info.days if unarchive_info.days else 7,
                                'GlacierJobParameters': {
                                    'Tier': unarchive_info.restore_tier.name if unarchive_info.restore_tier else 'Standard'}}
                    p = partial(s3_client.restore_object, Bucket=bucket_name, Key=obj_sum['Key'], RestoreRequest=r_params)
                    await loop.run_in_executor(None, p)
                await queued_processing(gen, item_processor)
            except BotoClientError as e:
                activity.status = Status.FAILED
                return response.status_bad_request(str(e))

    return web.HTTPAccepted()


async def delete_object(request: Request, recursive=False,
                        activity_cb: Callable[[Application, DesktopObjectAction], Awaitable[None]] | None = None,
                        delete_completed_cb: Callable[[str, str], Awaitable[None]] | None = None) -> Response:
    """
    Deletes a single object. The volume id must be in the volume_id entry of the request's match_info dictionary. The
    bucket id must be in the bucket_id entry of the request's match_info dictionary. The item id must be in the id
    entry of the request's match_info dictionary. An optional folder id may be passed in the folder_id entry of the
    request's match_info_dictinary.

    :param request: the aiohttp Request (required).
    :param object_type: only delete the requested object only if it is a file or only if it is a folder. Pass in
    ObjectType.ANY or None (the default) to signify that it does not matter.
    :param recursive: if True, and the object is a folder, this function will delete the folder and all of its
    contents, otherwise it will return a 400 error if the folder is not empty. If the object to delete is not a folder,
    this flag will have no effect.
    :param activity_cb: optional awaitable that is called when potentially relevant activity occurred.
    :param delete_completed_cb: optional awaitable that is called upon successful deletion of an object. The two
    parameters are the bucket name and the object key.
    :return: the HTTP response with a 204 status code if the item was successfully deleted, 403 if access was denied,
    404 if the item was not found, or 500 if an internal error occurred.
    """
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.delete_object
    # TODO: bucket.object_versions.filter(Prefix="myprefix/").delete()     add versioning option like in the delete bucket?
    if 'volume_id' not in request.match_info:
        return response.status_bad_request('volume_id is required')
    if 'bucket_id' not in request.match_info:
        return response.status_bad_request('bucket_id is required')
    if 'id' not in request.match_info:
        return response.status_bad_request('id is required')

    bucket_name = request.match_info['bucket_id']
    encoded_key = request.match_info['id']
    volume_id = request.match_info['volume_id']
    encoded_folder_key = request.match_info.get('folder_id', None)
    try:
        key = decode_key(encoded_key)
    except KeyDecodeException:
        return response.status_not_found()

    async with S3ClientContext(request=request, volume_id=volume_id) as s3_client:
        folder_key = decode_folder(encoded_folder_key) if encoded_folder_key is not None else None
        if folder_key is None and encoded_folder_key is not None:
            return response.status_bad_request(f'Invalid folder_id {encoded_folder_key}')
        if encoded_folder_key is not None and not is_object_in_folder(key, folder_key):
            loop = asyncio.get_running_loop()
            return await return_bucket_status_or_not_found(bucket_name, loop, s3_client)
        async with DesktopObjectActionLifecycle(request=request,
                                                code='hea-delete',
                                                description=f'Deleting {_activity_object_display_name(bucket_name, key)}',
                                                activity_cb=activity_cb) as activity:
            resp = await _delete_object(s3_client, bucket_name, key, recursive, delete_completed_cb=delete_completed_cb)
            if resp.status != 204:
                activity.status = Status.FAILED
            return resp

_delete_lock = asyncio.Lock()
async def delete_object_async(request: Request, status_location: URL | str, recursive=False,
                              activity_cb: Optional[
                                  Callable[[Application, DesktopObjectAction], Awaitable[None]]] = None,
                              done_cb: Callable[[Response], Awaitable[None]] | None = None,
                              delete_completed_cb: Callable[[str, str], Awaitable[None]] | None = None) -> Response:
    """
    Deletes a single object. The volume id must be in the volume_id entry of the request's match_info dictionary. The
    bucket id must be in the bucket_id entry of the request's match_info dictionary. The item id must be in the id
    entry of the request's match_info dictionary. An optional folder id may be passed in the folder_id entry of the
    request's match_info_dictinary.

    :param request: the aiohttp Request (required).
    :param object_type: only delete the requested object only if it is a file or only if it is a folder. Pass in
    ObjectType.ANY or None (the default) to signify that it does not matter.
    :param recursive: if True, and the object is a folder, this function will delete the folder and all of its
    contents, otherwise it will return a 400 error if the folder is not empty. If the object to delete is not a folder,
    this flag will have no effect.
    :param activity_cb: optional awaitable that is called when potentially relevant activity occurred.
    :param done_cb: optional awaitable that is called after successful completion of this operation.
    :param delete_completed_cb: optional awaitable that is called upon successful deletion of an object. The two
    parameters are the bucket name and the object key.
    :return: the HTTP response with a 204 status code if the item was successfully deleted, 403 if access was denied,
    404 if the item was not found, or 500 if an internal error occurred.
    """
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.delete_object
    # TODO: bucket.object_versions.filter(Prefix="myprefix/").delete()     add versioning option like in the delete bucket?
    logger = logging.getLogger(__name__)
    sub = request.headers.get(SUB, NONE_USER)
    if 'volume_id' not in request.match_info:
        return response.status_bad_request('volume_id is required')
    if 'bucket_id' not in request.match_info:
        return response.status_bad_request('bucket_id is required')
    if 'id' not in request.match_info:
        return response.status_bad_request('id is required')

    bucket_name = request.match_info['bucket_id']
    encoded_key = request.match_info['id']
    volume_id = request.match_info['volume_id']
    encoded_folder_key = request.match_info.get('folder_id', None)
    try:
        key = decode_key(encoded_key)
    except KeyDecodeException:
        return response.status_not_found()


    async with S3ClientContext(request=request, volume_id=volume_id) as s3_client:
        folder_key = decode_folder(encoded_folder_key) if encoded_folder_key is not None else None
        if folder_key is not None and not is_object_in_folder(key, folder_key):
            loop = asyncio.get_running_loop()
            return await return_bucket_status_or_not_found(bucket_name, loop, s3_client)

    async def coro(app: Application):
        async with DesktopObjectActionLifecycle(request=request,
                                                code='hea-delete',
                                                description=f'Deleting {_activity_object_display_name(bucket_name, key)}',
                                                activity_cb=activity_cb) as activity:
            async with S3ClientContext(request=request, volume_id=volume_id) as s3_client:
                resp = await _delete_object(s3_client, bucket_name, key, recursive,
                                            delete_completed_cb=delete_completed_cb)
                if resp.status != 204:
                    activity.status = Status.FAILED
                try:
                    if done_cb:
                        await done_cb(resp)
                except:
                    logger.exception('done_cb raised exception')
                return resp
    task_name = f'{sub}^{status_location}'
    async with _delete_lock:
        if request.app[HEA_BACKGROUND_TASKS].in_progress(task_name):
            return response.status_conflict(f'Deleting {_activity_object_display_name(bucket_name, key)} is already in progress')
        await request.app[HEA_BACKGROUND_TASKS].add(coro, name=task_name)
    return response.status_see_other(status_location)


async def get_volume_id_for_account_id(request: web.Request) -> str | None:
    """
    Gets the id of the volume associated with an AWS account. The account id is expected to be in the request object's
    match_info mapping, with key 'id'. The account is fetched from AWS during this operation.

    :param request: an aiohttp Request object (required).
    :return: a volume id string, or None if no volume was found associated with the AWS account or the account does not
    exist.
    """
    async def get_one(request, volume_id):
        return volume_id, await request.app[HEA_DB].get_account(request, volume_id)
    return next((volume_id for (volume_id, a) in await gather(
        *[get_one(request, v.id) async for v in request.app[HEA_DB].get_volumes(request, AWSFileSystem)])
                 if
                 a.id == request.match_info['id']), None)


# def transfer_object_between_account():
#     """
#     https://markgituma.medium.com/copy-s3-bucket-objects-across-separate-aws-accounts-programmatically-323862d857ed
#     """
#     # TODO: use update_bucket_policy to set up "source" bucket policy correctly
#     """
#     {
#     "Version": "2012-10-17",
#     "Id": "Policy1546558291129",
#     "Statement": [
#         {
#             "Sid": "Stmt1546558287955",
#             "Effect": "Allow",
#             "Principal": {
#                 "AWS": "arn:aws:iam::<AWS_IAM_USER>"
#             },
#             "Action": [
#               "s3:ListBucket",
#               "s3:GetObject"
#             ],
#             "Resource": "arn:aws:s3:::<SOURCE_BUCKET>/",
#             "Resource": "arn:aws:s3:::<SOURCE_BUCKET>/*"
#         }
#     ]
#     }
#     """
#     # TODO: use update_bucket_policy to set up aws "destination" bucket policy
#     """
#     {
#     "Version": "2012-10-17",
#     "Id": "Policy22222222222",
#     "Statement": [
#         {
#             "Sid": "Stmt22222222222",
#             "Effect": "Allow",
#             "Principal": {
#                 "AWS": [
#                   "arn:aws:iam::<AWS_IAM_DESTINATION_USER>",
#                   "arn:aws:iam::<AWS_IAM_LAMBDA_ROLE>:role/
#                 ]
#             },
#             "Action": [
#                 "s3:ListBucket",
#                 "s3:PutObject",
#                 "s3:PutObjectAcl"
#             ],
#             "Resource": "arn:aws:s3:::<DESTINATION_BUCKET>/",
#             "Resource": "arn:aws:s3:::<DESTINATION_BUCKET>/*"
#         }
#     ]
#     }
#     """
#     # TODO: code
#     source_client = boto3.client('s3', "SOURCE_AWS_ACCESS_KEY_ID", "SOURCE_AWS_SECRET_ACCESS_KEY")
#     source_response = source_client.get_object(Bucket="SOURCE_BUCKET", Key="OBJECT_KEY")
#     destination_client = boto3.client('s3', "DESTINATION_AWS_ACCESS_KEY_ID", "DESTINATION_AWS_SECRET_ACCESS_KEY")
#     destination_client.upload_fileobj(source_response['Body'], "DESTINATION_BUCKET",
#                                       "FOLDER_LOCATION_IN_DESTINATION_BUCKET")


# async def rename_object(request: Request, volume_id: str, object_path: str, new_name: str):
#     """
#     BOTO3, the copy and rename is the same
#     https://medium.com/plusteam/move-and-rename-objects-within-an-s3-bucket-using-boto-3-58b164790b78
#     https://stackoverflow.com/questions/47468148/how-to-copy-s3-object-from-one-bucket-to-another-using-python-boto3
#
#     :param request: the aiohttp Request (required).
#     :param volume_id: the id string of the volume representing the user's AWS account.
#     :param object_path: (str) path to object, includes both bucket and key values
#     :param new_name: (str) value to rename the object as, will only replace the name not the path. Use transfer object for that
#     """
#     # TODO: check if ACL stays the same and check existence
#     try:
#         s3_resource = await request.app[HEA_DB].get_resource(request, 's3', volume_id)
#         copy_source = {'Bucket': object_path.partition("/")[0], 'Key': object_path.partition("/")[2]}
#         bucket_name = object_path.partition("/")[0]
#         old_name = object_path.rpartition("/")[2]
#         s3_resource.meta.client.copy(copy_source, bucket_name,
#                                      object_path.partition("/")[2].replace(old_name, new_name))
#     except ClientError as e:
#         logging.error(e)


def handle_client_error(e: BotoClientError) -> HTTPError:
    """
    Translates a boto3 client error into an appropriate HTTP response.

    :param e: a boto3 client error (required).
    :return: an HTTP response with status code >=400 that can be raised as an exception.
    """
    status, msg = client_error_status(e)
    return response.status_generic_error(status=status, body=msg)


async def list_objects(s3: S3Client,
                       bucket_id: str,
                       prefix: str | None = None,
                       max_keys: int | None = None,
                       loop: AbstractEventLoop | None = None,
                       delimiter: str | None = None,
                       include_restore_status: bool | None = None) -> AsyncIterator[Mapping[str, Any]]:
    if not loop:
        loop_ = asyncio.get_running_loop()
    else:
        loop_ = loop
    list_partial = partial(s3.get_paginator('list_objects_v2').paginate, Bucket=bucket_id)
    if max_keys is not None:
        list_partial = partial(list_partial, PaginationConfig={'MaxItems': max_keys})
    if prefix is not None:  # Boto3 will raise an exception if Prefix is set to None.
        list_partial = partial(list_partial, Prefix=prefix)
    if delimiter is not None:
        list_partial = partial(list_partial, Delimiter=delimiter)
    if include_restore_status is not None and include_restore_status:
        list_partial = partial(list_partial, OptionalObjectAttributes=['RestoreStatus'])
    pages = await loop_.run_in_executor(None, lambda: iter(list_partial()))
    while (page := await loop_.run_in_executor(None, next, pages, None)) is not None:
        for common_prefix in page.get('CommonPrefixes', []):
            yield common_prefix
        for content in page.get('Contents', []):
            yield content


async def is_versioning_enabled(s3: S3Client, bucket_id: str,
                                loop: asyncio.AbstractEventLoop | None = None,
                                thread_pool_executor: ThreadPoolExecutor | None = None) -> bool:
    """
    Returns true if versioning is either enabled or suspended. In other words, this function returns True if there
    may be versions to retrieve.

    :param s3: the S3 client (required).
    :param loop: optional event loop. If None or unspecified, the running loop will be used.
    :param thread_pool_executor: an optional thread pool executor.
    :return: True if versioning is enabled or suspended, False otherwise.
    """
    if not loop:
        loop_ = asyncio.get_running_loop()
    else:
        loop_ = loop
    response = await loop_.run_in_executor(thread_pool_executor, partial(s3.get_bucket_versioning, Bucket=bucket_id))
    return 'Status' in response


async def list_object_versions(s3: S3Client, bucket_id: str, prefix: str | None = None,
                               loop: asyncio.AbstractEventLoop | None = None,
                               filter_deleted: bool = False,
                               filter_folder: bool = False) -> AsyncIterator[Mapping[str, Any]]:
    """
    Gets all versions of the objects with the given prefix.

    :param s3: an S3 client (required).
    :param bucket_id: the bucket id (required).
    :param prefix: the key prefix. Will get all keys in the bucket if unspecified.
    :param loop: the event loop. Will use the current running loop if unspecified.
    :param filter_deleted: flag to filter out the deleted objects from listed versions.
    :param filter_folder: flag to filter out folders and only show objects versions
    :return: an asynchronous iterator of dicts with the following shape:
            'ETag': 'string',
            'ChecksumAlgorithm': [
                'CRC32'|'CRC32C'|'SHA1'|'SHA256',
            ],
            'Size': 123,
            'StorageClass': 'STANDARD',
            'Key': 'string',
            'VersionId': 'string',
            'IsLatest': True|False,
            'LastModified': datetime(2015, 1, 1),
            'Owner': {
                'DisplayName': 'string',
                'ID': 'string'
            }
    """
    if not loop:
        loop_ = asyncio.get_running_loop()
    else:
        loop_ = loop
    list_partial = partial(s3.get_paginator('list_object_versions').paginate, Bucket=bucket_id)
    if prefix is not None:  # Boto3 will raise an exception if Prefix is set to None.
        list_partial = partial(list_partial, Prefix=prefix)
    pages = await loop_.run_in_executor(None, lambda: iter(list_partial()))
    while (page := await loop_.run_in_executor(None, next, pages, None)) is not None:
        if filter_deleted:
            deleted_markers = page.get('DeleteMarkers', [])
            dm_keys = {dm['Key'] for dm in deleted_markers}
        for obj in page.get('Versions', []):
            if (filter_folder and is_folder(obj.get("Key"))) or (filter_deleted and obj.get('Key') in dm_keys):
                continue
            yield obj

async def get_latest_object_version(s3: S3Client, bucket_id: str, key: str,
                                    loop: asyncio.AbstractEventLoop | None = None) -> Mapping[str, Any] | None:
    async for obj in list_object_versions(s3, bucket_id=bucket_id, prefix=key, loop=loop):
        if obj['Key'] == key and obj['IsLatest']:
            return obj
    return None



async def get_object_versions_by_key(s3: S3Client, bucket_id: str, prefix: str | None = None,
                                     loop: asyncio.AbstractEventLoop | None = None) -> dict[str, list[Mapping[str, Any]]]:
    versions_by_key: dict[str, list[Mapping[str, Any]]] = {}
    async for v in list_object_versions(s3, bucket_id, prefix, loop):
        versions_by_key.setdefault(v['Key'], []).append(v)
    return versions_by_key


async def return_bucket_status_or_not_found(bucket_name, loop, s3):
    if loop is None:
        loop = asyncio.get_running_loop()
    try:
        await loop.run_in_executor(None, partial(s3.head_bucket, Bucket=bucket_name))
        return response.status_not_found()
    except BotoClientError as e:
        return handle_client_error(e)


def decode_folder(folder_id_: str) -> str | None:
    """
    Decodes a folder id to an S3 key.

    :param folder_id_: the folder id. A value of 'root' is decoded to the empty string.
    :return: the folder's key, or None if the id is invalid.
    """
    if folder_id_ == ROOT_FOLDER.id:
        folder_id = ''
    else:
        try:
            folder_id = decode_key(folder_id_)
            if not is_folder(folder_id):
                folder_id = None
        except KeyDecodeException:
            # Let the bucket query happen so that we consistently return Forbidden if the user lacks permissions
            # for the bucket.
            folder_id = None
    return folder_id


def s3_object_display_name(bucket_name: str, key: str | None) -> str:
    """
    Function for use with heaserver.service.aiohttp.http_error_message() to generate names of S3 buckets and objects
    for use in error messages.

    :param bucket_name: the name of an S3 bucket (required).
    :param key: an optional key for objects in a bucket.
    """
    return f'{display_name(key)} in bucket {bucket_name}' if key is not None else bucket_name


def http_error_message(http_error: web.HTTPError, bucket_name: str, key: str | None) -> web.HTTPError:
    """
    If the HTTPError object has an empty body, it will try filling in the body with a message appropriate for the given
    status code for operations on desktop objects from AWS. Uses s3_object_display_name() to generate the message.

    :param http_error: the HTTPError (required).
    :param bucket_name: the bucket name (required).
    :param key: the key.
    :return: the updated HTTPError.
    """
    return aiohttp.http_error_message(http_error, s3_object_display_name, bucket_name, key)


async def _delete_object(s3_client: S3Client, bucket_name: str, key: str, recursive: bool,
                         delete_completed_cb: Callable[[str, str], Awaitable[None]] | None = None) -> Response:
    """
    Delete the object with the given key in the given bucket. If the key is a prefix, and recursive is True, delete
    all objects with the given prefix.

    :param s3_client: the S3 client (required).
    :param bucket_name: the bucket (required).
    :param key: the key or prefix (required).
    :param recursive: whether or not to treat the key as a prefix and delete all objects with the given prefix
    (required).
    :param delete_completed_cb: called upon successful deletion of an object. Must be reentrant. The callable must
    accept two parameters: the bucket name and the object's key.
    :return: the HTTP response.
    """
    loop = asyncio.get_running_loop()
    try:
        if key is None:
            return await return_bucket_status_or_not_found(bucket_name, loop, s3_client)

        async def gen():
            root = None
            async for obj in list_objects(s3_client, bucket_name, prefix=key, loop=loop):
                if root is not None and not recursive:
                    raise response.status_bad_request(f'The folder {key} is not empty')
                elif root is None:
                    root = obj
                else:
                    yield obj
            if root is not None:
                yield root
            else:
                raise await return_bucket_status_or_not_found(bucket_name, loop, s3_client)
        async def item_processor(item: Mapping[str, Any]):
            key_ = item['Key']
            await loop.run_in_executor(None, partial(s3_client.delete_object, Bucket=bucket_name, Key=key_))
            if delete_completed_cb:
                await delete_completed_cb(bucket_name, key_)
        await queued_processing(gen, item_processor)
        return await response.delete(True)
    except BotoClientError as e:
        return handle_client_error(e)
    except HTTPException as e:
        # Return the exception/response rather than raise it.
        return e


async def _object_exists_with_prefix(s3_client: S3Client, bucket_name: str, prefix: str):
    """
    Return whether there are any objects with the given key prefix.

    :param s3_client: the S3 client (required).
    :param bucket_name: the bucket name (required).
    :param prefix: the key prefix (required).
    """
    # head_object doesn't 'see' folders, need to use list_objects to see if a folder exists.
    obj = await anext(list_objects(s3_client, bucket_id=bucket_name, prefix=prefix, max_keys=1), None)
    return obj is not None


async def _object_exists(s3_client: S3Client, bucket_name: str, key: str):
    """
    Return whether there exists an object with the given key.

    :param s3_client: the S3 client (required).
    :param bucket_name: the bucket name (required).
    :param key: the key (required).
    """
    # head_object doesn't 'see' folders, need to use list_objects to see if a folder exists.
    obj = await anext(list_objects(s3_client, bucket_id=bucket_name, prefix=key, max_keys=1), None)
    return obj is not None and obj['Key'] == key


async def _copy_object(s3_client: S3Client, source_bucket_name, source_key, target_bucket_name,
                       target_key, copy_completed_cb: Callable[[str, str, str, str], Awaitable[None]] | None = None) -> web.Response:
    logger = logging.getLogger(__name__)

    # First, make sure the target is a folder
    if target_key and not is_folder(target_key):
        return response.status_bad_request(f'Target {display_name(target_key)} is not a folder')

    # Next, make sure the source exists.
    if not await _object_exists_with_prefix(s3_client, source_bucket_name, source_key):
        return response.status_bad_request(f'Source {display_name(source_key)} does not exist in bucket {source_bucket_name}')

    # Next make sure that the target folder exists.
    if target_key and not await _object_exists_with_prefix(s3_client, target_bucket_name, target_key):
        return response.status_bad_request(f'Target {display_name(target_key)} does not exist in bucket {source_bucket_name}')

    # Next check if we would be clobbering something in the target location.
    try:
        key_to_check = replace_parent_folder(source_key, target_key, parent(source_key) if source_key else None)
        if await _object_exists(s3_client, target_bucket_name, key_to_check):
            return response.status_bad_request(
                f'Object {display_name(key_to_check)} already exists in target bucket {target_bucket_name}')
    except BotoClientError as e:
        return handle_client_error(e)

    # Finally make sure that the target folder is not a subfolder of the source folder.
    if source_bucket_name == target_bucket_name and (target_key or '').startswith(source_key or ''):
        return response.status_bad_request(f'Target folder {display_name(target_key)} is a subfolder of {display_name(source_key)}')

    try:
        loop = asyncio.get_running_loop()

        async def _do_copy() -> AsyncIterator[asyncio.Future[None]]:
            source_key_folder = split(source_key)[0]
            def do_copy(source_key_, target_key_):
                s3_client.copy({'Bucket': source_bucket_name, 'Key': source_key_}, target_bucket_name, target_key_)
                return source_key_, target_key_
            logger.debug('Copying from bucket %s and prefix %s to bucket %s and target key %s', source_bucket_name, source_key, target_bucket_name, target_key)
            cached_values: list[Mapping[str, Any]] = []
            async for obj in list_objects(s3_client, source_bucket_name, prefix=source_key, include_restore_status=True):
                logger.debug('copy candidate: %s', obj)
                if obj['StorageClass'] in (S3StorageClass.DEEP_ARCHIVE.name, S3StorageClass.GLACIER.name) and not ((restore := obj.get('RestoreStatus')) and restore.get('RestoreExpiryDate')):
                    if is_folder(source_key):
                        raise response.status_bad_request(f'{_activity_object_display_name(source_bucket_name, source_key)} contains archived objects')
                    else:
                        raise response.status_bad_request(f'{_activity_object_display_name(source_bucket_name, source_key)} is archived')
                elif len(cached_values) < 1000:
                    cached_values.append(obj)
            if len(cached_values) <= 1000:
                for obj in cached_values:
                    source_key_ = obj['Key']
                    target_key_ = replace_parent_folder(source_key=source_key_, target_key=target_key, source_key_folder=source_key_folder)
                    logger.debug('Copying %s/%s to %s/%s', source_bucket_name, source_key_, target_bucket_name, target_key_)
                    yield loop.run_in_executor(None, do_copy, source_key_, target_key_)
            else:
                async for obj in list_objects(s3_client, source_bucket_name, prefix=source_key):
                    source_key_ = obj['Key']
                    target_key_ = replace_parent_folder(source_key=source_key_, target_key=target_key, source_key_folder=source_key_folder)
                    logger.debug('Copying %s/%s to %s/%s', source_bucket_name, source_key_, target_bucket_name, target_key_)
                    yield loop.run_in_executor(None, do_copy, source_key_, target_key_)

        async def process_item(item):
            source_key_, target_key_ = await item
            if copy_completed_cb:
                await copy_completed_cb(source_bucket_name, source_key_, target_bucket_name, target_key_)

        await queued_processing(_do_copy, process_item)

        return web.HTTPCreated()
    except BotoClientError as e_:
        return handle_client_error(e_)
    except ValueError as e_:
        return response.status_internal_error(str(e_))

async def _archive_object(s3_client: S3Client, source_bucket_name: str, source_key_name: str,
                          storage_class: str) -> web.Response:
    logger = logging.getLogger(__name__)
    try:
        source_resp = s3_client.list_objects_v2(Bucket=source_bucket_name, Prefix=source_key_name.rstrip('/'),
                                                Delimiter="/")
        if not source_resp.get('CommonPrefixes', None):
            # key is either file or doesn't exist
            s3_client.head_object(Bucket=source_bucket_name,
                                  Key=source_key_name)  # check if source object exists, if not throws an exception
            source_key = source_key_name
        else:
            source_key = source_key_name if source_key_name.endswith('/') else f"{source_key_name}/"

        loop = asyncio.get_running_loop()

        async def _do_copy() -> AsyncIterator[asyncio.Future[None]]:
            async for obj in list_objects(s3_client, source_bucket_name, prefix=source_key):
                if obj['Key'].endswith("/") or storage_class == obj['StorageClass']:
                    continue
                p = partial(s3_client.copy,
                            {'Bucket': source_bucket_name, 'Key': obj['Key']},
                            source_bucket_name, obj['Key'],
                            ExtraArgs={
                                'StorageClass': storage_class,
                                'MetadataDirective': 'COPY'
                            } if storage_class else None)
                logger.debug('Copying %s/%s to %s/%s', source_bucket_name, obj['Key'], source_bucket_name,
                             object)
                yield loop.run_in_executor(None, p)

        async def process_item(item):
            await item

        def exceptions_to_ignore(e: Exception) -> bool:
            if isinstance(e, BotoClientError):
                # For folders some objects could already be archived, if object already archived just skip.
                logger.debug('Error response while archiving (is ignored if the object is already archived): %s', e.response)
                error = e.response['Error']
                if error['Code'] == 'InvalidObjectState' and storage_class == error['StorageClass']:  # type:ignore[typeddict-item]
                    return True
            return False

        await queued_processing(_do_copy, process_item, exceptions_to_ignore=exceptions_to_ignore)

        return web.HTTPCreated()
    except BotoClientError as e_:
        return handle_client_error(e_)

def _activity_object_display_name(bucket_name: str, key: str | None) -> str:
    return s3_object_display_name(bucket_name, key)

async def _extract_source(match_info: dict[str, Any]) -> tuple[str, str]:
    source_bucket_name = match_info['bucket_id']
    try:
        source_key_name = decode_key(match_info['id']) if 'id' in match_info else None
    except KeyDecodeException as e:
        raise web.HTTPBadRequest(body=str(e)) from e
    if source_bucket_name is None or source_key_name is None:
        raise web.HTTPBadRequest(body='Invalid request URL')
    return source_bucket_name, source_key_name


class TargetInfo(NamedTuple):
    url: str
    bucket_name: str
    key: str
    volume_id: str


async def _copy_object_extract_target(body: dict[str, Any]) -> TargetInfo:
    """
    Extracts the bucket name and folder key from the target property of a Collection+JSON template. It un-escapes them
    as needed.

    :param body: a Collection+JSON template dict.
    :return: a named tuple with the target URL (an absolute URL), the un-escaped bucket name, the folder key, and the volume id
    :raises web.HTTPBadRequest: if the given body is invalid.
    """
    try:
        target_url = next(
            item['value'] for item in body['template']['data'] if item['name'] == 'target')
        vars_ = tvars(route='http{prefix}/volumes/{volume_id}/buckets/{bucket_id}/{folderorproject}/{id}',
                      url=str(URL(target_url).with_query(None).with_fragment(None)))
        # FIXME: may need to fetch the target to see what it is to be maximally reliable and generalizable.
        if 'folderorproject' in vars_ and vars_['folderorproject'] not in ('awss3folders', 'awss3projects'):
            raise ValueError('Not a folder or project')
        bucket_id = vars_['bucket_id']
        assert isinstance(bucket_id, str), 'bucket_id not a str'
        target_bucket_name = unquote(bucket_id)
        id_ = vars_.get('id')
        assert isinstance(id_, (str, type(None))), 'id not a str nor None'
        target_folder_name = decode_key(unquote(id_)) if id_ is not None else ''
        if target_folder_name and not is_folder(target_folder_name):
            raise web.HTTPBadRequest(reason=f'Target {target_url} is not a folder')
        volume_id = vars_['volume_id']
        assert isinstance(volume_id, str), 'volume_id not a str'
        return TargetInfo(url=target_url, bucket_name=target_bucket_name, key=target_folder_name, volume_id=volume_id)
    except (KeyError, ValueError, KeyDecodeException) as e:
        raise web.HTTPBadRequest(body=f'Invalid target: {e}') from e


class RestoreTier(Enum):
    Standard = auto()
    Bulk = auto()
    Expedited = auto()


class UnarchiveInfo:
    days: int
    restore_tier: RestoreTier


async def _extract_unarchive_params(body: dict[str, Any]) -> UnarchiveInfo:
    """
    Extracts the unarchived properties of a Collection+JSON template.

    :param body: a Collection+JSON template dict.
    :return: a Object UnarchiveInfo with days and restore_tier properties
    :raises web.HTTPBadRequest: if the given body is invalid.
    """
    try:
        unarchive_params_dict = {item['name']: item['value'] for item in body['template']['data']}
        unarchive_params = UnarchiveInfo()
        unarchive_params.days = int(unarchive_params_dict['days'])

        if unarchive_params_dict['restore_tier'] == RestoreTier.Standard.name:
            unarchive_params.restore_tier = RestoreTier.Standard
        elif unarchive_params_dict['restore_tier'] == RestoreTier.Expedited.name:
            unarchive_params.restore_tier = RestoreTier.Expedited
        elif unarchive_params_dict['restore_tier'] == RestoreTier.Bulk.name:
            unarchive_params.restore_tier = RestoreTier.Bulk
        else:
            raise ValueError(f"The value {unarchive_params_dict['restore_tier']} is not a valid Restore Tier")

        return unarchive_params
    except (KeyError, ValueError, KeyDecodeException) as e:
        raise web.HTTPBadRequest(body=f'Invalid Unarchive Params: {e}') from e


async def _create_object(s3_client: S3Client, bucket_name: str, key: str) -> web.Response:
    if bucket_name is None:
        raise ValueError('bucket_name cannot be None')
    if key is None:
        raise ValueError('key cannot be None')
    logger = logging.getLogger(__name__)
    loop = asyncio.get_running_loop()
    try:
        response_ = await loop.run_in_executor(None, partial(s3_client.head_object, Bucket=bucket_name,
                                                             Key=key))  # check if object exists, if not throws an exception
        logger.debug('Result of creating object %s: %s', key, response_)
        return response.status_bad_request(body=f"Object {display_name(key)} already exists")
    except BotoClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == CLIENT_ERROR_404:  # folder doesn't exist
            await loop.run_in_executor(None, partial(s3_client.put_object, Bucket=bucket_name, Key=key))
            return web.HTTPCreated()
        else:
            return handle_client_error(e)
    except ParamValidationError as e:
        return response.status_bad_request(str(e))
