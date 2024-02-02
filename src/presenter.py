from view import View
from models.excelmanager import ExcelManager
from models.discordrolemanager import DiscordRoleManager
from helpers.dataclasses import ErrorInfo
from helpers.constants import TIME_FORMAT

from datetime import datetime


class Presenter:
    """Presenter for the app

    This is a Presenter in the MVP pattern.
    """

    def __init__(self):
        self.view = View(self)
        self.drm = DiscordRoleManager()
        self.excelmanager = ExcelManager()

    async def pull(self) -> None:
        date = datetime.now()
        await self.view.update_timestamp(date.strftime(TIME_FORMAT))

        roles = await self.drm.get_roles()
        members = await self.drm.get_members()

        if isinstance(roles, ErrorInfo):
            await self.view.show_popup("Discord Error", roles.message)
            return

        if isinstance(members, ErrorInfo):
            await self.view.show_popup("Discord Error", members.message)
            return

        resp = await self.excelmanager.write(date, members, roles)

        if resp is False:
            await self.view.show_popup("Excel Error", "Please close excel file and try again.")
            return

        await self.view.show_popup("Success", "Changes have been pulled and put in the excel file!")
        await self.view.update_changes("No changes")

    async def push(self) -> None:
        resp = await self.excelmanager.read()

        if isinstance(resp, ErrorInfo):
            self.view.update_timestamp("N/A")
            self.view.update_changes("N/A")
            await self.view.show_popup("Excel Error", resp.message)
            return

        approx_time = 0
        for change in resp.changes:
            approx_time += len(change.added_roles) + len(change.removed_roles)
        approx_time += 10

        await self.view.show_popup("Status", f"Applying changes... ~{approx_time} seconds)")

        discord_resp = await self.drm.apply_changes(resp.changes)

        if isinstance(discord_resp, ErrorInfo):
            await self.view.show_popup("Discord Error", discord_resp.message)
            return

        await self.view.show_popup("Success", "Changes have been applied! See discord or pull again.")

    async def refresh(self) -> None:
        resp = await self.excelmanager.read()

        if isinstance(resp, ErrorInfo):
            await self.view.update_timestamp("N/A")
            await self.view.update_changes("N/A")
            await self.view.show_popup("Excel Error", resp.message)
            return

        _str = ""
        for change in resp.changes:
            username = change.username
            added_ammount = len(change.added_roles)
            removed_ammount = len(change.removed_roles)

            crosses = f"[color=00ff00]{added_ammount * '+'}[/color]"
            minuses = f"[color=ff0000]{removed_ammount * '—'}[/color]"
            _str += f"[b]{username}[/b] -> {crosses}{minuses}\n"

        await self.view.update_timestamp(resp.date.strftime(TIME_FORMAT))
        await self.view.update_changes(_str if _str else "No changes")
