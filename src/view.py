from typing import Protocol
from kivy.uix.widget import Widget
from helpers.async_wrapper import sync_to_async_wrapper


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

    async def show_popup(self, title: str, text: str) -> None:
        # TODO Implement popup for errors and warnings
        ...
