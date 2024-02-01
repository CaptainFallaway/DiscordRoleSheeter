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
        self.presenter.pull()

    @sync_to_async_wrapper
    async def push(self) -> None:
        self.presenter.push()

    @sync_to_async_wrapper
    async def refresh(self) -> None:
        self.presenter.refresh()

    async def update_timestamp(self) -> None:
        self.ids.status_panel.ids.tim
