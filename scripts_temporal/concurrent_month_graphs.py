from pathlib import Path
import re
import requests
import time
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pymongo import MongoClient
from multiprocessing import Pool
import os
import functools

client = MongoClient()
acousticbrainz = client.thesis.acousticbrainz

# Use seaborn style defaults and set the default figure size
sns.set(rc={'figure.figsize':(10, 4)})

mlhd_folder = Path("E:/Datasets/MLHD")
mlhd_demographics_folder = Path("E:/Datasets/MLHD_demographics")

# Regex to only select items from user files that have a MBID
p = re.compile(r'(\w+)\x09(.*)\x09(.*)\x09(.+)')

def find_features(id):
    res = acousticbrainz.find_one({"_id": (id + "-0")})
    if not res:
        return None
    return res

def createMonthGraph(userPath, demographics):
    user_demographics = demographics.loc[demographics['uuid'] == userPath.stem]

    data = {
        "Timestamp": [],
        "Sad": [],
        "Happy": []
    }

    tuples = p.findall(userPath.read_text())

    for t in tuples:
        features = find_features(t[3])
        if features and 'highlevel' in features.keys():
            data['Timestamp'].append(t[0])
            data['Sad'].append(features['highlevel']['mood_sad']['value'])
            data['Happy'].append(features['highlevel']['mood_happy']['value'])

    df = pd.DataFrame(data, columns=['Timestamp', 'Sad', 'Happy'])
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], unit='s')
    df['Month'] = [d.strftime('%b') for d in df.Timestamp]
    df['Year'] = [d.strftime('%Y') for d in df.Timestamp]
    df = df.set_index('Timestamp').sort_index()

    tograph = df.groupby('Month')['Sad'].value_counts(normalize=True).unstack().reindex(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    tograph.plot(kind="bar", stacked='True')
    plt.ylabel("Percentage of listened music")
    try:
        plt.title("UUID: {UUID}\nCountry: {Country}\nAge: {Age}\nGender: {Gender}".format(
            UUID= userPath.stem,
            Country = user_demographics.country.values[0],
            Age = user_demographics.age.values[0],
            Gender = user_demographics.gender.values[0]
        ))
    except:
        plt.title("Data not available")
    plt.legend(['Not sad', 'Sad'], loc=3)
    plt.savefig(userPath.stem + '.png', bbox_inches="tight")
    # plt.show()
    print("Saved {id}".format(id=userPath.stem))

# Load in demographics
csv_demographics = next(mlhd_demographics_folder.glob("**/MLHD_demographics.csv"))
d = pd.read_csv(csv_demographics, delimiter='\t')

# Concurrent loop to speed up processing
users = mlhd_folder.iterdir()

if __name__ == '__main__':
    pool = Pool(os.cpu_count())
    pool.map(functools.partial(createMonthGraph, demographics=d), users)