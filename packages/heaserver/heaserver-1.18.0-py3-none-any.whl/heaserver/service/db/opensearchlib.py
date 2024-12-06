import logging

from aiohttp import web
from aiohttp.web_request import Request
from aiohttp.web_response import Response
from heaobject.user import NONE_USER
from opensearchpy import AsyncOpenSearch
import re

from heaserver.service import response
from heaserver.service.appproperty import HEA_DB
from heaserver.service.db.database import DatabaseContextManager
from heaserver.service.db.opensearch import OpenSearch, ItemTypeVar, OpenSearchContext
from heaserver.service.oidcclaimhdrs import SUB


def build_query(request: Request, permission_context: dict[str, list[str]]):
    # Placeholder for the must array in the query
    # Handle multiple `regexp` query params
    search_term = request.query.get('text', '')
    santize_search_term = re.escape(search_term)
    regexp_type = request.query.get('regexp_type', 'contains')

    if not search_term:
        raise ValueError("search text is required and cannot be empty")

    # Build the final query object
    if regexp_type == 'contains':
        regex_value = f".*{santize_search_term}.*"
    elif regexp_type == 'starts_with':
        regex_value = f"{santize_search_term}.*"
    elif regexp_type == 'ends_with':
        regex_value = f".*{santize_search_term}"
    else:
        raise ValueError("Invalid query type. Must be one of: 'contains', 'starts_with', 'ends_with'.")

    query = {
        "query": {
            "bool": {
                "must": [
                    {
                        "regexp": {
                            "path": {
                                "value": regex_value
                            }
                        }
                    },
                    {"terms": permission_context}
                ]
            }
        }
    }

    return query


async def search(request: Request,
                 search_item_type: type[ItemTypeVar],
                 perm_context: dict[str, list[str]],
                 index: str | None = None,
                 volume_id: str | None = None) -> Response:
    """
    Executes a dynamic search query in OpenSearch and returns the result.

    :param request: the HTTP request.
    :param search_item_type:
    :param perm_context: The permission context provides list of strings where at least one needs match
    :param index: (Optional) the OpenSearch index name, if not present it will default to db config for it.
    :param volume_id: (Optional) the id of the volume
    :return: The OpenSearch query result or None if no result is found.
    """
    sub = request.headers.get('SUB', 'none_user')
    logger = logging.getLogger(__name__)
    volume_id_ = request.match_info.get('volume_id') if request.match_info.get('volume_id', None) else volume_id

    # Build the query dynamically based on the input parameters
    query = build_query(request, perm_context)
    async with OpenSearchContext(request=request, volume_id=volume_id_) as opensearch:
        results = await opensearch.search(query=query, search_item_type=search_item_type, index=index)
        if not results:
            return response.status_bad_request("Invalid search results")
        logger.debug(f"opensearch result: {results}")
    return await response.get_all(request, [sr.to_dict() for sr in results])

