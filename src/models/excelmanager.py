from datetime import datetime

from ._excel_writer import ExcelWriter
from ._excel_reader import ExcelReader
from helpers.dataclasses import DiscordMember, DiscordRole, ExcelReadResponse, ErrorInfo


class ExcelManager:
    """
    Manager for the excel file

    This class is a facade for the excel writer and reader.
    """

    def __init__(self, excel_filename: str) -> None:
        self.writer = ExcelWriter(excel_filename)
        self.reader = ExcelReader(excel_filename)

    async def write(self, datetime: datetime, members: list[DiscordMember], roles: list[DiscordRole]) -> bool:
        return self.writer.write(datetime, members, roles)

    async def read(self) -> ExcelReadResponse | ErrorInfo:
        return self.reader.read()
