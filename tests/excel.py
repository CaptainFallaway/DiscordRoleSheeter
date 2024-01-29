import json
import xlsxwriter
from pydantic import BaseModel, model_validator, Field
from typing import TypeAliasType

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


workbook = xlsxwriter.Workbook('checkbox_example.xlsm')
worksheet = workbook.add_worksheet("Roles")

workbook.add_vba_project('./bin/togglebtn.bin')
CC_FALSE = {'macro': 'ToggleBtn', 'caption': "—"}
CC_TRUE = {'macro': 'ToggleBtn', 'caption': "✓"}

with open("./tests/samples/roles.json", "r") as f:
    content = json.load(f)
    roles = [Role(**role) for role in content]

with open("./tests/samples/members.json", "r") as f:
    content = json.load(f)
    members = [Member(**member) for member in content]
    members = list(
        filter(
            lambda member: not member.user.bot,
            members
        )
    )

worksheet.write(0, 0, "Name")
for i, role in enumerate(roles):
    _format = workbook.add_format({'bg_color': role.color})
    worksheet.write_string(0, i+1, role.name, _format)

for i, member in enumerate(members):
    worksheet.write_string(i+1, 0, member.user.username)
    for role in roles:
        worksheet.insert_button(i+1, roles.index(role)+1, CC_TRUE if role.id in member.roles else CC_FALSE)

worksheet.autofit()

workbook.close()
