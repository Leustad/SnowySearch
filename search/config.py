import logging
import os


env = os.getenv("ENVIRONMENT")

logging.info(f"App Started with {env} configs")
print(f"App Started with {env} configs")


class LocalDev:
    POSTGRES_HOST = "search-postgres"
    POSTGRES_PASS = "password"
    POSTGRES_USER = "postgres"
    POSTGRES_PORT = "5432"
    POSTGRES_DB_NAME = "search_db"
    OS_HOST = "opensearch-node1"
    OS_PORT = 9200


class LocalProd:
    POSTGRES_HOST = os.getenv("POSTGRES_HOST", None)
    POSTGRES_PASS = os.getenv("POSTGRES_PASS", None)
    POSTGRES_USER = os.getenv("POSTGRES_USER", None)
    POSTGRES_PORT = os.getenv("POSTGRES_PORT", None)
    POSTGRES_DB_NAME = os.getenv("POSTGRES_DB_NAME", None)
    OS_HOST = os.getenv("OS_HOST", None)
    OS_PORT = os.getenv("OS_POST", 9200)


if env == "local_dev":
    running_config = LocalDev()
