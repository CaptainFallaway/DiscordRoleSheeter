import asyncio
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

        # Auto refresh on startup
        loop = asyncio.get_event_loop()
        loop.create_task(self.refresh(ignore_error=True))

    async def pull(self) -> None:
        date = datetime.now()

        roles = await self.drm.get_roles()
        members = await self.drm.get_members()

        if isinstance(roles, ErrorInfo):
            await self.view.show_popup("Discord Error", roles.message, "red")
            return

        if isinstance(members, ErrorInfo):
            await self.view.show_popup("Discord Error", members.message, "red")
            return

        resp = await self.excelmanager.write(date, members, roles)

        if resp is False:
            await self.view.show_popup("Excel Error", "Please close excel file and try again.", "red")
            return

        await self.view.update_changes("No changes")
        await self.view.update_timestamp(date.strftime(TIME_FORMAT))
        await self.view.show_popup("Success", "Changes have been pulled and put in the excel file!", "green")

    async def push(self) -> None:
        resp = await self.excelmanager.read()

        if isinstance(resp, ErrorInfo):
            self.view.update_timestamp("N/A")
            self.view.update_changes("N/A")
            await self.view.show_popup("Excel Error", resp.message, False)
            return

        if not resp.changes:
            await self.view.show_popup("No changes", "No changes to apply.", "yellow")
            return

        approx_time = 0
        for change in resp.changes:
            approx_time += len(change.added_roles) + len(change.removed_roles)

        if approx_time > 10:
            approx_time += 10

        status_popup = await self.view.show_popup(
            "Status", f"Applying changes... (Approx ±{approx_time} seconds)", "yellow"
            )

        discord_resp = await self.drm.apply_changes(resp.changes)

        if isinstance(discord_resp, ErrorInfo):
            status_popup.dismiss()
            await self.view.show_popup("Discord Error", discord_resp.message, "red")
            return

        status_popup.dismiss()
        await self.view.show_popup("Success", "Changes have been applied! See discord or pull again.", "green")

    async def refresh(self, ignore_error: bool = False) -> None:
        resp = await self.excelmanager.read()

        if isinstance(resp, ErrorInfo):
            await self.view.update_timestamp("N/A")
            await self.view.update_changes("N/A")
            await self.view.show_popup("Excel Error", resp.message, "red") if not ignore_error else None
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
