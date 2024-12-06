import asyncio
import configparser
import logging
from abc import ABC
from typing import Optional, TypeVar, List
from aiohttp import web
from aiohttp.web_request import Request
from heaobject.error import DeserializeException
from heaobject.keychain import Credentials
from heaobject.root import HEAObject, HEAObjectDict
from heaobject.volume import OpenSearchFileSystem, FileSystem
from opensearchpy import AsyncOpenSearch

from heaserver.service.appproperty import HEA_DB
from heaserver.service.db.aws import S3, S3Manager
from heaserver.service.db.database import Database, DatabaseContextManager, MicroserviceDatabaseManager, \
    get_file_system_and_credentials_from_volume
from configparser import ConfigParser
from heaobject.folder import Item, AWSS3Item

from heaserver.service.db.mongo import Mongo, MongoManager

CONFIG_SECTION="Opensearch"

ItemTypeVar = TypeVar('ItemTypeVar', bound=Item)

class OpenSearch(Database, ABC):

    def __init__(self, config: Optional[ConfigParser],
                 host: str | None = None,
                 port: int | None = None,
                 use_ssl: bool | None = False,
                 verify_certs: bool | None = False,
                 index: str | None = None,
                 **kwargs):
        """
        Initializes the OpenSearch client and stores configuration parameters.

        :param host: host of opensearch microservice
        :param port: port of opensearch microservice
        :param use_ssl: Whether to use SSL for the connection.
        :param verify_certs: Whether to verify SSL certificates.
        :param index_name: The name of the index to act upon.
        """
        super().__init__(config, **kwargs)
        self.__host = host
        self.__port = port
        self.__use_ssl = use_ssl
        self.__verify_certs = verify_certs
        self.__index = index
        self.__scroll_ids: list[str] = []  # Keep track of scroll IDs

        if config and CONFIG_SECTION in config:
            _section = config[CONFIG_SECTION]
            self.__host = _section.get('Host', fallback=self.__host)
            self.__port = _section.getint( 'Port', fallback=self.__port)
            self.__use_ssl = _section.getboolean('UseSSL', fallback=self.__use_ssl)
            self.__verify_certs = _section.getboolean('VerifyCerts', fallback=self.__verify_certs)
            self.__index = _section.get('Index', fallback=self.__index)

        self.__client = AsyncOpenSearch(
            hosts=[{'host': self.__host, 'port': self.__port}],
            use_ssl=self.__use_ssl,
            verify_certs=self.__verify_certs,
        )

    @property
    def file_system_type(self) -> type[FileSystem]:
        return OpenSearchFileSystem

    async def search(self,query: dict, search_item_type: type[ItemTypeVar],
                     index: str | None = None,
                     scroll_timeout: str = "1m",
                     max_results: int = 1000,
                     page_size: int = 100) -> list[ItemTypeVar]:
        """
        Executes a search query against the specified OpenSearch index and returns a list of items.

        :param query: A dictionary representing the search query to be executed.
        :param search_item_type: The type of item to which the search results should be deserialized.
        :param index: (Optional) The name of the OpenSearch index to search. If not provided, the default index will be used.
        :param scroll_timeout: The duration for which the scroll context will remain open. Default is "1m" (1 minute).
        :param max_results: The maximum number of results to return. The search will stop once this limit is reached.
        :param page_size: The number of results to retrieve in each page (scroll iteration). Default is 100.

        :return: A list of items of type `search_item_type`, deserialized from the search results.

        :raises DeserializeException: Raised if there is an error during deserialization of the response.
        :raises Exception: Raised for any other errors encountered during the search or deserialization.
        """
        logger = logging.getLogger(__name__)
        search_items = []
        total_results = 0  # Track the number of results
        self.__scroll_ids = []
        try:
            resp= await self.__client.search(index=index if index else self.__index, body=query, scroll=scroll_timeout,
                                             size=page_size)
            self.__scroll_ids.append(resp['_scroll_id'])  # Set scroll_id from response
            hits = resp['hits']['hits']

            while hits and total_results < max_results:
                for hit in resp['hits']['hits']:
                    hit_id = hit['_id']
                    if hit['_source']:
                        search_item =  search_item_type()
                        hit['_source']['id'] = hit_id
                        hit['_source']['type'] = search_item.get_type_name()
                        search_item.from_dict(hit['_source'])
                        search_items.append(search_item)
                    if total_results < max_results:
                        resp = await self.__client.scroll(scroll_id=self.__scroll_ids[-1], scroll=scroll_timeout)
                        self.__scroll_ids.append(resp['_scroll_id'])
                        hits = resp['hits']['hits']

        except DeserializeException as de:
            raise de
        except Exception as e:
            raise e
        return search_items

    async def perform_scroll_cleanup(self):
        for scroll_id in self.__scroll_ids:
            try:
                await self.__client.clear_scroll(scroll_id=scroll_id)
            except Exception as clear_exception:
                logging.error(f"Failed to clear scroll with ID {scroll_id}: {clear_exception}")
        self.__scroll_ids = []  # Reset the list after clearing all scrolls

    def close(self):
        if self.__scroll_ids:
            asyncio.create_task(self.perform_scroll_cleanup())



