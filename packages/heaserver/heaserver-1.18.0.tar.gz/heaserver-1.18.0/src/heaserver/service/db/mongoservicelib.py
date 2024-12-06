import heaobject.root
from .. import response
from ..heaobjectsupport import new_heaobject_from_type, RESTPermissionGroup
from ..appproperty import HEA_DB, HEA_CACHE
from .mongo import MongoContext
from heaobject.error import DeserializeException
from aiohttp.web import Request, StreamResponse, Response, HTTPError
from typing import Any, AsyncGenerator, Literal, IO
from heaobject.root import DesktopObject, DesktopObjectDict, desktop_object_from_dict, Permission, PermissionContext
from heaobject.user import NONE_USER
from heaserver.service.oidcclaimhdrs import SUB
from pymongo.errors import WriteError, DuplicateKeyError
from collections.abc import Sequence, Mapping
import logging


async def get_dict(request: Request, collection: str, volume_id: str | None = None) -> DesktopObjectDict | None:
    """
    Gets the requested desktop object as a desktop object dict.

    :param request: the HTTP request, which must have an id value in the match_info mapping. Required.
    :param collection: the Mongo collection name. Required.
    :param volume_id: the id string of the volume containing the requested HEA
    object. If None, the root volume is assumed.
    :return: a desktop object dict or None if the object was not found.
    """
    sub = request.headers.get(SUB, NONE_USER)
    cache_key = (sub, collection, f'id^{request.match_info["id"]}')
    cached_value = request.app[HEA_CACHE].get(cache_key)
    if cached_value is not None:
        return cached_value
    else:
        async with MongoContext(request, volume_id) as mongo:
            result = await mongo.get(request, collection, var_parts='id',
                                    sub=request.headers.get(SUB))

            if result is not None:
                obj = heaobject.root.desktop_object_from_dict(result)
                permitted = await obj.has_permissions(perms=RESTPermissionGroup.GETTER_PERMS,
                                                      context=PermissionContext[DesktopObject](sub=sub))
                if not permitted:
                    return None
                request.app[HEA_CACHE][cache_key] = result
            return result


async def get(request: Request, collection: str, volume_id: str | None = None) -> Response:
    """
    Gets the desktop object with the specified id. The desktop object is
    formatted according to the requested mime types in the HTTP request's
    Accept header as one of the formats supported by the
    heaserver.service.representor module.

    :param request: the HTTP request, which must have an id value in the match_info mapping. Required.
    :param collection: the Mongo collection name. Required.
    :param volume_id: the id string of the volume containing the requested HEA object. If None, the root volume is
    assumed.
    :return: a Response with the requested HEA object or Not Found.
    """
    sub = request.headers.get(SUB, NONE_USER)
    result = await get_dict(request, collection, volume_id)
    if result is None:
        return await response.get(request, None)
    else:
        obj = desktop_object_from_dict(result)
        sub = request.headers.get(SUB, NONE_USER)
        context = PermissionContext[DesktopObject](sub)
        return await response.get(request, obj.to_dict(), await obj.get_permissions(context),
                                  await obj.get_all_attribute_permissions(context))


async def get_content(request: Request, collection: str, volume_id: str | None = None) -> StreamResponse:
    """
    Gets the HEA object's associated content.

    :param request: the HTTP request. Required.
    :param collection: the Mongo collection name. Required.
    :param volume_id: the id string of the volume containing the requested HEA object. If None, the root volume is
    assumed.
    :return: an aiohttp StreamResponse with the requested HEA object or Not Found.
    """
    sub = request.headers.get(SUB, NONE_USER)
    async with MongoContext(request, volume_id) as mongo:
        result = await mongo.get(request, collection, var_parts='id', sub=request.headers.get(SUB))

        if result is not None:
            obj = heaobject.root.desktop_object_from_dict(result)
            permitted = await obj.has_permissions(perms=RESTPermissionGroup.GETTER_PERMS,
                                                  context=PermissionContext[DesktopObject](sub=sub))
            if not permitted:
                return response.status_not_found()
        out = await mongo.get_content(request, collection, var_parts='id', sub=request.headers.get(SUB))
        if out is not None:
            return await response.get_streaming(request, out, 'text/plain')
        else:
            return response.status_not_found()


