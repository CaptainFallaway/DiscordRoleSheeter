import sys
import asyncio
from os import path
from pydantic import ValidationError
from tomllib import load, loads, TOMLDecodeError

from kivy.app import App
from kivy.config import Config
from kivy.core.window import Window
from kivy.resources import resource_add_path

from view import View
from presenter import Presenter
from helpers.dataclasses import TomlConfig
from helpers.async_wrapper import sync_to_async_wrapper
from helpers.constants import WINDOW_SIZE, ICON_PATH, WINDOW_TITLE, TOML_FILE, TOML_CONTENT


class MainApp(App):
    """Main app class"""

    toml_config_error: bool = False
    toml_config: TomlConfig = TomlConfig(**loads(TOML_CONTENT))
    _empty_toml_config: TomlConfig = TomlConfig(**loads(TOML_CONTENT))

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        if path.exists(TOML_FILE):
            with open(TOML_FILE, "rb") as f:
                try:
                    self.toml_config = TomlConfig(**load(f))
                except (ValidationError, TOMLDecodeError):
                    self.toml_config_error = True
        else:
            with open(TOML_FILE, "w") as f:
                f.write(TOML_CONTENT)

        self.presenter = Presenter(self.toml_config)

        Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
        Config.set('kivy', 'exit_on_escape', '0')

        Window.size = WINDOW_SIZE
        Window.bind(on_resize=lambda *_: Window._set_size(WINDOW_SIZE))  # Static window size

    @sync_to_async_wrapper
    async def on_start(self) -> None:
        if self.toml_config_error:
            await self.presenter.view.show_popup(
                "Config Error",
                f"Please check [b]'{TOML_FILE}'[/b] for quotation errors, improper values or changed property names."
                + "\n\n(Or just delete the file and restart the application to generate a new one)",
                "red",
                btn_callback=self.stop,
                btn_text="Exit"
            )
        elif self.toml_config is None or self.toml_config == self._empty_toml_config:
            await self.presenter.view.show_popup(
                "Config Info",
                f"Please exit the application and edit [b]'{TOML_FILE}'[/b] to enter your bot token and guild id.",
                "yellow",
                btn_callback=self.stop,
                btn_text="Exit"
            )

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
