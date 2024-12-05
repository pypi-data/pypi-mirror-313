#!/usr/bin/env python3
from heaobject.registry import Resource

from heaserver.storage import service
from heaserver.service.wstl import builder_factory
from heaserver.service.testcase.awsdockermongo import S3WithDockerMongoManager
from heaserver.service.testcase import swaggerui
from heaserver.service.testcase.dockermongo import DockerMongoManager
from integrationtests.heaserver.storageintegrationtest.testcase import db_store
from aiohttp.web import get
from heaserver.service.testcase.docker import MicroserviceContainerConfig
import logging
from heaobject.volume import DEFAULT_FILE_SYSTEM

logging.basicConfig(level=logging.DEBUG)


HEASERVER_REGISTRY_IMAGE = 'registry.gitlab.com/huntsman-cancer-institute/risr/hea/heaserver-registry:1.0.0'
HEASERVER_VOLUMES_IMAGE = 'registry.gitlab.com/huntsman-cancer-institute/risr/hea/heaserver-volumes:1.0.0'
HEASERVER_KEYCHAIN_IMAGE = 'registry.gitlab.com/huntsman-cancer-institute/risr/hea/heaserver-keychain:1.0.0'


if __name__ == '__main__':
    volume_microservice = MicroserviceContainerConfig(
        image=HEASERVER_VOLUMES_IMAGE,
        port=8080, check_path='/volumes',
        resources=[Resource(resource_type_name='heaobject.volume.Volume',
                            base_path='volumes',
                            file_system_name=DEFAULT_FILE_SYSTEM),
                   Resource(resource_type_name='heaobject.volume.FileSystem',
                            base_path='filesystems',
                            file_system_name=DEFAULT_FILE_SYSTEM)],
        db_manager_cls=DockerMongoManager)
    keychain_microservice = MicroserviceContainerConfig(
        image=HEASERVER_KEYCHAIN_IMAGE,
        port=8080, check_path='/credentials',
        resources=[Resource(resource_type_name='heaobject.keychain.Credentials',
                            base_path='credentials',
                            file_system_name=DEFAULT_FILE_SYSTEM)],
        db_manager_cls=DockerMongoManager)
    swaggerui.run(project_slug='heaserver-storage', desktop_objects=db_store,
                  wstl_builder_factory=builder_factory(service.__package__),
                  routes=[
                      (get, '/volumes/{volume_id}/storage', service.get_all_storage),
                      # (get, '/volumes/{volume_id}/buckets/byname/{bucket_name}/storage', service.get_bucket_storage)
                  ],
                  registry_docker_image=HEASERVER_REGISTRY_IMAGE,
                  other_docker_images=[keychain_microservice, volume_microservice],
                  db_manager_cls=S3WithDockerMongoManager)
