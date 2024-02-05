from datetime import datetime
from typing import TypeAliasType
from pydantic import BaseModel, model_validator, Field

SnowFlake = TypeAliasType("SnowFlake", str)


class DiscordRole(BaseModel):
    """
    Describes a DiscordRole object

    properties:
        id: SnowFlake (snowflake is a literal string)
        name: str
        color: str (In hexadecimal string format "#RRGGBB")
    """

    id: SnowFlake
    name: str
    color: str

    @model_validator(mode="before")
    def int_to_hex(cls, values) -> dict:
        values['color'] = f"#{values['color']:06x}"
        return values


class DiscordUser(BaseModel):
    """
    Describes a DiscordUser object

    properties:
        id: SnowFlake (snowflake is a literal string)
        username: str
        global_name: str | None
        bot: bool
    """

    id: SnowFlake
    username: str
    bot: bool = Field(default=False, alias="bot")


class DiscordMember(BaseModel):
    """
    Describes a DiscordMember object

    properties:
        roles: list[SnowFlake] (list of strings)
        user: User
    """

    roles: list[SnowFlake]
    user: DiscordUser


class DiscordResp(BaseModel):
    """
    Response object

    properties:
        ok: int
        status: int
        json: dict | None

    description:
        ok -> True if status is 200, else False
        status -> HTTP status code
        json -> json response from Discord API. in our case a dict means no no happend.
    """

    ok: bool
    status: int
    json_data: list | dict


class ErrorInfo(BaseModel):
    """
    ErrorInfo object

    properties:
        message: str

    description:
        Some functions may return this to indicate an error.
    """

    message: str


class ExcelMember(BaseModel):
    """
    Describes a member from the excel sheet

    properties:
        user_id: SnowFlake
        roles: list[str]
    """

    user_id: SnowFlake
    roles: list[str]


class MemberChanges(BaseModel):
    """
    Descibes a members changes from the excel sheet

    properties:
        user_id: SnowFlake
        added_roles: list[SnowFlake] = []
        removed_roles: list[SnowFlake] = []
    """

    username: str
    user_id: SnowFlake
    added_roles: list[SnowFlake] = []
    removed_roles: list[SnowFlake] = []


class ExcelReadResponse(BaseModel):
    """
    ExcelReadResponse object

    properties:
        date: datetime
        changes: list[MemberChanges]
    """

    date: datetime
    changes: list[MemberChanges]


class DiscordRateLimitHeaders(BaseModel):
    """
    DiscordRateLimitHeaders object

    properties:
        limit: int
        remaining: int
        reset-after: float

    description:
        This class is used to parse the headers from the Discord API response.

        limit -> The maximum number of requests that can be made in a given time frame
        remaining -> The number of requests remaining in the current time frame
        reset-after -> The number of seconds after which the rate limit resets
    """

    limit: int = Field(alias="x-ratelimit-limit")
    remaining: int = Field(alias="x-ratelimit-remaining")
    reset_after: float = Field(alias="x-ratelimit-reset-after")


class TomlDiscordConfig(BaseModel):
    """
    TomlDiscordConfig object

    properties:
        token: str
        guild: SnowFlake

    description:
        This class is used to parse the configuration file.
    """

    bot_token: str
    guild_id: SnowFlake


class TomlExcelConfig(BaseModel):
    """
    TomlExcelConfig object

    properties:
        export_filename: str

    description:
        This class is used to parse the configuration file.
    """

    export_filename: str


class TomlConfig(BaseModel):
    """
    TomlConfig object

    properties:
        discord: TomlDiscordConfig
        excel: TomlExcelConfig

    description:
        This class is used to parse the configuration file.
    """

    discord: TomlDiscordConfig = Field(alias="Discord")
    excel: TomlExcelConfig = Field(alias="Excel")
