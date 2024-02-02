import xlsxwriter
from datetime import datetime
from helpers.dataclasses import Member, Role
from helpers.constants import EXCEL_FILENAME


class ExcelWriter:
    def __init__(self) -> None:
        self._base_fmt = {
            'bold': True,
            'font_size': 11,
            'align': 'center',
            'valign': 'center',
            'bottom': 1,
            'border_color': "#ABABAB",
        }

        self.workbook = None

    def write(self, date: datetime, members: list[Member], roles: list[Role]) -> bool:
        self.workbook = xlsxwriter.Workbook(EXCEL_FILENAME)

        self._add_roles(members, roles)
        self._add_metadata(date, members, roles)

        try:
            self.workbook.close()
        except xlsxwriter.exceptions.FileCreateError:
            return False

        return True

    def _get_text_color(self, hex_color):
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

    def _get_role_format(self, role_color: str) -> xlsxwriter.workbook.Format:
        return self.workbook.add_format(
            {
                **self._base_fmt,
                'fg_color': role_color,
                'font_color': self._get_text_color(role_color),
            }
        )

    def _get_value_format(self, fg_color: str, role_color: str) -> xlsxwriter.workbook.Format:
        text = self.workbook.add_format({
            'align': 'center',
            'valign': 'center',
            'right': 1,
            'left': 1,
            'border_color': "#ABABAB",
            'bold': True,
        })

        text.set_fg_color(fg_color)
        text.set_font_color(role_color)

        return text

    def _add_roles(self, members: list[Member], roles: list[Role]) -> None:
        worksheet = self.workbook.add_worksheet("Roles")

        fmt = self.workbook.add_format({
            **self._base_fmt,
            'fg_color': "#C2C2C2",
        })

        worksheet.write_string(0, 0, "Name", fmt)

        # Add role names at the top of the sheet (headers)
        for i, role in enumerate(roles):
            role_format = self._get_role_format(role.color)
            worksheet.write_string(0, i+1, role.name, role_format)

        # Add member names and their roles
        for i, member in enumerate(members):
            fg = "#D2D2D2" if i % 2 == 0 else "#C2C2C2"

            fmt = self.workbook.add_format()
            fmt.set_fg_color(fg)

            worksheet.write_string(i+1, 0, member.user.username, fmt)
            for j, role in enumerate(roles):
                value_format = self._get_value_format(fg, role.color)

                worksheet.write_number(i+1, j+1, int(role.id in member.roles), value_format)

        worksheet.autofit()

    def _add_metadata(self, date: datetime, members: list[Member], roles: list[Role]) -> None:
        worksheet = self.workbook.add_worksheet("Metadata")

        worksheet.write_string(0, 0, date.isoformat())

        for i, role in enumerate(roles):
            worksheet.write_string(1, i, role.id)

        for i, member in enumerate(members):
            worksheet.write_string(2, i, member.user.id)
            worksheet.write_string(3, i, member.user.username)
            worksheet.write_string(4, i, "|".join(member.roles))

        worksheet.protect()
