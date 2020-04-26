import os
import json
import lib_data

path = "./lib/total"


def readAllFiles(folder_path):
    files = os.listdir(folder_path)

    for file in files:
        f = open(folder_path + "/" + file , "r")
        user_data = f.read()
        f.close()

    return "File Finished"


def userStatsAnalyse(user_data):
    return 0


f = open("./lib/Azer.json", "r")
content = f.read()
print(type(content))
j = json.dumps(content)
list = list(eval(content))
print(type(list))
print(j)







