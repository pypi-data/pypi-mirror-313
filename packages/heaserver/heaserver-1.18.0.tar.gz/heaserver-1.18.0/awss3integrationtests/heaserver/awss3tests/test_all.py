from unittest import IsolatedAsyncioTestCase
from .awss3foldertestcase import AWSS3FolderTestCase
from heaserver.service.db import awsservicelib
from heaserver.service.db.aws import S3
from heaobject.awss3key import encode_key
import boto3
from botocore.exceptions import ClientError
from aiohttp import hdrs
from freezegun.api import FakeDatetime
from dateutil.tz import tzutc
from heaobject.user import NONE_USER
from moto import mock_aws


class TestS3GetAccount(IsolatedAsyncioTestCase):

    @mock_aws()
    def run(self, result):
        super().run(result)

    async def test_get_account(self):
        sts = boto3.client('sts')
        actual = await S3._get_basic_account_info(sts)
        self.assertEqual('123456789012', actual.id)


class TestAWSProperties(AWSS3FolderTestCase):
    async def test_get_property(self):
        async with self.client.request('GET', '/properties/CLOUD_AWS_CRED_URL') as resp:
            self.assertEqual(200, resp.status)

    async def test_get_property_not_found(self):
        async with self.client.request('GET', '/properties/TEST') as resp:
            self.assertEqual(404, resp.status)


class TestMockAWSAccount(AWSS3FolderTestCase):
    @mock_aws()
    def run(self, result):
        super().run(result)

    async def test_get_volume_id_for_account_id(self):
        async with self.client.request('GET', '/accounts/123456789012') as resp:
            self.assertEqual(200, resp.status)


