import requests
from bs4 import BeautifulSoup
import re
import json
import lib_data

url = "https://osu.ppy.sh/users/4007897/scores/recent?mode=osu&offset=5&limit=51"

r = requests.get(url)
temp = json.loads(r.text)
content = json.dumps(temp, sort_keys=True, indent=4, separators=(',', ':'))


def writein(haha):
    o = open('new.txt', 'a+', encoding='utf-8')
    o.write(haha)
    return 0

writein(content)





