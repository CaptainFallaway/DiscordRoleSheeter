import json
import xlsxwriter
from datetime import datetime
from typing import TypeAliasType
from pydantic import BaseModel, model_validator, Field

SnowFlake = TypeAliasType("SnowFlake", str)

# TODO add a new sheet in the workbook for the role id's and a date of the last update.


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


def get_text_color(hex_color):
    # Convert hex color to RGB
    hex_color = hex_color.lstrip('#')
    rgb_color = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    # Calculate relative luminance
    luminance = 0.2126 * rgb_color[0] / 255 + 0.7152 * rgb_color[1] / 255 + 0.0722 * rgb_color[2] / 255

    # Decide text color based on luminance
    if luminance > 0.5:
        return "#000000"
    else:
        return "#FFFFFF"


base_fmt = {
    'bold': True,
    'font_size': 11,
    'align': 'center',
    'valign': 'center',
    'bottom': 1,
    'border_color': "#ABABAB",
}


workbook = xlsxwriter.Workbook('checkbox_example.xlsx')
worksheet = workbook.add_worksheet("Roles")

with open("./tests/samples/ers.json", "r") as f:
    content = json.load(f)
    roles = [Role(**role) for role in content]
    # for _ in range(3):
    #     roles.extend(roles)

with open("./tests/samples/members.json", "r") as f:
    content = json.load(f)
    members = [Member(**member) for member in content]
    members = list(
        filter(
            lambda member: not member.user.bot,
            members
        )
    )
    members = sorted(members, key=lambda member: len(member.roles))[::-1]
    for _ in range(3):
        members.extend(members)

fmt = workbook.add_format({
    **base_fmt,
    'fg_color': "#C2C2C2",
})

worksheet.write_string(0, 0, "Name", fmt)
for i, role in enumerate(roles):
    _format = workbook.add_format(
        {
            **base_fmt,
            'fg_color': role.color,
            'font_color': get_text_color(role.color),
        }
    )
    worksheet.write_string(0, i+1, role.name, _format)

for i, member in enumerate(members):
    fmt = workbook.add_format()
    fg = "#D2D2D2" if i % 2 == 0 else "#C2C2C2"
    fmt.set_fg_color(fg)

    worksheet.write_string(i+1, 0, member.user.username, fmt)
    for j, role in enumerate(roles):
        text = workbook.add_format({
            'align': 'center',
            'valign': 'center',
            'right': 1,
            'left': 1,
            'border_color': "#ABABAB",
            'bold': True,
        })
        text.set_fg_color(fg)
        text.set_font_color(role.color)

        worksheet.write_number(i+1, j+1, int(role.id in member.roles), text)

worksheet.autofit()

worksheet = workbook.add_worksheet("Metadata")

worksheet.write_string(0, 0, datetime.now().isoformat())
for i, role in enumerate(roles):
    worksheet.write_string(0, i+1, role.id)

workbook.close()
