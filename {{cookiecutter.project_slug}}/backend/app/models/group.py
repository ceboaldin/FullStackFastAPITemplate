from pydantic import BaseModel, ConfigDict


class GroupIn(BaseModel):
    group_name: str


class Group(GroupIn):
    model_config = ConfigDict(from_attributes=True)
    id: int


