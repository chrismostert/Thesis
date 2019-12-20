from pathlib import Path
from tqdm import tqdm
import os
import json

feature_folder = Path('E:/Datasets/acousticbrainz-highlevel-json-20150130/highlevel')
output_folder = Path.cwd() / 'data' / 'datasets'

data = {}

if not os.path.exists(output_folder):
        os.makedirs(output_folder)


matches = list(feature_folder.glob('**/*-0.json'))

for feature_file in tqdm(matches):
    features = json.loads(feature_file.read_text())
    
    if 'highlevel' in features.keys():
        data[feature_file.stem[0:-2]] = {
            'mood_sad': features['highlevel']['mood_sad']['value'],
            'mood_happy': features['highlevel']['mood_happy']['value']
        }

with open(output_folder / 'mood_features.json', 'w') as outfile:
    json.dump(data, outfile)