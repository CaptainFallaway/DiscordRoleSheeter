
# App Window Constants

WINDOW_SIZE = (700, 250)
ICON_PATH = "src/assets/icon.ico"
WINDOW_TITLE = "Discord Role Manager - By captainfallaway"


# Discord API Constants

TOKEN = "MTE5NzY0NjYwOTA0ODE1ODMzMA.GZVCNG.ps32lXOUnU0WdcEsfzh8ARYfGjvWEeShFwj0kE"
GUILD = "341280708377051137"

API_URI = "https://discord.com/api/v10"
GATEWAY_URI = "wss://gateway.discord.gg/?v=10&encoding=json"
HEADERS = {
        'authorization': f"Bot {TOKEN}",
        'Content-Type': 'application/json'
    }


# Kivy Lang Path Constants

VIEW_PATH = "src/kv/view.kv"
POPUP_PATH = "src/kv/popup.kv"


# Excel

EXCEL_FILENAME = "roles.xlsx"


# Standard time format

TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
