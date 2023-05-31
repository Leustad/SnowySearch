import logging
from datetime import datetime
from typing import List

import requests
from bs4 import BeautifulSoup
from fastapi import APIRouter, Response, status
from sqlalchemy import desc

from search.clients.opensearch import OpensearchClient
from search.config import running_config
from search.db.db import db_session
from search.db.models import News

# index_name = "hacker_news"
URL = "https://news.ycombinator.com/"

router = APIRouter(
    prefix="/ingest",
    tags=["ingest"],
    responses={404: {"description": "Not found"}},
)


@router.get("/{index_name}", status_code=200)
def index_news(index_name: str, response: Response):
    """
    Index Hacker News data into OpenSearch
    :param response: FastApi Response Obj
    :type index_name: String
    """
    client = OpensearchClient(host=running_config.OS_HOST, port=running_config.OS_PORT)
    try:
        data = _crawl(url=URL)
        _insert_data(data=data)
    except Exception as e:
        logging.error(f"Error: {e}")
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return f"Error: {e}"

    try:
        if data:
            if not client.index_exists(index_name):
                # create index if not exist
                client.create_index(index_name=index_name)
            client.bulk_index(data=data, index_name=index_name)
    except Exception as e:
        logging.error(f"<< Bulk insert Error: {e}")
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            "success": False,
            "operation": "bulk insert",
            "count": len(data),
            "error": e,
        }

    response.status_code = status.HTTP_200_OK
    return {"success": True, "operation": "bulk insert", "count": len(data)}


def _insert_data(data: List):
    """
    Insert Crawl data to DB
    :param data: List of dicts
    :return:
    """
    try:
        session = db_session()
        for item in data:
            _ = News(
                url=item["link"], text=item["text"], article_publish_date=item["age"]
            )
            session.add(_)

        session.commit()
        session.close()
    except Exception as e:
        logging.error(f"<< DB Insert Error: {e}")


def _crawl(url: str):
    """
    Crawl Hacker News
    :return: List of Dicts
    """
    next_page = "?p=2"
    latest_publish_date = _get_last_publish_date()
    response = requests.get(url)
    html_content = response.text
    data = []

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser")

    # Find all entries with class "athing"
    entries = soup.find_all("tr", class_="athing")

    # Iterate over the entries and extract the required information
    for entry in entries:
        # Extract the href value and text associated with the "a" tag within class "titleline"
        titleline = entry.find("span", class_="titleline")
        link = titleline.find("a")
        href = link["href"]
        text = link.text.strip()

        # Find the next "tr" element and extract the value of the "title" attribute within class "age"
        age_element = entry.find_next_sibling("tr").find("span", class_="age")
        age = age_element["title"]

        # Prevent inserting already inserted documents
        if latest_publish_date:
            if latest_publish_date >= datetime.strptime(age, "%Y-%m-%dT%H:%M:%S"):
                break

        # Print the extracted information
        data.append({"link": href, "text": text, "age": age})
    return data


def _get_last_publish_date():
    """
    Get last publish date from DB
    :return: Datetime obj | None
    """
    session = db_session()
    latest_publish_date = (
        session.query(News.article_publish_date)
        .order_by(desc(News.article_publish_date))
        .first()
    )

    # Access the value
    return latest_publish_date[0] if latest_publish_date else None
