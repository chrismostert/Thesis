from pathlib import Path
import json
import os
from tqdm import tqdm
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import multiprocessing as mp

# Function that uses the acousticbrainz folder structure to find all submission paths
# for a certain recording id
def get_filepaths(id, dataset):
    folder = dataset / id[0] / id[0:2]
    return folder.glob("**/" + id + "-*.json")

# Returns a pandas dataframe which contains all highlevel features of all submissions
# of a specified MBID from the acousticbrainz dataset
def get_features(id, dataset):
    matches = get_filepaths(id, dataset)
    res = {}
    count = 0

    for match in matches:
        data = json.loads(match.read_text())

        if 'highlevel' in data:
            count += 1
            for feature in featureNames:
                values = data['highlevel'][feature]['all']
                for subfeature in values:
                    try:
                        res[(feature, subfeature)].append(values[subfeature])
                    except:
                        res[(feature, subfeature)] = [values[subfeature]]

    if count > 0:  
        return pd.DataFrame(res, 
            index=pd.MultiIndex.from_tuples([(id, x) for x in range(0, count)]))
    else:
        return pd.DataFrame()

# Writes song features from the acousticbrainz dataset for a specified mbid
# to the defined location.
def write_features(id, loc, dataset):
    df = get_features(id, dataset)
    df.to_pickle(loc / (id + '.pkl'))

# Generates a list of mbids that have already been processed by iterating
# over the ids present in the output folder
def generate_toskip(loc):
    out = set()
    for file in loc.glob('**/*'):
        out.add(file.stem)
    return out

# Define the features we wish to extract from the acousticbrainz data
featureNames = [
    "danceability",
    "gender",
    "genre_dortmund",
    "genre_electronic",
    "genre_rosamerica",
    "genre_tzanetakis",
    "ismir04_rhythm",
    "mood_acoustic",
    "mood_aggressive",
    "mood_electronic",
    "mood_happy",
    "mood_party",
    "mood_relaxed",
    "mood_sad",
    "moods_mirex",
    "timbre",
    "tonal_atonal",
    "voice_instrumental"
]
# Acousticbrainz dataset path
dataset = Path("C:/Users/Chris/Documents/Thesis/datasets/acousticbrainz-highlevel-json-20150130/highlevel")
# Read in file containing MBIDS
mbids = set(json.loads((Path.cwd() / 'counts.json').read_text()).keys())
# Define where to save the results
outPath = Path.cwd() / 'out'
# Check which files are already present in the output path (and thus have already been processed)
mbids = mbids.difference(generate_toskip(outPath))

# Make sure output folder exists on disk
if not outPath.exists():
    os.makedirs(outPath)

# Write all features to the output directory
if __name__ == '__main__':
    with mp.Pool(processes=mp.cpu_count()) as pool:
        pool.starmap(write_features, ((x, outPath, dataset) for x in mbids))





