"""
The HEA Server storage Microservice provides ...
"""

from heaserver.service import response
from heaserver.service.runner import init_cmd_line, routes, start, web
from heaserver.service.db import aws, awsservicelib
from heaserver.service.wstl import builder_factory, action
from heaserver.service.appproperty import HEA_DB, HEA_BACKGROUND_TASKS
from heaserver.service.sources import AWS_S3
from heaserver.service.oidcclaimhdrs import SUB
from heaserver.service.customhdrs import PREFER, PREFERENCE_RESPOND_ASYNC
from heaserver.service.util import now
from heaobject.user import NONE_USER, AWS_USER
from heaobject.root import PermissionContext, ViewerPermissionContext, ShareImpl, Permission
from heaobject.storage import AWSStorage
from botocore.exceptions import ClientError
from collections import defaultdict
from datetime import datetime
from dataclasses import dataclass
from typing import Callable, Coroutine, Any
import logging
import asyncio

MONGODB_STORAGE_COLLECTION = 'storage'

_get_storage_lock = asyncio.Lock()

@routes.get('/volumes/{volume_id}/storage')
@routes.get('/volumes/{volume_id}/storage/')
@action(name='heaserver-storage-storage-get-properties', rel='hea-properties')
async def get_all_storage(request: web.Request) -> web.Response:
    """
    Gets all the storage of the volume id that associate with the AWS account.
    :param request: the HTTP request.
    :return: A list of the account's storage or an empty array if there's no any objects data under the AWS account.
    ---
    summary: get all storage for a hea-volume associate with account.
    tags:
        - heaserver-storage-storage-get-account-storage
    parameters:
        - name: volume_id
          in: path
          required: true
          description: The id of the user's AWS volume.
          schema:
            type: string
          examples:
            example:
              summary: A volume id
              value: 666f6f2d6261722d71757578
    responses:
      '200':
        description: Expected response to a valid request.
        content:
            application/json:
                schema:
                    type: array
                    items:
                        type: object
            application/vnd.collection+json:
                schema:
                    type: array
                    items:
                        type: object
            application/vnd.wstl+json:
                schema:
                    type: array
                    items:
                        type: object
    """
    sub = request.headers.get(SUB, NONE_USER)
    async_requested = PREFERENCE_RESPOND_ASYNC in request.headers.get(PREFER, [])
    if async_requested:
        status_location = f'{str(request.url).rstrip("/")}asyncstatus'
        task_name = f'{sub}^{status_location}'
        async with _get_storage_lock:
            if not request.app[HEA_BACKGROUND_TASKS].in_progress(task_name):
                await request.app[HEA_BACKGROUND_TASKS].add(_get_all_storage(request), name=task_name)
        return response.status_see_other(status_location)
    else:
        storage_coro = _get_all_storage(request)
        return await storage_coro(request.app)


@routes.get('/volumes/{volume_id}/storageasyncstatus')
async def get_storage_async_status(request: web.Request) -> web.Response:
    return response.get_async_status(request)


@routes.get('/ping')
async def ping(request: web.Request) -> web.Response:
    """
    For testing whether the service is up.

    :param request: the HTTP request.
    :return: Always returns status code 200.
    """
    return response.status_ok(None)


def main() -> None:
    config = init_cmd_line(description='a service for managing storage and their data within the cloud',
                           default_port=8080)
    start(package_name='heaserver-storage', db=aws.S3Manager, wstl_builder_factory=builder_factory(__package__), config=config)


@dataclass
class _StorageMetadata:
    total_size: int = 0
    object_count: int = 0
    first_modified: datetime | None = None
    last_modified: datetime | None = None