class TestAWSServiceLib(AWSS3FolderTestCase):

    def setUp(self):
        super().setUp()
        self.s3 = boto3.client('s3')

    def tearDown(self):
        super().tearDown()
        self.s3.close()

    async def test_list_bucket_not_found(self):
        with self.assertRaises(ClientError):
            l = [o async for o in awsservicelib.list_objects(self.s3, 'blah')]

    async def test_list_bucket(self):
        expected = [{'Key': 'TestFolder/', 'LastModified': FakeDatetime(2022, 5, 17, 0, 0, tzinfo=tzutc()),
                     'ETag': '"d41d8cd98f00b204e9800998ecf8427e"', 'Size': 0, 'StorageClass': 'STANDARD'},
                    {'Key': 'TestFolder2/', 'LastModified': FakeDatetime(2022, 5, 17, 0, 0, tzinfo=tzutc()),
                     'ETag': '"d41d8cd98f00b204e9800998ecf8427e"', 'Size': 0, 'StorageClass': 'STANDARD'}]
        actual = [o async for o in awsservicelib.list_objects(self.s3, 'arp-scale-2-cloud-bucket-with-tags11')]
        self.assertEqual(expected, actual)

    async def test_list_empty_bucket_with_filter(self):
        expected = [{'Key': 'TestFolder/', 'LastModified': FakeDatetime(2022, 5, 17, 0, 0, tzinfo=tzutc()),
                     'ETag': '"d41d8cd98f00b204e9800998ecf8427e"', 'Size': 0, 'StorageClass': 'STANDARD'},
                    {'Key': 'TestFolder2/', 'LastModified': FakeDatetime(2022, 5, 17, 0, 0, tzinfo=tzutc()),
                     'ETag': '"d41d8cd98f00b204e9800998ecf8427e"', 'Size': 0, 'StorageClass': 'STANDARD'}]
        actual = [o async for o in
                  awsservicelib.list_objects(self.s3, 'arp-scale-2-cloud-bucket-with-tags11', prefix='TestFolder')]
        self.assertEqual(expected, actual)

    async def test_list_empty_bucket_with_filter_one(self):
        expected = [{'Key': 'TestFolder/', 'LastModified': FakeDatetime(2022, 5, 17, 0, 0, tzinfo=tzutc()),
                     'ETag': '"d41d8cd98f00b204e9800998ecf8427e"', 'Size': 0, 'StorageClass': 'STANDARD'}]
        actual = [o async for o in
                  awsservicelib.list_objects(self.s3, 'arp-scale-2-cloud-bucket-with-tags11', prefix='TestFolder/')]
        self.assertEqual(expected, actual)

    async def test_delete_object_status(self):
        actual = await awsservicelib._delete_object(self.s3, bucket_name='arp-scale-2-cloud-bucket-with-tags11',
                                                    key='TestFolder2/', recursive=True)
        self.assertEqual(204, actual.status)

    async def test_delete_object(self):
        await awsservicelib._delete_object(self.s3, bucket_name='arp-scale-2-cloud-bucket-with-tags11',
                                           key='TestFolder2/', recursive=True)
        self.assertFalse(await awsservicelib._object_exists_with_prefix(self.s3,
                                                            'arp-scale-2-cloud-bucket-with-tags11',
                                                            'TestFolder2/'))

    async def test_delete_object_not_found_status(self):
        actual = await awsservicelib._delete_object(self.s3, bucket_name='arp-scale-2-cloud-bucket-with-tags11',
                                                    key='foobar/', recursive=True)
        self.assertEqual(404, actual.status)

    async def test_object_not_found_status(self):
        self.assertFalse(await awsservicelib._object_exists_with_prefix(self.s3, 'arp-scale-2-cloud-bucket-with-tags11', 'foobar/'))

    async def test_delete_object_bucket_not_found(self):
        actual = await awsservicelib._delete_object(self.s3, bucket_name='arp-scale-2-cloud-bucket-with-tags1',
                                                    key='TestFolder2/', recursive=True)
        self.assertEqual(404, actual.status)

    async def test_copy_object_status(self):
        actual = await awsservicelib._copy_object(self.s3, source_bucket_name='arp-scale-2-cloud-bucket-with-tags11',
                                                  source_key='TestFolder2/',
                                                  target_bucket_name='arp-scale-2-cloud-bucket-with-tags11',
                                                  target_key='TestFolder/')
        self.assertEqual(201, actual.status, actual.text)

    async def test_copy_object(self):
        await awsservicelib._copy_object(self.s3, source_bucket_name='arp-scale-2-cloud-bucket-with-tags11',
                                         source_key='TestFolder2/',
                                         target_bucket_name='arp-scale-2-cloud-bucket-with-tags11',
                                         target_key='TestFolder/')
        self.assertTrue(await awsservicelib._object_exists_with_prefix(self.s3, 'arp-scale-2-cloud-bucket-with-tags11',
                                                           'TestFolder/TestFolder2/'))

    async def test_copy_folder_into_itself(self):
        actual = await awsservicelib._copy_object(self.s3, source_bucket_name='arp-scale-2-cloud-bucket-with-tags11',
                                                  source_key='TestFolder/',
                                                  target_bucket_name='arp-scale-2-cloud-bucket-with-tags11',
                                                  target_key='TestFolder/')
        self.assertEqual(400, actual.status, actual.text)

    async def test_copy_object_recursive(self):
        actual = await awsservicelib._copy_object(self.s3, source_bucket_name='arp-scale-2-cloud-bucket-with-tags11',
                                                  source_key='TestFolder2/',
                                                  target_bucket_name='arp-scale-2-cloud-bucket-with-tags11',
                                                  target_key='TestFolder/')
        if actual.status != 201:
            self.fail(f'1: {actual.text}')
        actual = await awsservicelib._copy_object(self.s3, source_bucket_name='arp-scale-2-cloud-bucket-with-tags11',
                                                  source_key='TestFolder/',
                                                  target_bucket_name='arp-scale-2-cloud-bucket-with-tags11',
                                                  target_key='TestFolder2/')
        if actual.status != 201:
            self.fail(f'2: {actual.text}')
        self.assertTrue(await awsservicelib._object_exists_with_prefix(self.s3, 'arp-scale-2-cloud-bucket-with-tags11',
                                                           'TestFolder2/TestFolder/TestFolder2/'))

    async def test_copy_object_to_different_bucket_status(self):
        resp = await awsservicelib._copy_object(self.s3, source_bucket_name='arp-scale-2-cloud-bucket-with-tags11',
                                                source_key='TestFolder2/',
                                                target_bucket_name='arp-scale-2-cloud-bucket-with-tags1',
                                                target_key='')
        self.assertEqual(201, resp.status, resp.text)

    async def test_copy_object_to_different_bucket_at_root(self):
        await awsservicelib._copy_object(self.s3, source_bucket_name='arp-scale-2-cloud-bucket-with-tags11',
                                         source_key='TestFolder2/',
                                         target_bucket_name='arp-scale-2-cloud-bucket-with-tags1',
                                         target_key='')
        self.assertTrue(await awsservicelib._object_exists_with_prefix(self.s3, 'arp-scale-2-cloud-bucket-with-tags1',
                                                           'TestFolder2/'))

    async def test_copy_object_to_different_bucket_at_root2(self):
        await awsservicelib._copy_object(self.s3, source_bucket_name='arp-scale-2-cloud-bucket-with-tags11',
                                         source_key='TestFolder2/',
                                         target_bucket_name='arp-scale-2-cloud-bucket-with-tags1',
                                         target_key=None)
        self.assertTrue(await awsservicelib._object_exists_with_prefix(self.s3, 'arp-scale-2-cloud-bucket-with-tags1',
                                                           'TestFolder2/'))

    async def test_copy_whole_bucket(self):
        await awsservicelib._copy_object(self.s3, source_bucket_name='arp-scale-2-cloud-bucket-with-tags11',
                                         source_key='',
                                         target_bucket_name='arp-scale-2-cloud-bucket-with-tags1',
                                         target_key='')
        self.assertTrue(await awsservicelib._object_exists_with_prefix(self.s3, 'arp-scale-2-cloud-bucket-with-tags1',
                                                           'TestFolder2/'))

    async def test_copy_whole_bucket_none(self):
        await awsservicelib._copy_object(self.s3, source_bucket_name='arp-scale-2-cloud-bucket-with-tags11',
                                         source_key=None,
                                         target_bucket_name='arp-scale-2-cloud-bucket-with-tags1',
                                         target_key=None)
        self.assertTrue(await awsservicelib._object_exists_with_prefix(self.s3, 'arp-scale-2-cloud-bucket-with-tags1',
                                                           'TestFolder2/'))

    async def test_copy_whole_bucket_same_bucket(self):
        actual = await awsservicelib._copy_object(self.s3, source_bucket_name='arp-scale-2-cloud-bucket-with-tags11',
                                                  source_key=None,
                                                  target_bucket_name='arp-scale-2-cloud-bucket-with-tags11',
                                                  target_key=None)
        self.assertEqual(400, actual.status, actual.text)

    async def test_copy_whole_bucket_empty_same_bucket(self):
        actual = await awsservicelib._copy_object(self.s3, source_bucket_name='arp-scale-2-cloud-bucket-with-tags1',
                                                  source_key=None,
                                                  target_bucket_name='arp-scale-2-cloud-bucket-with-tags1',
                                                  target_key=None)
        self.assertEqual(400, actual.status, actual.text)

    async def test_copy_object_not_found_source_bucket(self):
        actual = await awsservicelib._copy_object(self.s3, source_bucket_name='arp-scale-2-cloud-bucket-with-tags1',
                                                  source_key='TestFolder2/',
                                                  target_bucket_name='arp-scale-2-cloud-bucket-with-tags11',
                                                  target_key='foobar/TestFolder3/')
        self.assertEqual(400, actual.status, actual.text)

    async def test_copy_object_not_found_destination_bucket(self):
        actual = await awsservicelib._copy_object(self.s3, source_bucket_name='arp-scale-2-cloud-bucket-with-tags11',
                                                  source_key='TestFolder2/',
                                                  target_bucket_name='arp-scale-2-cloud-bucket-with-tags1',
                                                  target_key='foobar/TestFolder3/')
        self.assertEqual(400, actual.status, actual.text)

    async def test_copy_object_not_found_object(self):
        actual = await awsservicelib._copy_object(self.s3, source_bucket_name='arp-scale-2-cloud-bucket-with-tags11',
                                                  source_key='TestFolder22/',
                                                  target_bucket_name='arp-scale-2-cloud-bucket-with-tags11',
                                                  target_key='foobar/TestFolder3/')
        self.assertEqual(400, actual.status, actual.text)

    async def test_copy_rest_status(self):
        href = f'/volumes/666f6f2d6261722d71757578/buckets/arp-scale-2-cloud-bucket-with-tags11/awss3folders/{encode_key("TestFolder/")}/duplicator'
        body = {'template':
            {'data': [
                {'name': 'target',
                 'value': f'http://localhost:8080/volumes/666f6f2d6261722d71757578/buckets/arp-scale-2-cloud-bucket-with-tags11/awss3folders/{encode_key("TestFolder2/")}'}]}}
        async with self.client.post(href, json=body) as resp:
            self.assertEqual(201, resp.status, await resp.text())

    async def test_copy_rest_header(self):
        href = f'/volumes/666f6f2d6261722d71757578/buckets/arp-scale-2-cloud-bucket-with-tags11/awss3folders/{encode_key("TestFolder/")}/duplicator'
        body = {'template':
            {'data': [
                {'name': 'target',
                 'value': f'http://localhost:8080/volumes/666f6f2d6261722d71757578/buckets/arp-scale-2-cloud-bucket-with-tags11/awss3folders/{encode_key("TestFolder2/")}'}]}}
        async with self.client.post(href, json=body) as resp:
            self.assertEqual(
                f'http://localhost:8080/volumes/666f6f2d6261722d71757578/buckets/arp-scale-2-cloud-bucket-with-tags11/awss3folders/{encode_key("TestFolder2/")}',
                resp.headers.get(hdrs.LOCATION), await resp.text())

    async def test_create_folder_status(self):
        actual = await awsservicelib._create_object(self.s3,
                                                    bucket_name='arp-scale-2-cloud-bucket-with-tags11',
                                                    key='TestFolder2/TestFolder/')
        self.assertEqual(201, actual.status, actual.text)

    async def test_create_folder_bad_bucket_name(self):
        actual = await awsservicelib._create_object(self.s3,
                                                    bucket_name='arp-scale-2-cloud-bucket-with-tags11-bad',
                                                    key='TestFolder2/TestFolder/')
        self.assertEqual(404, actual.status, actual.text)

    async def test_create_folder_no_bucket(self):
        with self.assertRaises(ValueError):
            await awsservicelib._create_object(self.s3,
                                               bucket_name=None,
                                               key='TestFolder2/TestFolder/')

    async def test_create_folder_bucket_empty_string(self):
        actual = await awsservicelib._create_object(self.s3,
                                                    bucket_name='',
                                                    key='TestFolder2/TestFolder/')
        self.assertEqual(400, actual.status, actual.text)

    async def test_create_folder_no_key(self):
        with self.assertRaises(ValueError):
            await awsservicelib._create_object(self.s3,
                                               bucket_name='arp-scale-2-cloud-bucket-with-tags11-bad',
                                               key=None)

    async def test_create_folder_key_empty_string(self):
        actual = await awsservicelib._create_object(self.s3,
                                                    bucket_name='arp-scale-2-cloud-bucket-with-tags11-bad',
                                                    key='')
        self.assertEqual(400, actual.status, actual.text)

    async def test_create_folder_rest_status(self):
        href = f'/volumes/666f6f2d6261722d71757578/buckets/arp-scale-2-cloud-bucket-with-tags11/awss3folders/'
        body = {'bucket_id': 'arp-scale-2-cloud-bucket-with-tags11', 'created': '2022-05-17T00:00:00+00:00',
                'derived_by': None, 'derived_from': [], 'description': None, 'display_name': 'TestFolder',
                'id': 'VGVzdEZvbGRlcjIvVGVzdEZvbGRlci8=', 'invites': [], 'is_folder': True,
                'key': 'TestFolder2/TestFolder/', 'mime_type': 'application/x.folder',
                'modified': '2022-05-17T00:00:00+00:00', 'name': 'VGVzdEZvbGRlcjIvVGVzdEZvbGRlci8=',
                'owner': 'system|none',
                'path': '/arp-scale-2-cloud-bucket-with-tags11/TestFolder2/TestFolder/', 'presigned_url': None,
                's3_uri': 's3://arp-scale-2-cloud-bucket-with-tags11/TestFolder2/TestFolder/', 'shares': [],
                'source': 'AWS S3', 'storage_class': 'STANDARD',
                'type': 'heaobject.folder.AWSS3Folder'}
        async with self.client.post(href, json=body) as resp:
            self.assertEqual(201, resp.status, await resp.text())

    async def test_create_folder_rest_header(self):
        href = f'/volumes/666f6f2d6261722d71757578/buckets/arp-scale-2-cloud-bucket-with-tags11/awss3folders/'
        body = {'bucket_id': 'arp-scale-2-cloud-bucket-with-tags11', 'created': '2022-05-17T00:00:00+00:00',
                'derived_by': None, 'derived_from': [], 'description': None, 'display_name': 'TestFolder',
                'id': 'VGVzdEZvbGRlcjIvVGVzdEZvbGRlci8=', 'invites': [], 'is_folder': True,
                'key': 'TestFolder2/TestFolder/', 'mime_type': 'application/x.folder',
                'modified': '2022-05-17T00:00:00+00:00', 'name': 'VGVzdEZvbGRlcjIvVGVzdEZvbGRlci8=',
                'owner': 'system|none',
                'path': '/arp-scale-2-cloud-bucket-with-tags11/TestFolder2/TestFolder/', 'presigned_url': None,
                's3_uri': 's3://arp-scale-2-cloud-bucket-with-tags11/TestFolder2/TestFolder/', 'shares': [],
                'source': 'AWS S3', 'storage_class': 'STANDARD',
                'type': 'heaobject.folder.AWSS3Folder'}
        async with self.client.post(href, json=body) as resp:
            if resp.status != 201:
                self.fail(await resp.text())
            else:
                self.assertEqual(
                    'http://localhost:8080/volumes/666f6f2d6261722d71757578/buckets/arp-scale-2-cloud-bucket-with-tags11/awss3folders/VGVzdEZvbGRlcjIvVGVzdEZvbGRlci8=',
                    resp.headers[hdrs.LOCATION])
