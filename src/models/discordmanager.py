from time import time
from json import dumps
from asyncio import sleep
from aiohttp import ClientSession
from helpers.constants import API_URI, DISCORD_MEMBER_LIMIT

from helpers.dataclasses import (
    SnowFlake,
    ErrorInfo,
    DiscordRole,
    DiscordResp,
    DiscordMember,
    MemberChanges,
    DiscordRateLimitHeaders,
)


class DiscordManager:
    def __init__(self, token: str, guild_id: SnowFlake) -> None:
        self.sleep_release_timestamp = 0.0

        self.guild_id = guild_id
        self.headers = {
            'authorization': f"Bot {token}",
            'Content-Type': 'application/json'
        }

    async def _dc_req(self, method: str, endpoint: str, json_data: dict | None = None) -> DiscordResp:
        async with ClientSession() as session:
            if self.sleep_release_timestamp > time():
                await sleep(self.sleep_release_timestamp - time() + 0.5)

            async with session.request(method, f"{API_URI}{endpoint}", json=json_data, headers=self.headers) as resp:
                if not resp.ok:
                    return DiscordResp(ok=resp.ok, status=resp.status, json_data=await resp.json())

                rate_headers = DiscordRateLimitHeaders(**dict(resp.headers))

                if rate_headers.remaining == 0:
                    self.sleep_release_timestamp = time() + rate_headers.reset_after

                if resp.status == 204:  # Since 204 has no content, we return an empty dict
                    return DiscordResp(ok=resp.ok, status=resp.status, json_data={})

                return DiscordResp(ok=resp.ok, status=resp.status, json_data=await resp.json())

    async def get_roles(self) -> list[DiscordRole] | ErrorInfo:
        resp = await self._dc_req("GET", f"/guilds/{self.guild_id}/roles")

        if resp.ok:
            return [
                DiscordRole(**role) for role in resp.json_data if not role["managed"] and role['name'] != "@everyone"
            ]
        else:
            return ErrorInfo(message=dumps(resp.json_data, indent=4) + f"\ncode: {resp.status}")

    async def get_members(self) -> list[DiscordMember] | ErrorInfo:
        after = "0"
        members = []

        while True:
            resp = await self._dc_req(
                "GET",
                f"/guilds/{self.guild_id}/members?limit={DISCORD_MEMBER_LIMIT}&after={after}"
                )

            if resp.ok:
                arr = [DiscordMember(**member) for member in resp.json_data]
                len_members = len(arr)
                last_usr_id = arr[-1].user.id

                members.extend(arr)

                if len_members < DISCORD_MEMBER_LIMIT:
                    break

                after = last_usr_id
            else:
                return ErrorInfo(message=dumps(resp.json_data, indent=4) + f"\ncode: {resp.status}")

        # Filter out the bots and sort the users with the most roles to the top
        members = sorted(
            filter(
                lambda member: not member.user.bot,
                members
            ),
            key=lambda member: len(member.roles),
            reverse=True
        )

        return list(members)

    async def apply_changes(self, changes: list[MemberChanges]) -> None | ErrorInfo:
        for change in changes:
            for role in change.added_roles:
                resp = await self._dc_req("PUT", f"/guilds/{self.guild_id}/members/{change.user_id}/roles/{role}")
                if not resp.ok:
                    return ErrorInfo(message=dumps(resp.json_data, indent=4) + f"\ncode: {resp.status}")

            for role in change.removed_roles:
                resp = await self._dc_req("DELETE", f"/guilds/{self.guild_id}/members/{change.user_id}/roles/{role}")
                if not resp.ok:
                    return ErrorInfo(message=dumps(resp.json_data, indent=4) + f"\ncode: {resp.status}")
