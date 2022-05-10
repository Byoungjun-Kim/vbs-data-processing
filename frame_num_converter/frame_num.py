import argparse
import pandas as pd

ap = argparse.ArgumentParser()

ap.add_argument("--shot", type = str, default = "")

args = vars(ap.parse_args())

shot_num = args["shot"]

shot = shot_num.split("_")[1]
shot_num  = shot_num.split("_")[0]
dataset = pd.read_csv("/home/jiyea/ir.nist.gov/V3C1/msb/" + shot_num + ".tsv", delimiter = '\t', header =  0)

frame = dataset["startframe"][int(shot) - 1]
frame = shot_num + "_" + str(frame)

print(frame)
