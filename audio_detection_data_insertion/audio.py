import json
from json.decoder import JSONDecodeError
import glob, os
from pprint import pprint
from pymongo import MongoClient
conn = MongoClient('mongodb://jiyea:jiyea@143.248.49.144', 27017)
db = conn.admin
collection = db.feature2

for k in range (3374, 7476) :
    os.chdir("/home/jiyea/data/audio_classes_json/" + "{0:0=5d}".format(k))
#    print(glob.glob("*.json"))
    for j in range (0, len(glob.glob("*.json"))) :
        path = glob.glob("*.json")[j]
        shot_num = path.split("shot")[1].split(".")[0]
        print(shot_num)
        with open(path) as data_file:
            try :
                data = json.load(data_file)
                sound = []
#                print(path)
                if "status" not in data : 
                    continue
                else :
                    if data["status"] != "ok" :
                        continue
                for i in range(0, len(data["predictions"])) :
                    if data["predictions"][i]["probability"] > 0.7:
                        sound.append(data["predictions"][i]["label"])
#                print(sound)
                emp_rec1 = {
                    "shot": shot_num,
                    "audio": sound
                }
                collection.insert_one(emp_rec1)
            except JSONDecodeError :
                pass