def _get_all_storage(request: web.Request) -> Callable[[web.Application | None], Coroutine[Any, Any, web.Response]]:
    """
    List available storage classes by name

    :param request: the aiohttp Request (required).
    :return: (list) list of available storage classes
    """
    async def coro(app: web.Application | None) -> web.Response:
        logger = logging.getLogger(__name__)
        sub = request.headers.get(SUB, NONE_USER)
        volume_id = request.match_info.get("volume_id", None)
        bucket_id = request.match_info.get('id', None)
        bucket_name = request.match_info.get('bucket_name', None)
        if not volume_id:
            return web.HTTPBadRequest(body="volume_id is required")
        async with aws.S3ClientContext(request, volume_id) as s3_client:
            loop_ = asyncio.get_running_loop()
            try:
                groups: dict[str, _StorageMetadata] = defaultdict(_StorageMetadata)
                coro_list = []
                for bucket in (await loop_.run_in_executor(None, s3_client.list_buckets))['Buckets']:
                    if (bucket_id is None and bucket_name is None) or (bucket['Name'] in (bucket_id, bucket_name)):
                        coro_list.append(_list_objects(s3_client, groups, bucket['Name']))
                        coro_list.append(_list_object_versions(s3_client, groups, bucket['Name']))
                await asyncio.gather(*coro_list)

                storage_class_list = []
                perms = []
                attr_perms = []
                context: PermissionContext[AWSStorage] = ViewerPermissionContext(sub)
                for item_key, item_values in groups.items():
                    storage_class = _get_storage_class(volume_id=volume_id, item_key=item_key, item_values=item_values)
                    storage_class_list.append(storage_class)
                    perms.append(await storage_class.get_permissions(context))
                    attr_perms.append(await storage_class.get_all_attribute_permissions(context))
                return await response.get_all(request, [o.to_dict() for o in storage_class_list],
                                            permissions=perms, attribute_permissions=attr_perms)
            except ClientError as e:
                logging.exception('Error calculating storage classes')
                return response.status_bad_request(str(e))
    return coro


async def _list_objects(s3_client, groups, bucket_name):
    async for obj in awsservicelib.list_objects(s3_client, bucket_name):
        metadata = groups[obj['StorageClass']]
        metadata.object_count += 1
        metadata.total_size += obj['Size']
        metadata.first_modified = obj['LastModified'] if metadata.first_modified is None or obj['LastModified'] < metadata.first_modified else metadata.first_modified
        metadata.last_modified = obj['LastModified'] if metadata.last_modified is None or obj['LastModified'] > metadata.last_modified else metadata.last_modified


async def _list_object_versions(s3_client, groups, bucket_name):
    async for obj in awsservicelib.list_object_versions(s3_client, bucket_name):
        for obj_ in obj.get('Versions', []):
            metadata = groups[obj_['StorageClass']]
            metadata.total_size += obj_['Size']
            metadata.first_modified = obj_['LastModified'] if metadata.first_modified is None or obj_['LastModified'] < metadata.first_modified else metadata.first_modified
            metadata.last_modified = obj_['LastModified'] if metadata.last_modified is None or obj_['LastModified'] > metadata.last_modified else metadata.last_modified
        for obj_ in obj.get('DeleteMarkers', []):
            metadata.first_modified = obj_['LastModified'] if metadata.first_modified is None or obj_['LastModified'] < metadata.first_modified else metadata.first_modified
            metadata.last_modified = obj_['LastModified'] if metadata.last_modified is None or obj_['LastModified'] > metadata.last_modified else metadata.last_modified

def _get_storage_class(volume_id: str, item_key: str, item_values: _StorageMetadata) -> AWSStorage:
    """
    :param item_key: the item_key
    :param item_values:  item_values
    :return: Returns the AWSStorage
    """
    logger = logging.getLogger(__name__)

    assert volume_id is not None, "volume_id is required"
    assert item_key is not None, "item_key is required"
    assert item_values is not None, "item_values is required"

    s = AWSStorage()
    s.name = item_key
    s.id = item_key
    s.display_name = item_key
    s.object_init_modified = item_values.first_modified
    s.object_last_modified = item_values.last_modified
    s.storage_bytes = item_values.total_size
    s.object_count = item_values.object_count
    s.created = now()
    s.modified = now()
    s.volume_id = volume_id
    s.set_storage_class_from_str(item_key)
    s.source = AWS_S3
    s.owner = AWS_USER
    share = ShareImpl()
    share.user = NONE_USER
    share.permissions = [Permission.VIEWER]
    s.shares = [share]
    return s