class S3WithOpenSearch(S3, OpenSearch):
    def __init__(self, config: Optional[ConfigParser], **kwargs):
        super().__init__(config, **kwargs)
class MongoWithOpenSearch(Mongo, OpenSearch):
    def __init__(self, config: Optional[ConfigParser], **kwargs):
        super().__init__(config, **kwargs)

class OpenSearchManager(MicroserviceDatabaseManager):

    def __init__(self, config: Optional[configparser.ConfigParser] = None,
                 host: Optional[str] = 'opensearch-node1',
                 port: Optional[int] = 9200,
                 use_ssl: Optional[bool] = False,
                 verify_certs: Optional[bool] = False,
                 index: Optional[str] = 'local_index'):
        super().__init__(config)
        self.config = config
        self.host = host
        self.port = port
        self.use_ssl = use_ssl
        self.verify_certs = verify_certs
        self.index = index


    def get_database(self) -> OpenSearch:
        """
        Initializes and returns an instance of OpenSearchClient with the provided configuration.
        """
        client = OpenSearch(config=self.config, host=self.host, port=self.port, use_ssl=self.use_ssl,
                            verify_certs=self.verify_certs, index=self.index)
        return client

    @classmethod
    def database_types(self) -> list[str]:
        return ['system|opensearch']


class S3WithOpenSearchManager(OpenSearchManager):

    def get_database(self) -> S3WithOpenSearch:
        """
        Initializes and returns an instance of OpenSearchClient with the provided configuration.
        """
        logger = logging.getLogger(__name__)
        logger.debug(f" s3 open search manager host: {self.host} port: {self.port} config: {self.config}")
        client = S3WithOpenSearch(
            config =self.config,
            host=self.host,
            port=self.port,
            use_ssl=self.use_ssl,
            verify_certs=self.verify_certs,
            index=self.index)
        return client


class MongoWithOpenSearchManager(OpenSearchManager):

    def get_database(self) -> MongoWithOpenSearch:
        """
        Initializes and returns an instance of OpenSearchClient with the provided configuration.
        """
        client = MongoWithOpenSearch(
            config =self.config,
            host=self.host,
            port=self.port,
            use_ssl=self.use_ssl,
            verify_certs=self.verify_certs,
            index=self.index)
        return client


class OpenSearchContext(DatabaseContextManager[OpenSearch, Credentials]): # Go into db package?
    """
    Provides a OpenSearch index connection object. If neither a volume nor a credentials object is passed into the
    constructor, the host, port in the microservice's configuration file will be used, it will use defaults of OpenSearch
    filesystem.
    """

    async def connection(self) -> OpenSearch:
        return await _get_opensearch(self.request, self.volume_id)





async def _get_opensearch(request: web.Request, volume_id: Optional[str]) -> OpenSearch:
    """
    Gets a opensearch client.

    :param request: the HTTP request (required).
    :param volume_id: the id string of a volume.
    :return: a OpenSearch client for the file system specified by the volume's file_system_name attribute. If no volume_id
    was provided, the return value will be the "default" OpenSearch client for the microservice found in the HEA_DB
    application-level property.
    :raise ValueError: if there is no volume with the provided volume id, the volume's file system does not exist,
    or a necessary service is not registered.
    """

    if volume_id is not None:
        file_system, credentials = await get_file_system_and_credentials_from_volume(request, volume_id, OpenSearchFileSystem)
        if credentials is None:
            return OpenSearch(None, host=file_system.host, port=file_system.port, index=file_system.index)
        else:
            return OpenSearch(None, host=file_system.host, port=file_system.port, index=file_system.index,
                              username=credentials.account, password=credentials.password)
    else:
        return request.app[HEA_DB]
