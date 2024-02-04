import asyncio
from datetime import datetime

from view import View
from helpers.dataclasses import ErrorInfo
from models.excelmanager import ExcelManager
from models.discordmanager import DiscordManager
from helpers.constants import TIME_FORMAT, EXCEL_FILENAME


class Presenter:
    """
    Presenter for the app

    This is the Presenter in the MVP pattern.
    """

    def __init__(self):
        # Instentiate the view of the app, main.py will use this to build the app
        self.view = View(self)

        # Instentiate the models
        self.drm = DiscordManager()
        self.excelmanager = ExcelManager()

        # A flag to see what changes have been refreshed and put in to the view
        self.refreshed_changes = []

        # Auto refresh on startup
        loop = asyncio.get_event_loop()
        loop.create_task(self.refresh(ignore_error=True))

    async def pull(self) -> None:
        date = datetime.now()

        status_popup = await self.view.show_popup("Status", "Pulling members and roles from discord...", "yellow")

        roles = await self.drm.get_roles()
        members = await self.drm.get_members()

        if isinstance(roles, ErrorInfo):
            status_popup.dismiss()
            await self.view.show_popup("Discord Error", roles.message, "red")
            return

        if isinstance(members, ErrorInfo):
            status_popup.dismiss()
            await self.view.show_popup("Discord Error", members.message, "red")
            return

        resp = await self.excelmanager.write(date, members, roles)

        if resp is False:
            status_popup.dismiss()
            await self.view.show_popup("Excel Error", "Please [b]close excel[/b] file and try again.", "red")
            return

        status_popup.dismiss()
        self.refreshed_changes = []  # Reset the changes since we have a new excel file
        await self.view.update_changes("No changes")
        await self.view.update_timestamp(date.strftime(TIME_FORMAT))
        await self.view.show_popup(
            "Success", f"Changes have been pulled and put in '[b]{EXCEL_FILENAME}[/b]' !", "green"
            )

    async def push(self) -> None:
        resp = await self.excelmanager.read()

        if isinstance(resp, ErrorInfo):
            await self.view.update_timestamp("N/A")
            await self.view.update_changes("N/A")
            await self.view.show_popup("Excel Error", resp.message, "red")
            return

        if not resp.changes:
            await self.view.show_popup("No changes", "No changes to apply.", "yellow")
            return

        if self.refreshed_changes != resp.changes:
            await self.view.show_popup("Warning", "Please [b]refresh[/b] to review changes first.", "yellow")
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

        if resp.changes:
            self.refreshed_changes = resp.changes

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
