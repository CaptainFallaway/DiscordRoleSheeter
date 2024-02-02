from json import dumps
from aiohttp import ClientSession
from helpers.constants import API_URI, GUILD, HEADERS
from helpers.dataclasses import Member, Role, Resp, ErrorInfo


class DiscordRoleManager:
    def __init__(self) -> None:
        ...

    async def _dc_req(self, method: str, endpoint: str, json_data: dict | None = None) -> Resp:
        async with ClientSession() as session:
            async with session.get(f"{API_URI}{endpoint}", json=json_data, headers=HEADERS) as resp:
                json_data = await resp.json()
                return Resp(ok=resp.ok, status=resp.status, json_data=json_data)

    async def get_roles(self) -> list[Role] | ErrorInfo:
        resp = await self._dc_req("GET", f"/guilds/{GUILD}/roles")

        if resp.ok:
            return [Role(**role) for role in resp.json_data if not role["managed"] and role['name'] != "@everyone"]
        else:
            return ErrorInfo(message=dumps(resp.json_data, indent=4))

    async def get_members(self) -> list[Member] | ErrorInfo:
        resp = await self._dc_req("GET", f"/guilds/{GUILD}/members?limit=1000")

        if resp.ok:
            arr = [Member(**member) for member in resp.json_data]

            # Filter out the bots
            arr = list(
                filter(
                    lambda member: not member.user.bot,
                    arr
                )
            )

            # Sort the members by the ammount of roles they have
            arr = sorted(arr, key=lambda member: len(member.roles))[::-1]

            return arr
        else:
            return ErrorInfo(message=dumps(resp.json_data, indent=4))

    # TODO add more methods for setting the roles to the members of the guild.
    # Lower the ammount of requests to discord api by only changing those who need to be changed.
    # Aka the ones who changed when the last request was made.
    # Either you save the previous response or you fetch again.
