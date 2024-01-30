import asyncio
from typing import Any
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from lib.discordrolemanager import DiscordRoleManager

GUILD = "341280708377051137"


class RootWidget(GridLayout):
    def __init__(self, root_node: 'MainApp', **kwargs):
        super().__init__(**kwargs)

        self.cols = 2

        self.btn1 = Button(text='Roles')
        self.btn1.bind(
            on_press=lambda instance: self.async_wrapper(root_node.on_press_1, instance)
            )
        self.add_widget(self.btn1)

        self.btn2 = Button(text='Members')
        self.btn2.bind(
            on_press=lambda instance: self.async_wrapper(root_node.on_press_2, instance)
            )
        self.add_widget(self.btn2)

    def async_wrapper(self, func, *args, **kwargs):
        loop = asyncio.get_event_loop()
        loop.create_task(func(*args, **kwargs))


class MainApp(App):
    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)

        self.drm = DiscordRoleManager(GUILD)

    def build(self):
        return RootWidget(self)

    async def on_press_1(self, instance):
        roles = await self.drm.get_roles()
        print(roles)

    async def on_press_2(self, instance):
        members = await self.drm.get_members()
        print(members)


if __name__ == '__main__':
    app = MainApp()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(app.async_run())
    loop.close()
