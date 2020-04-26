import json
import requests
import lib_data

getuser_api = "/api/get_user"       # 获取用户信息
api_key = "a79d02baf6e68c39d4ff2f7ba24324b8bd360b77"
getuser_params = {"k": "", "u": ""}
getbeatmap_api = "/api/get_beatmaps"

getrecent_api = "/api/get_user_recent"

test = "https://osu.ppy.sh/users/7969090"


def getUserInfo(url):
    print("Getting User Info ...")
    request_url = lib_data.osu_main_url + getuser_api
    user_id = url.split("/", 4)[4]          # 获取玩家主页Url最后数字部分的id
    params = {"k": api_key, "u" : user_id}
    # r = requests.get(request_url, params)           # 申请访问
    # r.raise_for_status()
    # user_info = json.loads(r.text)
    user_info = lib_data.getJsonInfo(request_url,params = params)
    return user_info                        # 返回json的list


def getUserRecent(url):
    print("Getting User Recent ...")
    request_url = lib_data.osu_main_url + getrecent_api
    user_id = url.split("/", 4)[4]         # 获取玩家主页Url最后数字部分的id
    params = {"k": api_key, "u": user_id}
    # r = requests.get(request_url, params)
    # r.raise_for_status()
    # user_recent = json.loads(r.text)
    user_recent = lib_data.getJsonInfo(request_url,params=params)

    return user_recent







