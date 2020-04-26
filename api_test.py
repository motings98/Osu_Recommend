import lib_data
import requests
import json_viewer

get_user_api = "/api/get_user"

base_url = "https://osu.ppy.sh/api/v2/"

params = {"k": "a79d02baf6e68c39d4ff2f7ba24324b8bd360b77", "u": "754565"}



url = lib_data.osu_main_url + get_user_api

r = requests.get(url, params)
r.raise_for_status()

print(r.text)
