# Steam API key
# https://steamcommunity.com/dev/apikey
key = ""

# SteamID
# https://steamid.io/lookup
steamid = "76561198845412957"

#
# 
#

import requests
import json
import time
import os

player_summaries_endpoint = f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={key}&steamids={steamid}"
player_data               = {}

#
#
#

# TODO: better logging
def badappend(line: str):
    with open("player_history.txt", 'a') as player_history_fd:
        player_history_fd.write(
            time.strftime(
                f"%Y-%m-%d %H:%M:%S: {line}\n",
                time.localtime()
            )
        )

if os.path.exists("player_data.txt"):
    with open("player_data.txt", 'r') as fd:
        player_data = json.loads(
            fd.read()
        )

while True:
    player_summaries = requests.get(player_summaries_endpoint).json()

    for key, v in player_summaries["response"]["players"][0].items():
        if player_data.get(key) != v:
            player_data[key] = v

            match key:
                case "avatarhash":
                    badappend(f"a nice new avatar: {v}")
                case "avatar":
                    pass
                case "avatarmedium":
                    pass
                case "avatarfull":
                    avatar        = requests.get(v).content
                    avatar_path   = f"avatars/{ int(time.time()) }.jpg"

                    with open(avatar_path, 'wb') as fd:
                        fd.write(avatar)

                    badappend(f"saved the avatar to {avatar_path}")
                case _:
                    badappend(f"{key} = {v}")

            with open("player_data.txt", 'w') as fd:
                fd.write(
                    json.dumps(player_data)
                )

        # https://steamcommunity.com/comment/Profile/render/76561198845412957/?start=0&&count=1
        # https://stackoverflow.com/questions/47526053/python-parsing-comments-from-steam

    time.sleep(300)