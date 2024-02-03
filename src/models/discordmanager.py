from time import time
from json import dumps
from asyncio import sleep
from aiohttp import ClientSession
from helpers.constants import API_URI, GUILD, HEADERS

from helpers.dataclasses import (
    ErrorInfo,
    DiscordRole,
    DiscordResp,
    DiscordMember,
    MemberChanges,
    DiscordRateLimitHeaders
)


class DiscordManager:
    def __init__(self) -> None:
        self.sleep_release_timestamp = 0.0

    async def _dc_req(self, method: str, endpoint: str, json_data: dict | None = None) -> DiscordResp:
        async with ClientSession() as session:
            if self.sleep_release_timestamp > time():
                await sleep(self.sleep_release_timestamp - time() + 0.5)

            async with session.request(method, f"{API_URI}{endpoint}", json=json_data, headers=HEADERS) as resp:
                rate_headers = DiscordRateLimitHeaders(**dict(resp.headers))

                if rate_headers.remaining == 0:
                    self.sleep_release_timestamp = time() + rate_headers.reset_after

                if resp.status == 204:  # Since 204 has no content, we return an empty dict
                    return DiscordResp(ok=True, status=204, json_data={})

                return DiscordResp(ok=resp.ok, status=resp.status, json_data=await resp.json())

    async def get_roles(self) -> list[DiscordRole] | ErrorInfo:
        resp = await self._dc_req("GET", f"/guilds/{GUILD}/roles")

        if resp.ok:
            return [
                DiscordRole(**role) for role in resp.json_data if not role["managed"] and role['name'] != "@everyone"
            ]
        else:
            return ErrorInfo(message=dumps(resp.json_data, indent=4))

    async def get_members(self) -> list[DiscordMember] | ErrorInfo:
        # NOTE the limit is 1000, if the server has more than 1000 members, we need to implement pagination
        resp = await self._dc_req("GET", f"/guilds/{GUILD}/members?limit=1000")

        if resp.ok:
            arr = [DiscordMember(**member) for member in resp.json_data]

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

    async def apply_changes(self, changes: list[MemberChanges]) -> None | ErrorInfo:
        for change in changes:
            for role in change.added_roles:
                resp = await self._dc_req("PUT", f"/guilds/{GUILD}/members/{change.user_id}/roles/{role}")
                if not resp.ok:
                    return ErrorInfo(message=dumps(resp.json_data, indent=4) + f"\ncode: {resp.status}")

            for role in change.removed_roles:
                resp = await self._dc_req("DELETE", f"/guilds/{GUILD}/members/{change.user_id}/roles/{role}")
                if not resp.ok:
                    return ErrorInfo(message=dumps(resp.json_data, indent=4) + f"\ncode: {resp.status}")