async def get_by_name(request: Request, collection: str,
                      volume_id: str | None = None) -> Response:
    """
    Gets an HTTP response object with the requested desktop object in the body.
    The desktop object is formatted according to the requested mime types in
    the HTTP request's Accept header as one of the formats supported by the
    heaserver.service.representor module.

    :param request: the HTTP request, which must have a name value in the match_info mapping. Required.
    :param collection: the Mongo collection name. Required.
    :param volume_id: the id string of the volume containing the requested
    desktop object. If None, the root volume is assumed.
    :return: a Response with the requested desktop object or Not Found.
    """
    sub = request.headers.get(SUB, NONE_USER)
    result = await get_by_name_dict(request, collection, volume_id)
    if result is None:
        return await response.get(request, None)
    else:
        obj = desktop_object_from_dict(result)
        context = PermissionContext[DesktopObject](sub)
        return await response.get(request, desktop_object_from_dict(result).to_dict() if result is not None else None,
                                  permissions=await obj.get_permissions(context),
                                  attribute_permissions=await obj.get_all_attribute_permissions(context))

async def get_by_name_dict(request: Request, collection: str,
                           volume_id: str | None = None) -> DesktopObjectDict | None:
    """
    Gets the requested desktop object as a desktop object dict.

    :param request: the HTTP request, which must have a name value in the match_info mapping. Required.
    :param collection: the Mongo collection name. Required.
    :param volume_id: the id string of the volume containing the requested HEA
    object. If None, the root volume is assumed.
    :return: a desktop object dict or None if the object was not found.
    """
    sub = request.headers.get(SUB, NONE_USER)
    cache_key = (sub, collection, f'name^{request.match_info["name"]}')
    cached_value = request.app[HEA_CACHE].get(cache_key)
    if cached_value is not None:
        return cached_value
    else:
        async with MongoContext(request, volume_id) as mongo:
            result = await mongo.get(request, collection, var_parts='name',
                                    sub=request.headers.get(SUB))

            if result is not None:
                obj = heaobject.root.desktop_object_from_dict(result)
                permitted = await obj.has_permissions(perms=RESTPermissionGroup.GETTER_PERMS,
                                                      context=PermissionContext[DesktopObject](sub=sub))
                if not permitted:
                    return None
                request.app[HEA_CACHE][cache_key] = result
            return result


async def get_all(request: Request,
                  collection: str,
                  volume_id: str | None = None,
                  mongoattributes: Any | None = None,
                  sort: dict[str, Literal[-1, 1]] | None = None) -> Response:
    """
    Gets an HTTP response with all requested desktop objects in the body.
    The desktop objects are formatted according to the requested mime types in
    the HTTP request's Accept header as one of the formats supported by the
    heaserver.service.representor module.

    :param request: the HTTP request. Required.
    :param collection: the Mongo collection name. Required.
    :param volume_id: the id string of the volume containing the requested HEA
    object. If None, the root volume is assumed.
    :param sort: the sort order of the desktop objects as a dict of desktop
    object attribute to 1 or -1 for ascending or descending.
    :return: a Response with a list of HEA object dicts. If no desktop objects
    are found, the body will contain an empty list.
    """
    sub = request.headers.get(SUB, NONE_USER)
    if mongoattributes is None and not request.query:
        cache_key = (sub, collection, None, tuple((key, val) for key, val in (sort or {}).items()))
        cached_value = request.app[HEA_CACHE].get(cache_key)
    else:
        cached_value = None
    if mongoattributes is None and cached_value is not None:
        return await response.get_all(request, cached_value)
    else:
        objs: list[DesktopObject] = []
        l: list[DesktopObjectDict] = []
        async for obj in _get_all_gen(request, collection, volume_id, mongoattributes, sort):
            objs.append(obj)
            l.append(obj.to_dict())
        if mongoattributes is None and not request.query:
            request.app[HEA_CACHE][cache_key] = l
        perms: list[list[Permission]] = []
        attr_perms: list[dict[str, list[Permission]]] = []
        context = PermissionContext[DesktopObject](sub)
        for obj in objs:
            perms.append(await obj.get_permissions(context))
            attr_perms.append(await obj.get_all_attribute_permissions(context))
        return await response.get_all(request, l, permissions=perms, attribute_permissions=attr_perms)

