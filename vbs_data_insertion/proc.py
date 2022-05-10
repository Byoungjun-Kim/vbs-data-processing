import pymongo
from pymongo import MongoClient
import pandas as pd
conn = MongoClient('mongodb://jiyea:jiyea@143.248.49.144', 27017)
db = conn.admin
collection = db.feature2
#import numpy as np
'''shotnum, colorlabel, faces, text'''
color = ["BLACKWHITE", "BLUE", "CYAN", "GRAY", "GREEN", "MAGENTA", "ORANGE", "RED", "UNDETERMINED", "VIOLET", "YELLOW"]
faces = ["nofaces","1face","2faces","3faces","4faces","manyfaces"]
texts = ["fewtext", "muchtext"]
def shot_col(content, color_name) :
    for i in range(0, len(content)):
        shot_num = content[i].split("\n")[0]
#        result = collection.update_many(
#            {"shot": shot_num},
#            {
#                "$set": {
#                    "shot" : shot_num,
#                    "color": color_name,
#                }
#            },
#            upsert=True
#        )
        ent = {"shot" : shot_num, "color" : color_name}
        collection.insert_one(ent)

def shot_face(content, face_num) :
    for i in range(1, len(content)):
        shot_num = content[i].split("/")[1].split("\n")[0]
        frame = shot_num.split("_")[1]
        shot_num = shot_num.split("_")[0]
#        print(shot_num)
#        print(frame)
        dataset = pd.read_csv("/home/jiyea/ir.nist.gov/V3C1/msb/" + shot_num + ".tsv", delimiter = '\t', header = 0)
        cnt = 1
        for j in range (0, len(dataset["startframe"]) - 1) :
             if dataset["startframe"][j] < int(frame) and dataset["startframe"][j+1] > int(frame) : 
                 break
             cnt = cnt + 1
        shot_num = shot_num + "_" + str(cnt)
#        result = collection.update_many(
#            {"shot": shot_num},
#            {
#                "$set": {
#                    "shot": shot_num,
#                    "face": face_num
#                }
#            },
#            upsert=True
#        )'''
        ent = {"shot" : shot_num, "face" : face_num}
        collection.insert_one(ent)

def shot_text(content, texts) :
    for i in range(1, len(content)):
        shot_num = content[i].split("/")[1]
        frame = shot_num.split("_")[1]
        shot_num = shot_num.split("_")[0]
        dataset = pd.read_csv("/home/jiyea/ir.nist.gov/V3C1/msb/" + shot_num + ".tsv", delimiter = '\t', header = 0)
        cnt = 1
        for j in range (0, len(dataset["startframe"]) - 1) :
            if dataset["startframe"][j] < int(frame) and dataset["startframe"][j+1] > int(frame) :
                break
            cnt = cnt + 1
        shot_num = shot_num + "_" + str(cnt)
#        result = collection.update_many(
#            {"shot": shot_num},
#            {
#                "$set": {
#                    "shot": shot_num,
#                    "texts": texts
#                }
#            },
#            upsert=True
#        )'''
        ent = {"shot" : shot_num, "texts" : texts}
        collection.insert_one(ent)

print("start")
#for i in range (0, 11) :
#    print(i)
#    file_name = color[i] + ".txt"
#    with open(file_name) as f:
#        content = f.readlines()
#    shot_col(content, color[i])
#print("shot color complete")


for i in range (1, 6) :
    print(i)
    file_name = faces[i] + ".txt"
    with open(file_name) as f:
        content = f.readlines()
    shot_face(content, i)
print("shot face complete")
for i in range (0, 2) :
    print(i)
    file_name = texts[i] + ".txt"
    with open(file_name) as f:
        content = f.readlines()
    shot_text(content, texts[i])
print("shot text complete")
#f = open("output.txt", 'w')
#for i in range(0, len(shots)):
#    data = str(shots[i][0]) + " " + str(shots[i][1]) + " " + str(shots[i][2]) + " " + str(shots[i][3]) + "\n"
#    f.write(data)
#f.close()


