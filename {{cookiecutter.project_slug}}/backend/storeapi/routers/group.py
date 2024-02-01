import logging
from fastapi import APIRouter
from storeapi.models.group import Group, GroupIn
from storeapi.database import group_table, database


router = APIRouter()
logger = logging.getLogger(__name__)



async def find_group(group_id: int):
    logger.info(f"Finding group with id {group_id}")
    query = group_table.select().where(group_table.c.id == group_id)
    logger.debug(query)
    return await database.fetch_one(query)


@router.post("/group", response_model=Group, status_code=201)
async def create_group(group: GroupIn):
    logger.info("Creating group")
    data = group.model_dump()  # previously .dict()
    query = group_table.insert().values(data)
    logger.debug(query)
    last_record_id = await database.execute(query)
    return {**data, "id": last_record_id}



@router.get("/group", response_model=list[Group])
async def get_all_groups():
    logger.info("Getting all groups")
    query = group_table.select()
    logger.debug(query)
    return await database.fetch_all(query)