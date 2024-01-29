from typing import TypeAliasType
from pydantic import BaseModel, model_validator, Field

SnowFlake = TypeAliasType("SnowFlake", str)


class Role(BaseModel):
    """
    Role object

    properties:
        id: SnowFlake (snowflake is a literal string)
        name: str
        color: str (In hexadecimal string format "#RRGGBB")
    """

    id: SnowFlake
    name: str
    color:  str

    @model_validator(mode="before")
    def int_to_hex(cls, values) -> dict:
        values['color'] = f"#{values['color']:06x}"
        return values


class User(BaseModel):
    """
    User object

    properties:
        id: SnowFlake (snowflake is a literal string)
        username: str
        global_name: str | None
        bot: bool

    description:
        global_name -> "the user's display name, if it is set. For bots, this is the application name" -Discord API Docs
    """

    id: SnowFlake
    username: str
    global_name: str | None
    bot: bool = Field(default=False, alias="bot")


class Member(BaseModel):
    """
    Member object

    properties:
        roles: list[SnowFlake] (list of strings)
        user: User
    """

    roles: list[SnowFlake]  # NOTE maybe a list of Role objects?
    user: User