async def get_all_dict(request: Request,
                       collection: str,
                       volume_id: str | None = None,
                       mongoattributes: Any | None = None,
                       sort: dict[str, Literal[-1, 1]] | None = None) -> list[DesktopObjectDict]:
    """
    Gets all HEA objects as a list of desktop object dicts.

    :param request: the HTTP request. Required.
    :param collection: the Mongo collection name. Required.
    :param volume_id: the id string of the volume containing the requested HEA
    object. If None, the root volume is assumed.
    :param sort: the sort order of the desktop objects as a dict of desktop
    object attribute to 1 or -1 for ascending or descending.
    :return: a list of DesktopObjectDict. If no desktop objects are found, the
    return value will be an empty list.
    """
    sub = request.headers.get(SUB, NONE_USER)
    if mongoattributes is None and not request.query:
        cache_key = (sub, collection, None, sort)
        cached_value = request.app[HEA_CACHE].get(cache_key)
    else:
        cached_value = None
    if mongoattributes is None and cached_value is not None:
        return cached_value
    else:
        l: list[DesktopObjectDict] = []
        async for desktop_object in _get_all_gen(request, collection,
                                                volume_id=volume_id,
                                                mongoattributes=mongoattributes,
                                                sort=sort):
            l.append(desktop_object.to_dict())
        if mongoattributes is None and not request.query:
            request.app[HEA_CACHE][cache_key] = l
        return l


async def opener(request: Request, collection: str, volume_id: str | None = None,
                 include_desktop_object: bool = True) -> Response:
    """
    Gets choices for opening an HEA desktop object's content.

    :param request: the HTTP request. Required. If an Accepts header is provided, MIME types that do not support links
    will be ignored.
    :param collection: the Mongo collection name. Required.
    :param volume_id: the id string of the volume containing the requested HEA object. If None, the root volume is
    assumed.
    :return: a Response object with status code 300, and a body containing the HEA desktop object and links
    representing possible choices for opening the HEA desktop object; or Not Found.
    """
    sub = request.headers.get(SUB, NONE_USER)
    cache_key = (sub, collection, f"id^{request.match_info['id']}")
    cached_value = request.app[HEA_CACHE].get(cache_key)
    if include_desktop_object is None:
        include_desktop_object_ = True
    else:
        include_desktop_object_ = bool(include_desktop_object)
    if cached_value is not None:
        return await response.get_multiple_choices(request, cached_value if include_desktop_object_ else None)
    else:
        async with MongoContext(request, volume_id) as mongo:
            result = await mongo.get(request, collection, var_parts='id', sub=request.headers.get(SUB))
            if result is not None:
                obj = heaobject.root.desktop_object_from_dict(result)
                context = PermissionContext[DesktopObject](sub)
                if not await obj.has_permissions(perms=RESTPermissionGroup.GETTER_PERMS, context=context):
                    return response.status_not_found()
                request.app[HEA_CACHE][cache_key] = result
                return await response.get_multiple_choices(request, result if include_desktop_object_ else None)
            else:
                return response.status_not_found()



async def post(request: Request, collection: str, type_: type[DesktopObject], default_content: IO | None = None,
               volume_id: str | None = None, resource_base: str | None = None) -> Response:
    """
    Posts the desktop object from a request body.

    :param request: the HTTP request containing the desktop object. The object's owner and the request's OIDC_CLAIM_sub
    header must match.
    :param collection: the Mongo collection name. Required.
    :param type_: The HEA object type. Required. The type of the object in the request body is compared to this type
    for whether the object is an instance of the given type, and a response with a 400 status code is returned if it is
    not.
    :param default_content: an optional blank document or other default content as a file-like object. This must be not-None
    for any microservices that manage content.
    :param volume_id: the id string of the volume containing the requested HEA object. If None, the root volume is
    assumed.
    :param resource_base: the base path of the created resource. If None, the collection is used as the base path.
    :return: a Response object with a status of Created and the object's URI in the Location header, otherwise returns
    a Response with an appropriate status code.
    """
    logger = logging.getLogger(__name__)
    sub = request.headers.get(SUB, NONE_USER)
    try:
        obj = await new_heaobject_from_type(request, type_)
    except DeserializeException as e:
        return response.status_bad_request(str(e))
    if not await request.app[HEA_DB].is_creator(request, type(obj)):
        logger.debug('Permission denied to %s creating object %s', sub, obj)
        return response.status_forbidden(f'Permission denied creating object of type {type_.get_type_name()}')
    if obj.owner != sub:
        logger.debug('Permission denied to %s creating object with owner %s', sub, obj.owner)
        return response.status_forbidden(f'Permission denied creating object of type {type_.get_type_name()}')
    async with MongoContext(request, volume_id) as mongo:
        try:
            result = await mongo.post(request, obj, collection, default_content)
            to_delete = []
            for cache_key in request.app[HEA_CACHE]:
                if cache_key[1] == collection and cache_key[2] is None:
                    to_delete.append(cache_key)
            for cache_key in to_delete:
                request.app[HEA_CACHE].pop(cache_key, None)
            return await response.post(request, result, resource_base if resource_base is not None else collection)
        except DuplicateKeyError as e:
            return response.status_conflict(f'Object {obj.display_name} already exists')

