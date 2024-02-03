from typing import Protocol, Literal
from helpers.constants import POPUP_PATH
from helpers.async_wrapper import sync_to_async_wrapper

from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.lang.builder import Builder


class NotificationPopup(Popup):
    """Custom popup for notifications

    description:
        This is a popup the populates the whole screen with information.
        The seperator color is supposed to invoke what type of information is displayed.
    """

    def __init__(self, title: str, text: str, color: Literal["red"] | Literal["green"] | Literal["yellow"], **kwargs):
        super().__init__(**kwargs)
        self.title = title
        self.ids.warning_content.ids.lbl_text.text = text

        match color:
            case "red":
                self.separator_color = (1, 0, 0, 1)
            case "green":
                self.separator_color = (0, 1, 0, 1)
            case "yellow":
                self.separator_color = (1, 1, 0, 1)


class Presenter(Protocol):
    """Protocol for the presenter class"""

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

    async def update_changes(self, text: str) -> None:
        self.ids.status_panel.ids.scrollable_text_container.ids.lbl_changes.text = text

    async def show_popup(
            self,
            title: str,
            text: str,
            color: Literal["red"] | Literal["green"] | Literal["yellow"]
            ) -> NotificationPopup:
        popup = NotificationPopup(title, text, color)
        popup.open()

        return popup
