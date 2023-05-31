from fastapi import FastAPI

from search.routers import main, sync
from search.routers.news import news
from search.ingest import index_news

app = FastAPI()


app.include_router(main.router)
app.include_router(sync.router)
app.include_router(news.router)
app.include_router(index_news.router)