async def post_dict_return_id(request: Request, obj_dict: DesktopObjectDict, collection: str,
                              type_: type[DesktopObject], default_content: IO | None = None,
                              volume_id: str | None = None) -> str | None:
    """
    Posts the desktop object from a request body.

    :param request: the HTTP request containing the desktop object. The object's owner and the request's OIDC_CLAIM_sub
    header must match.
    :param obj_dict: the object to create (required).
    :param collection: the Mongo collection name. Required.
    :param type_: The HEA object type. Required. The type of the object in the request body is compared to this type
    for whether the object is an instance of the given type, and a response with a 400 status code is returned if it is
    not.
    :param default_content: an optional blank document or other default content as a file-like object. This must be not-None
    for any microservices that manage content.
    :param volume_id: the id string of the volume containing the requested HEA object. If None, the root volume is
    assumed.
    :return: the created object's id.
    :raises HTTPError: if an error occurs creating the object on the server.
    """
    logger = logging.getLogger(__name__)
    sub = request.headers.get(SUB, NONE_USER)
    owner = obj_dict.get('owner')
    if sub != owner:
        logger.debug('Permission denied to %s creating object %s', sub, obj_dict)
        raise response.status_forbidden(f'Permission denied creating object with owner {owner}')
    try:
        obj = desktop_object_from_dict(obj_dict)
    except (DeserializeException, ValueError, TypeError) as e:
        raise response.status_bad_request(str(e))
    async with MongoContext(request, volume_id) as mongo:
        try:
            return await mongo.post(request, obj, collection, default_content)
        except DuplicateKeyError as e:
            raise response.status_conflict(f'Object {obj.display_name} already exists')

async def post_dict(request: Request, obj_dict: DesktopObjectDict, collection: str, type_: type[DesktopObject],
                    default_content: IO | None = None, volume_id: str | None = None,
                    resource_base: str | None = None) -> Response:
    """
    Posts a desktop object dict.

    :param request: the HTTP request (required). The owner property in the obj_dict parameter and the request's
    OIDC_CLAIM_sub header must match.
    :param obj_dict: a desktop object dict (required).
    :param collection: the Mongo collection name (required).
    :param type_: The HEA object type. Required. The type of the object in the request body is compared to this type
    for whether the object is an instance of the given type, and a response with a 400 status code is returned if it is
    not.
    :param default_content: an optional blank document or other default content as a file-like object. This must be not-None
    for any microservices that manage content.
    :param volume_id: the id string of the volume containing the requested HEA object. If None, the root volume is
    assumed.
    :param resource_base: the base path of the created resource. If None, the collection is used as the base path.
    :return: a Response object with a status of Created and the object's URI in the Location header if the request was
    successful, otherwise a Response object with an error status code.
    """
    try:
        result = await post_dict_return_id(request, obj_dict, collection, type_, default_content, volume_id)
        return await response.post(request, result, resource_base if resource_base is not None else collection)
    except HTTPError as e:
        return e

