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
    'font_size': 12,
    'align': 'center',
    'valign': 'center',
    'bottom': 2,
}


workbook = xlsxwriter.Workbook('checkbox_example.xlsm')
worksheet = workbook.add_worksheet("Roles")

workbook.add_vba_project('./bin/togglebtn.bin')

with open("./tests/samples/ers.json", "r") as f:
    content = json.load(f)
    roles = [Role(**role) for role in content]
    # for i in range(2):
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
    for i in range(2):
        members.extend(members)

fmt = workbook.add_format({
    **base_fmt,
    'bg_color': "#EEEAEA",
})

worksheet.write_string(0, 0, "Name", fmt)
for i, role in enumerate(roles):
    _format = workbook.add_format(
        {
            **base_fmt,
            'bg_color': role.color,
            'font_color': get_text_color(role.color),
        }
    )
    worksheet.write_string(0, i+1, role.name, _format)

for i, member in enumerate(members):
    fmt = workbook.add_format()
    if i % 2 == 0:
        fmt.set_bg_color("#EEEAEA")
    else:
        fmt.set_bg_color("#F8F4F4")

    worksheet.write_string(i+1, 0, member.user.username, fmt)
    for j, role in enumerate(roles):
        CC_FALSE = {'macro': 'ToggleBtn', 'caption': "—", 'color': role.color}
        CC_TRUE = {'macro': 'ToggleBtn', 'caption': "✓", 'color': role.color}
        worksheet.insert_button(i+1, j+1, CC_TRUE if role.id in member.roles else CC_FALSE,)

worksheet.autofit()

worksheet = workbook.add_worksheet("Raw Data")

worksheet.write(0, 0, "Name")
for i, role in enumerate(roles):
    worksheet.write_string(0, i+1, role.name)

for i, member in enumerate(members):
    worksheet.write_string(i+1, 0, member.user.username)
    for j, role in enumerate(roles):
        worksheet.write_number(i+1, j+1, 1 if role.id in member.roles else 0)

worksheet.autofit()

workbook.close()
