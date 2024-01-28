import json
import xlsxwriter
from dataclasses import dataclass


@dataclass
class Role:
    id: str
    name: str
    description: str | None
    permissions: str
    position: int
    color: int
    hoist: bool
    managed: bool
    mentionable: bool
    icon: str | None
    unicode_emoji: str | None
    flags: int


workbook = xlsxwriter.Workbook('checkbox_example.xlsm')
worksheet = workbook.add_worksheet("Roles")

workbook.add_vba_project('./bin/togglebtn.bin')
CHECKBOX_CONFIG = {'macro': 'ToggleBtn', 'caption': "—"}

with open("./tests/roles.json", "r") as f:
    content = json.load(f)
    roles = [Role(**role) for role in content]

worksheet.write(0, 0, "Name")
for i, role in enumerate(roles):
    worksheet.write(0, i + 1, role.name)

# for i in range(0, 10):
#     worksheet.insert_button(i, 0, CHECKBOX_CONFIG)  # Add the check button. Either "—" or "✓".

worksheet.autofit()

workbook.close()
