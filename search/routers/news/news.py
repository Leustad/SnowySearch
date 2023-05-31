import logging
import os

from fastapi import APIRouter

from search.clients.opensearch import OpensearchClient

router = APIRouter(
    prefix="/news",
    tags=["news"],
    responses={404: {"description": "Not found"}},
)


@router.get("/{index_name}")
async def get_news(index_name: str, query: str, page: int = 0):
    if not query:
        return {"Error": f"No Query: {query}"}, 404

    client = OpensearchClient(
        host=os.getenv("OS_HOST") if os.getenv("OS_HOST") else "opensearch-node1",
        port=os.getenv("OS_PORT") if os.getenv("OS_HOST") else 9200,
    )

    if not client.index_exists(index_name):
        return {"Error": f"index_name: {index_name}"}, 404

    template = {
        "query": {
            "match": {
                "text": {
                    "query": query,
                    "minimum_should_match": 1,
                }
            }
        },
        "size": 5,
        "from": page,
    }

    try:
        return client.search(body=template, index_name=index_name)
    except Exception as e:
        logging.error(f"Index_name: {index_name} | Query: {query} | Error: {e}")
