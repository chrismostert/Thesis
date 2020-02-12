from pathlib import Path
import json
from tqdm import tqdm

dataset = Path("C:/Users/Chris/Documents/Thesis/datasets/acousticbrainz-highlevel-json-20150130/highlevel")
recordings = {}

d = list(dataset.glob("**/*.json"))

for entry in tqdm(d):
    id = entry.stem.split('-')
    id = '-'.join(id[:-1])

    try:
        recordings[id] += 1
    except:
        recordings[id] = 1

recordings = {k: v for k,v in sorted(recordings.items(), key=lambda x: x[1], reverse=True)}

with open("counts.json", 'w') as f:
    f.write(json.dumps(recordings))

