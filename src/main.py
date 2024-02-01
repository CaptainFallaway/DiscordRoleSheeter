from kivy.app import App
from kivy.lang import Builder
from kivy.config import Config
from kivy.uix.button import Button
from kivy.uix.widget import Widget

import asyncio
from typing import Any, Coroutine
from lib.discordrolemanager import DiscordRoleManager  # Model

GUILD = "341280708377051137"


class RootWidget(Widget):
    """Root widget for the app

    This is a Presenter in the MVP pattern.
    """

    ASPECT_RATIO = 14 / 5  # TODO Imlpement this

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.drm = DiscordRoleManager(GUILD)

    def async_func(func: Coroutine) -> None:
        """Decorator for running async functions in a sync context"""

        def wrapper(instance: Any, *args, **kwargs) -> None:
            loop = asyncio.get_event_loop()
            loop.create_task(func(instance, *args, **kwargs))

        return wrapper

    @async_func
    async def on_btn_press(self, instance: Button) -> None:
        roles = await self.drm.get_roles()
        print(roles)

    @async_func
    async def on_btn_press_2(self, instance: Button) -> None:
        members = await self.drm.get_members()
        print(members)


class MainApp(App):
    def build(self) -> RootWidget:
        self.title = "Discord Role Manager"
        return RootWidget()


if __name__ == '__main__':
    Config.set('graphics', 'width', '700')
    Config.set('graphics', 'height', '250')

    app = MainApp()
    Builder.load_file("kv/main.kv")

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        loop.run_until_complete(app.async_run())
    except KeyboardInterrupt:
        while True:
            try:
                app.stop()
                break
            except KeyboardInterrupt:
                pass

    loop.close()
