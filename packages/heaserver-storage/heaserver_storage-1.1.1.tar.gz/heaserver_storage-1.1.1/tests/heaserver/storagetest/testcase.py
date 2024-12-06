"""
Creates a test case class for use with the unittest library that is built into Python.
"""
from heaserver.service.testcase.microservicetestcase import get_test_case_cls_default
from heaserver.service.testcase.mockaws import MockS3WithMockMongoManager
from heaserver.storage import service
from heaobject.user import NONE_USER, AWS_USER
from heaobject.data import AWSS3FileObject
from heaserver.service.testcase.expectedvalues import Action
import importlib.resources as pkg_resources
from . import files

db_store = {
    service.MONGODB_STORAGE_COLLECTION: [{
        'id': 'STANDARD',
        'instance_id': 'heaobject.storage.AWSStorage^STANDARD',
        'created': '2022-05-17T00:00:00+00:00',
        'derived_by': None,
        'derived_from': [],
        'description': None,
        'display_name': 'STANDARD',
        'invites': [],
        'modified': '2022-05-17T00:00:00+00:00',
        'name': 'STANDARD',
        'owner': AWS_USER,
        'shares': [{
            'invite': None,
            'permissions': ['VIEWER'],
            'type': 'heaobject.root.ShareImpl',
            'user': 'system|none',
            'type_display_name': 'Share'
        }],
        'source': 'AWS S3',
        'source_detail': None,
        'type': 'heaobject.storage.AWSStorage',
        'arn': None,
        'storage_bytes': 9927038,
        'min_storage_duration': None,
        'object_count': 2,
        'object_init_modified': '2022-05-17T00:00:00+00:00',
        'object_last_modified': '2022-05-17T00:00:00+00:00',
        'volume_id': '666f6f2d6261722d71757578',
        'mime_type': 'application/x.awsstorage',
        'storage_class': 'STANDARD',
        'type_display_name': 'Storage Summary'
    }],
    'buckets': [{
        'id': 'hci-foundation-1',
        'created': '2022-05-17T00:00:00+00:00',
        'derived_by': None,
        'derived_from': [],
        'description': None,
        'object_count': None,
        'size': None,
        'display_name': 'hci-foundation-1',
        'invites': [],
        'modified': None,
        'name': 'hci-foundation-1',
        'owner': NONE_USER,
        'shares': [],
        'source': 'AWS Simple Cloud Storage (S3)',
        'type': 'heaobject.bucket.AWSBucket',
        'version': None,
        'arn': None,
        'versioned': None,
        'encrypted': False,
        'region': 'us-west-1',
        'permission_policy': None,
        'tags': [],
        's3_uri': 's3://hci-foundation-1/',
        'presigned_url': None,
        'locked': False,
        'mime_type': 'application/x.awsbucket',
        'bucket_id': 'hci-foundation-1'
    }],
    'awss3files': [{
        'created': '2022-05-17T00:00:00+00:00',
        'derived_by': None,
        'derived_from': [],
        'description': None,
        'display_name': 'TextFileUTF8.txt',
        'id': 'VGV4dEZpbGVVVEY4LnR4dA==',
        'invites': [],
        'modified': '2022-05-17T00:00:00+00:00',
        'name': 'VGV4dEZpbGVVVEY4LnR4dA==',
        'owner': NONE_USER,
        'shares': [],
        'source': 'AWS Simple Cloud Storage (S3)',
        'storage_class': 'STANDARD',
        'type': AWSS3FileObject.get_type_name(),
        's3_uri': 's3://hci-foundation-1/TextFileUTF8.txt',
        'presigned_url': None,
        'version': None,
        'mime_type': 'text/plain',
        'size': 1253952,
        'human_readable_size': '1.3 MB',
        'bucket_id': 'hci-foundation-1',
        'key': 'TextFileUTF8.txt'
    },
    {
        'created': '2022-05-17T00:00:00+00:00',
        'derived_by': None,
        'derived_from': [],
        'description': None,
        'display_name': 'BinaryFile',
        'id': 'QmluYXJ5RmlsZQ==',
        'invites': [],
        'modified': '2022-05-17T00:00:00+00:00',
        'name': 'QmluYXJ5RmlsZQ==',
        'owner': NONE_USER,
        'shares': [],
        'source': 'AWS Simple Cloud Storage (S3)',
        'storage_class': 'STANDARD',
        'type': AWSS3FileObject.get_type_name(),
        's3_uri': 's3://hci-foundation-1/BinaryFile',
        'presigned_url': None,
        'version': None,
        'mime_type': 'application/octet-stream',
        'size': 8673160,
        'human_readable_size': '8.7 MB',
        'bucket_id': 'hci-foundation-1',
        'key': 'BinaryFile'
    }],
    'filesystems': [{
        'id': '666f6f2d6261722d71757578',
        'created': None,
        'derived_by': None,
        'derived_from': [],
        'description': None,
        'display_name': 'Amazon Web Services',
        'invited': [],
        'modified': None,
        'name': 'amazon_web_services',
        'owner': NONE_USER,
        'shared_with': [],
        'source': None,
        'type': 'heaobject.volume.AWSFileSystem',
        'version': None
    }],
    'volumes': [{
        'id': '666f6f2d6261722d71757578',
        'created': None,
        'derived_by': None,
        'derived_from': [],
        'description': None,
        'display_name': 'My Amazon Web Services',
        'invited': [],
        'modified': None,
        'name': 'amazon_web_services',
        'owner': NONE_USER,
        'shared_with': [],
        'source': None,
        'type': 'heaobject.volume.Volume',
        'version': None,
        'file_system_name': 'amazon_web_services',
        'credential_id': None  # Let boto3 try to find the user's credentials.
    }]}

content = {
    'awss3files': {
        'VGV4dEZpbGVVVEY4LnR4dA==': b'hci-foundation-1|' + pkg_resources.read_text(files, 'TextFileUTF8.txt').encode(
            'utf-8'),
        'QmluYXJ5RmlsZQ==': b'hci-foundation-1|' + pkg_resources.read_binary(files, 'BinaryFile')
    }
}

TestCase = get_test_case_cls_default(coll=service.MONGODB_STORAGE_COLLECTION,
                                     wstl_package=service.__package__,
                                     href='http://localhost:8080/volumes/666f6f2d6261722d71757578/storage/',
                                     fixtures=db_store,
                                     content=content,
                                     db_manager_cls=MockS3WithMockMongoManager,
                                     get_all_actions=[Action(name='heaserver-storage-storage-get-properties',
                                                             rel=['hea-properties'])],
                                     duplicate_action_name=None,
                                     exclude=['body_put', 'body_post'])
