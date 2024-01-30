import json  # noqa E402
from .dataclasses import Member, Role, User  # noqa E402
from aiohttp import ClientSession, ClientResponse


class DiscordRoleManager:
    API_URI = "https://discord.com/api/v10"

    TOKEN = "MTE5NzY0NjYwOTA0ODE1ODMzMA.GZVCNG.ps32lXOUnU0WdcEsfzh8ARYfGjvWEeShFwj0kE"

    HEADERS = {
            'authorization': f"Bot {TOKEN}",
            'Content-Type': 'application/json'
        }

    def __init__(self, guild_id: str) -> None:
        self.guild_id = guild_id

    async def _dc_req(self, method: str, endpoint: str, json_data: dict | None = None) -> ClientResponse:
        async with ClientSession() as session:
            async with session.get(f"{self.API_URI}{endpoint}", json=json_data, headers=self.HEADERS) as resp:
                return resp

        # return requests.request(
        #     method,
        #     f"{self.API_URI}{endpoint}",
        #     json=json_data,
        #     headers=self.HEADERS
        # )

    async def get_roles(self) -> list[Role]:
        resp = await self._dc_req("GET", f"/guilds/{self.guild_id}/roles")

        if resp.ok:
            return [Role(**role) for role in resp.json() if not role["managed"] and role['name'] != "@everyone"]
        else:
            # TODO handle error
            ...

    async def get_members(self) -> list[Member]:
        resp = await self._dc_req("GET", f"/guilds/{self.guild_id}/members?limit=1000")
        print(json.dumps(resp.json(), indent=4))

        if resp.ok:
            return [Member(**member) for member in resp.json()]
        else:
            # TODO handle error
            ...
