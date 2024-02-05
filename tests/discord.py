import json
import requests

# NOTE This token has been invalidated
TOKEN = "MTE5NzY0NjYwOTA0ODE1ODMzMA.GZVCNG.ps32lXOUnU0WdcEsfzh8ARYfGjvWEeShFwj0kE"
GUILD = "341280708377051137"

API_URI = "https://discord.com/api/v10"


def pprint(obj):
    print(json.dumps(obj, indent=4))


def dc_req(method, endpoint, json_data: dict | None = None):
    headers = {
        'authorization': f"Bot {TOKEN}",  # Bot {TOKEN}
        'Content-Type': 'application/json'
    }

    return requests.request(method, f"{API_URI}{endpoint}", json=json_data, headers=headers).json()


def print_dc_req(method, endpoint, json_data: dict | None = None):
    text = json.dumps(
        dc_req(method, endpoint, json_data),
        indent=4
        )
    print(text)


def get_roles():
    resp = dc_req("GET", f"/guilds/{GUILD}/roles")
    return [role for role in resp if not role["managed"] and role['name'] != "@everyone"]


# print_dc_req("DELETE", f"/guilds/{GUILD}/members/{659500796307570728}/roles/{1201040561856053318}")

with open("roles.json", "w") as f:
    json.dump(get_roles(), f, indent=4)


with open("members.json", "w") as f:
    json.dump(dc_req("GET", f"/guilds/{GUILD}/members?limit=1000"), f, indent=4)
