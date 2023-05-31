from fastapi import APIRouter

router = APIRouter(
    prefix="/sync",
    tags=["sync"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def sync_data():
    return {"OK": 200}
