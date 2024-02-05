import sys
import asyncio
from os import path
from tomllib import load
from kivy.resources import resource_add_path

from kivy.app import App
from kivy.config import Config
from kivy.core.window import Window

from view import View
from presenter import Presenter
from helpers.dataclasses import TomlConfig
from helpers.constants import WINDOW_SIZE, ICON_PATH, WINDOW_TITLE, TOML_PATH, TOML_CONTENT


class MainApp(App):
    """Main app class"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if path.exists(TOML_PATH):
            with open(TOML_PATH, "rb") as f:
                toml_config = TomlConfig(**load(f))
        else:
            with open(TOML_PATH, "w") as f:
                f.write(TOML_CONTENT)

        print(toml_config)

        self.presenter = Presenter()

        Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
        Config.set('kivy', 'exit_on_escape', '0')

        Window.size = WINDOW_SIZE
        Window.bind(on_resize=lambda *_: Window._set_size(WINDOW_SIZE))  # Static window size

    def build(self) -> View:
        self.icon = ICON_PATH
        self.title = WINDOW_TITLE
        return self.presenter.view


if __name__ == '__main__':
    # Add the resource path for the kivy app
    if hasattr(sys, '_MEIPASS'):
        resource_add_path(path.join(sys._MEIPASS))

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    app = MainApp()

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