async def put(request: Request, collection: str, type_: type[DesktopObject], volume_id: str | None = None,
              obj: DesktopObject | None = None) -> Response:
    """
    Updates the HEA object with the specified id.

    :param request: the HTTP request. Required.
    :param collection: the Mongo collection name. Required.
    :param type_: The HEA object type. Required.
    :param volume_id: the id string of the volume containing the requested HEA object. If None, the root volume is
    assumed.
    :param obj: desktop object to use instead of what is in the request body (optional). There will be no validation
    performed on the PUT body.
    :return: a Response object with a status of No Content, Forbidden, or Not Found.
    """
    sub = request.headers.get(SUB, NONE_USER)
    async with MongoContext(request, volume_id) as mongo:
        if obj is not None:
            obj_ = obj
        else:
            try:
                obj_ = await new_heaobject_from_type(request, type_)
            except DeserializeException as e:
                return response.status_bad_request(str(e))
        try:
            context = PermissionContext[DesktopObject](sub)
            permitted = await obj_.has_permissions(perms=RESTPermissionGroup.PUTTER_PERMS, context=context)
            if not permitted:
                if await obj_.has_permissions(perms=RESTPermissionGroup.GETTER_PERMS, context=context):
                    return response.status_forbidden()
                else:
                    return response.status_not_found()

            result = await mongo.put(request, obj_, collection, sub=sub)  # if lacks permissions or object is not in database, then updates no records.
        except WriteError as e:
            err_msg = e.details.get('errmsg') if e.details else None
            if e.code == 66:
                return response.status_bad_request(err_msg)
            else:
                return response.status_internal_error(err_msg)
        if result is not None and result.matched_count:
            to_delete = []
            for cache_key in request.app[HEA_CACHE]:
                if cache_key[1] == collection and cache_key[2] in (None, f"id^{request.match_info['id']}"):
                    to_delete.append(cache_key)
            for cache_key in to_delete:
                request.app[HEA_CACHE].pop(cache_key, None)
        return await response.put(bool(result.matched_count if result is not None else None))

async def upsert(request: Request, collection: str, type_: type[DesktopObject], volume_id: str | None = None, filter: Mapping[str, Any] | None = None) -> Response:
    """
    Updates the HEA object, using the specified filter if provided otherwise the object's id, and inserting a new object
    if none matches the filter or the id.

    :param request: the HTTP request. Required.
    :param collection: the Mongo collection name. Required.
    :param type_: The HEA object type. Required.
    :param volume_id: the id string of the volume containing the requested HEA object. If None, the root volume is
    assumed.
    :param filter: optional filter criteria.
    :return: a Response object with a status of No Content, Forbidden, or Not Found.
    """
    sub = request.headers.get(SUB, NONE_USER)
    async with MongoContext(request, volume_id) as mongo:
        try:
            obj = await new_heaobject_from_type(request, type_)
        except DeserializeException as e:
            return response.status_bad_request(str(e).encode())
        try:
            context = PermissionContext[DesktopObject](sub)
            permitted = await obj.has_permissions(perms=RESTPermissionGroup.PUTTER_PERMS, context=context) and \
                await obj.has_permissions(perms=RESTPermissionGroup.POSTER_PERMS, context=context)
            if not permitted:
                if await obj.has_permissions(perms=RESTPermissionGroup.GETTER_PERMS, context=context):
                    return response.status_forbidden()
                else:
                    return response.status_not_found()

            result = await mongo.upsert_admin(obj, collection, mongoattributes=filter)
        except WriteError as e:
            err_msg = e.details.get('errmsg') if e.details is not None else None
            if e.code == 66:
                return response.status_bad_request(err_msg)
            else:
                return response.status_internal_error(err_msg)
        to_delete = []
        for cache_key in request.app[HEA_CACHE]:
            if cache_key[1] == collection and cache_key[2] in (None, f"id^{request.match_info['id']}"):
                to_delete.append(cache_key)
        for cache_key in to_delete:
            request.app[HEA_CACHE].pop(cache_key, None)
        return await response.put(bool(result))


async def put_content(request: Request, collection: str, type_: type[DesktopObject], volume_id: str | None = None) -> Response:
    """
    Updates the HEA object's associated content.

    :param request: the HTTP request. Required.
    :param collection: the Mongo collection name. Required.
    :param type_: The HEA object type. Required.
    :param volume_id: the id string of the volume containing the requested HEA object. If None, the root volume is
    assumed.
    :return: a Response object with a status of No Content, Forbidden, or Not Found.
    """
    async with MongoContext(request, volume_id) as mongo:
        sub = request.headers.get(SUB, NONE_USER)
        result = await mongo.get(request, collection, var_parts='id', sub=sub)

        if result is not None:
            obj = heaobject.root.desktop_object_from_dict(result)
            context = PermissionContext[DesktopObject](sub)
            permitted = await obj.has_permissions(perms=RESTPermissionGroup.PUTTER_PERMS, context=context)
            if not permitted:
                if await obj.has_permissions(perms=RESTPermissionGroup.GETTER_PERMS, context=context):
                    return response.status_forbidden()
                else:
                    return response.status_not_found()
            result2 = await mongo.put_content(request, collection, sub=sub)  # if lacks permissions, then updates no records.
            return await response.put(result2)
        else:
            return response.status_not_found()


