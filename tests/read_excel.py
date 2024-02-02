import json
import openpyxl
from datetime import datetime
from typing import TypeAliasType
from pydantic import BaseModel, model_validator, Field

SnowFlake = TypeAliasType("SnowFlake", str)


class Role(BaseModel):
    id: SnowFlake
    name: str
    color:  str

    @model_validator(mode="before")
    def int_to_hex(cls, values) -> dict:
        values['color'] = f"#{values['color']:06x}"
        return values


class User(BaseModel):
    id: SnowFlake
    username: str
    global_name: str | None
    bot: bool = Field(default=False, alias="bot")


class Member(BaseModel):
    roles: list[str]  # NOTE maybe a list of Role objects?
    user: User


with open("./tests/samples/ers.json", "r") as f:
    content = json.load(f)
    roles = [Role(**role) for role in content]

workbook = openpyxl.load_workbook("checkbox_example.xlsx")

# Get metadata
metadata_sheet = workbook["Metadata"]

metadata_date = datetime.fromisoformat(metadata_sheet["A1"].value)

metadata_role_ids = [_id[0].value for _id in metadata_sheet.iter_cols(min_col=2)]

print(metadata_role_ids)