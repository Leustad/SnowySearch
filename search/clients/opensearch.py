import logging
import uuid
from typing import List

from opensearchpy import OpenSearch
from opensearchpy.helpers import bulk

news_mappings_path = "../resources/mappings/news.json"


class OpensearchClient:
    def __init__(self, host, port):
        self.client = OpenSearch(
            hosts=[{"host": host, "port": port}],
            http_compress=True,
            use_ssl=False,
            verify_certs=False,
            ssl_assert_hostname=False,
            ssl_show_warn=False,
        )

    def create_index(self, index_name: str = None):
        try:
            if index_name == "news":
                mappings_path = news_mappings_path
            else:
                return

            with open(mappings_path, "r") as mappings_file:
                body = mappings_file.read()

            self.client.indices.create(index_name, body=body)
        except Exception as e:
            logging.error(f"Create Index Error: {e}")
            raise Exception(f"Create Index Error: {e}")

    def index_exists(self, index_name):
        index_exists = self.client.indices.exists(index=index_name)
        if index_exists:
            return True

    def bulk_index(self, data: List, index_name: str):
        try:
            actions = []
            for row in data:
                body = {
                    "_index": index_name,
                    "_id": str(uuid.uuid4()),
                    "_source": {
                        "link": row["link"],
                        "text": row["text"],
                        "age": row["age"],
                    },
                }
                actions.append(body)

            bulk(self.client, actions=actions)
        except Exception as e:
            logging.error(
                f"Error while indexing: index_name: {index_name} | Error: {e}"
            )

    def search(self, body, index_name):
        return self.client.search(body=body, index=index_name)
