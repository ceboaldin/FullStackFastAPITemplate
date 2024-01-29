import pytest
from httpx import AsyncClient


async def create_group(group_name: str, async_client: AsyncClient) -> dict:
    response = await async_client.post("/group", json={"group_name": group_name})
    return response.json()


@pytest.fixture()
async def created_group(async_client: AsyncClient):
    return await create_group("Group Name One", async_client)


@pytest.mark.anyio
async def test_create_group(async_client: AsyncClient):
    group_name = "Test Group"

    response = await async_client.post("/group", json={"group_name": group_name})

    assert response.status_code == 201
    assert {"id": 1, "group_name": group_name}.items() <= response.json().items()