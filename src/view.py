from typing import Protocol
from helpers.constants import POPUP_PATH
from helpers.async_wrapper import sync_to_async_wrapper

from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.lang.builder import Builder


class WarningPopup(Popup):
    def __init__(self, title: str, text: str, **kwargs):
        super().__init__(**kwargs)
        self.title = title
        self.ids.warning_content.ids.lbl_text.text = text


class Presenter(Protocol):
    async def pull(self) -> None:
        ...

    async def push(self) -> None:
        ...

    async def refresh(self) -> None:
        ...


class View(Widget):
    """Root widget for the app view"""

    def __init__(self, presenter: Presenter, **kwargs):
        super().__init__(**kwargs)
        self.presenter = presenter

        Builder.load_file(POPUP_PATH)

    @sync_to_async_wrapper
    async def pull(self) -> None:
        await self.presenter.pull()

    @sync_to_async_wrapper
    async def push(self) -> None:
        await self.presenter.push()

    @sync_to_async_wrapper
    async def refresh(self) -> None:
        await self.presenter.refresh()

    async def update_timestamp(self, text: str) -> None:
        self.ids.status_panel.ids.lbl_timestamp.text = text

    async def update_status(self, text: str) -> None:
        self.ids.status_panel.ids.scrollable_text_container.ids.lbl_status.text = text

    async def show_warning_popup(self, title: str, text: str) -> None:
        popup = WarningPopup(title, text)

        popup.open()
