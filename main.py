import asyncio
from kivy.app import App
from kivy.uix.button import Button
from lib.discordrolemanager import DiscordRoleManager

GUILD = "341280708377051137"


class MainApp(App):
    async def build(self):
        # return a Button() as a root widget
        return Button(text='hello world')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(MainApp().async_run())
    # x = DiscordRoleManager(GUILD)
    # print(x.get_roles())
