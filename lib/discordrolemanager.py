from aiohttp import ClientSession
from .dataclasses import Member, Role, Resp


class DiscordRoleManager:
    API_URI = "https://discord.com/api/v10"

    TOKEN = "MTE5NzY0NjYwOTA0ODE1ODMzMA.GZVCNG.ps32lXOUnU0WdcEsfzh8ARYfGjvWEeShFwj0kE"

    HEADERS = {
            'authorization': f"Bot {TOKEN}",
            'Content-Type': 'application/json'
        }

    def __init__(self, guild_id: str) -> None:
        self.guild_id = guild_id

    async def _dc_req(self, method: str, endpoint: str, json_data: dict | None = None) -> Resp:
        async with ClientSession() as session:
            async with session.get(f"{self.API_URI}{endpoint}", json=json_data, headers=self.HEADERS) as resp:
                json_data = await resp.json()
                return Resp(ok=resp.ok, status=resp.status, json=json_data)

    async def get_roles(self) -> list[Role]:
        resp = await self._dc_req("GET", f"/guilds/{self.guild_id}/roles")

        if resp.ok:
            return [Role(**role) for role in resp.json if not role["managed"] and role['name'] != "@everyone"]
        else:
            # TODO handle error
            ...

    async def get_members(self) -> list[Member]:
        resp = await self._dc_req("GET", f"/guilds/{self.guild_id}/members?limit=1000")

        if resp.ok:
            return [Member(**member) for member in resp.json]
        else:
            # TODO handle error
            ...

    # TODO add more methods for setting the roles to the members of the guild.
    # Lower the ammount of requests to discord api by only changing those who need to be changed.
    # Aka the ones who changed when the last request was made.
    # Either you save the previous response or you fetch again.
