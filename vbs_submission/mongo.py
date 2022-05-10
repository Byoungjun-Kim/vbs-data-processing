import pymongo
from pymongo import MongoClient
import argparse
import pandas as pd

ap = argparse.ArgumentParser()

ap.add_argument("--color", type = str, default="")
ap.add_argument("--face", type = int, default=-1)
ap.add_argument("--object", type = str, default="")
ap.add_argument("--audio", type = str, default="")


args = vars(ap.parse_args())


conn = MongoClient('mongodb://jiyea:jiyea@143.248.49.144', 27017)
db = conn.admin
color = db.color
face = db.face
obj = db.object
audio = db.audio
#result = db.result

#result.remove({})
'''emp_rec1 = {
        "shot":"2",
        "color": "BLUE",
        "face": "2",
        }
#rec_id1 = collection.insert_one(emp_rec1)
a = "YELLOW"
result = collection.update_many(
    {"shot": "3"},
    {
        "$set": {
            "shot" : "3",
            "color" : "BLUE",
            "texts" : "3",
            "face" : "0"
        }
    },
    upsert = True
)'''
object_list = args["object"].split("-")
audio_list = args["audio"]

cursor_color = color.find({"color" : args["color"]})
cursor_face = face.find({"face" : args["face"]})
cursor_object = obj.find({"object" : object_list})
cursor_audio = audio.find({"audio" : audio_list})

color_shot = []
face_shot = []
object_shot = []
audio_shot = []

for record in cursor_color :
    color_shot.append(record["shot"])
for record in cursor_face :
    face_shot.append(record["shot"])
for record in cursor_object :
    object_shot.append(record["shot"])
for record in cursor_audio :
    audio_shot.append(record["shot"])

c = args["color"] == ""
f = args["face"] == -1
o = args["object"] == ""
a = args["audio"] == ""
if c == True and f == True and o == True and a == True :
    res = []
elif c == True and f == True and o == True and a == False :
    res = audio_shot
elif c == True and f == True and o == False and a == True:
    res = object_shot
elif c == True and f == True and o == False and a == False:
    res = list(set(audio_shot) & set(audio_shot))
elif c == True and f == False and o == True and a == True:
    res = face_shot
elif c == True and f == False and o == True and a == False:
    res = list(set(face_shot) & set(audio_shot))
elif c == True and f == False and o == False and a == True:
    res = list(set(face_shot) & set(object_shot))
elif c == True and f == False and o == False and a == False:
    res = list(set(face_shot) & set(audio_shot) & set(object_shot))
elif c == False and f == True and o == True and a == True:
    res = color_shot
elif c == False and f == True and o == True and a == False:
    res = list(set(color_shot) & set(audio_shot))
elif c == False and f == True and o == False and a == True:
    res = list(set(color_shot) & set(object_shot))
elif c == False and f == True and o == False and a == False:
    res = list(set(color_shot) & set(object_shot) & set(audio_shot))
elif c == False and f == False and o == True and a == True:
    res = list(set(color_shot) & set(face_shot))
elif c == False and f == False and o == True and a == False:
    res = list(set(color_shot) & set(face_shot) & set(audio_shot))
elif c == False and f == False and o == False and a == True:
    res = list(set(color_shot) & set(face_shot) & set(object_shot))
else :
    res = list(set(color_shot) & set(face_shot) & set(object_shot) & set(audio_shot))

res_frame = []
print(res)
for i in range (0, len(res)) :
#    result.insert({"shot" : res[i]})
    shot_num = res[i]
    shot = shot_num.split("_")[1]
    shot_num = shot_num.split("_")[0]
    dataset = pd.read_csv("/home/jiyea/ir.nist.gov/V3C1/msb/" + shot_num + ".tsv", delimiter = '\t', header = 0)
#    print(int(shot))
#    print(len(dataset["startframe"]))
    frame = dataset["startframe"][int(shot)-1]
    frame = shot_num + "_" + str(frame)
    res_frame.append(frame)
#print(res_frame)

while(1) :
    print("Type # of video")
    q = input()
    if q == "q" :
        break
    submit = "http://192.168.0.7:80/vbs/submit?team=3&member=1&video=" + res_frame[int(q)-1].split("_")[0] + "&frame="+res_frame[int(q)-1].split("_")[1]
    print(submit)


