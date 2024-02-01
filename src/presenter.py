from view import View
from models.excelmanager import ExcelManager
from models.discordrolemanager import DiscordRoleManager

from datetime import datetime


class Presenter:
    """Presenter for the app

    This is a Presenter in the MVP pattern.
    """

    def __init__(self):
        self.view = View(self)
        self.drm = DiscordRoleManager()
        self.excelmanager = ExcelManager()

        self.latest_pull_date = None

    async def pull(self) -> None:
        self.latest_pull_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        await self.view.update_timestamp(self.latest_pull_date)

    async def push(self) -> None:
        print("push")

    async def refresh(self) -> None:
        print("refresh")
