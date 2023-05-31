from fastapi import APIRouter

router = APIRouter(
    prefix="/main",
    tags=["main"],
    responses={404: {"description": "Not found"}},
)


@router.get("")
async def main(index_name: str, title: str):
    return {"OK": 200}