async def delete(request: Request, collection: str, volume_id: str | None = None) -> Response:
    """
    Deletes the HEA object with the specified id and any associated content.

    :param request: the HTTP request. Required.
    :param collection: the Mongo collection name. Required.
    :param volume_id: the id string of the volume containing the requested HEA object. If None, the root volume is
    assumed.
    :return: No Content, Forbidden, or Not Found.
    """
    async with MongoContext(request, volume_id) as mongo:
        sub = request.headers.get(SUB, NONE_USER)
        obj = await mongo.get(request, collection, var_parts='id', sub=request.headers.get(SUB))

        if obj is not None:
            obj_ = heaobject.root.desktop_object_from_dict(obj)
            context = PermissionContext[DesktopObject](sub)
            permitted = await obj_.has_permissions(perms=RESTPermissionGroup.DELETER_PERMS, context=context)
            if not permitted:
                return response.status_forbidden()
            delete_result = await mongo.delete(request, collection, var_parts='id', sub=sub)  # if lacks permissions, then deletes no records.
            if delete_result and delete_result.deleted_count:
                to_delete = []
                for cache_key in request.app[HEA_CACHE]:
                    if cache_key[1] == collection and cache_key[2] in (None, f"id^{request.match_info['id']}"):
                        to_delete.append(cache_key)
                for cache_key in to_delete:
                    request.app[HEA_CACHE].pop(cache_key, None)
            return await response.delete(bool(delete_result.deleted_count) if delete_result else False)
        else:
            return response.status_not_found()



async def ping(request: Request) -> Response:
    """
    Sends a ping command to the database.

    :param request: the HTTP request.
    :return: an HTTP response with status code 200 if the ping is successful, 500 otherwise.
    """
    async with MongoContext(request) as mongo:
        try:
            await mongo.ping()
            return response.status_ok()
        except Exception as e:  # The exact exception is not documented.
            raise response.status_internal_error() from e

async def aggregate(request: Request, collection: str,
                    pipeline: Sequence[Mapping[str, Any]], volume_id: str | None = None) -> Response:
    """
    Execute an aggregation pipeline that returns a list of desktop object dicts that the current user has access to.

    :param request: the HTTP request (required).
    :param collection. The Mongo collection name (required).
    :param volume_id: the volume_id of the Mongo database. If None, the root volume is assumed.
    :return: a 200 status code response with the desktop object dicts from the pipeline.
    """
    async with MongoContext(request, volume_id) as mongo:
        sub = request.headers.get(SUB, NONE_USER)
        result: list[DesktopObject] = []
        permissions: list[list[Permission]] = []
        async for r in mongo.aggregate(collection, pipeline):
            obj = heaobject.root.desktop_object_from_dict(r)
            context = PermissionContext[DesktopObject](sub)
            permitted = await obj.has_permissions(perms=RESTPermissionGroup.GETTER_PERMS.perms, context=context)
            if permitted:
                permissions.append(await obj.get_permissions(context))
                result.append(obj)
        return await response.get_all(request, [obj.to_dict() for obj in result], permissions=permissions)


async def _get_all_gen(request: Request,
                      collection: str,
                      volume_id: str | None = None,
                      mongoattributes: Any | None = None,
                      sort: dict[str, Literal[-1, 1]] | None = None) -> AsyncGenerator[DesktopObject, None]:
    """
    Gets an async generator of all HEA objects as desktop object dicts. Does no caching.

    :param request: the HTTP request. Required.
    :param collection: the Mongo collection name. Required.
    :param volume_id: the id string of the volume containing the requested HEA
    object. If None, the root volume is assumed.
    :param sort: the sort order of the desktop objects as a dict of desktop
    object attribute to 1 or -1 for ascending or descending.
    :return: an async generator of DesktopObject.
    """
    sub = request.headers.get(SUB, NONE_USER)
    context = PermissionContext[DesktopObject](sub)
    async with MongoContext(request, volume_id) as mongo:
        async for r in mongo.get_all(request, collection, mongoattributes=mongoattributes, sub=sub, sort=sort):
            obj = heaobject.root.desktop_object_from_dict(r)
            if await obj.has_permissions(perms=RESTPermissionGroup.GETTER_PERMS, context=context):
                yield obj
