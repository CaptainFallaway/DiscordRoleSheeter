import json
import requests


class DiscordRoleManager:
    API_URI = "https://discord.com/api/v10"

    TOKEN = "MTE5NzY0NjYwOTA0ODE1ODMzMA.GZVCNG.ps32lXOUnU0WdcEsfzh8ARYfGjvWEeShFwj0kE"
    GUILD = "341280708377051137"

    HEADERS = {
            'authorization': f"Bot {TOKEN}",
            'Content-Type': 'application/json'
        }

    def __init__(self, guild_id: str) -> None:
        self.guild_id = guild_id

    def _dc_req(self, method: str, endpoint: str, json_data: dict | None = None) -> requests.Response:
        return requests.request(
            method,
            f"{self.API_URI}{endpoint}",
            json=json_data,
            headers=self.HEADERS
        )

    def get_roles(self) -> None:
        ...