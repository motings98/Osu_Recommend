import requests

def getJsonInfo(url):
    request_finished = False
    try_time = 1
    while not request_finished and (try_time <= 10):
        try:
            print("try time : %d" % try_time)
            r = requests.get(url, timeout=15)
            r.raise_for_status()
            request_finished = True
        except Exception as e:
            try_time += 1
            print(e)

    return "s"

url = "http://www.youtube.com"

getJsonInfo(url)