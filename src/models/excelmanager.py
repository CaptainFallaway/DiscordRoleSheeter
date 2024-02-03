from datetime import datetime

from ._excel_writer import ExcelWriter
from ._excel_reader import ExcelReader
from helpers.dataclasses import Member, Role, ExcelReadResponse, ErrorInfo


class ExcelManager:
    """
    Manager for the excel file

    This class is a facade for the excel writer and reader.
    """

    def __init__(self) -> None:
        self.writer = ExcelWriter()
        self.reader = ExcelReader()

    async def write(self, datetime: datetime, members: list[Member], roles: list[Role]) -> bool:
        return self.writer.write(datetime, members, roles)

    async def read(self) -> ExcelReadResponse | ErrorInfo:
        return self.reader.read()
