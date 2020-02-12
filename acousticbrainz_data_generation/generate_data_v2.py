from pathlib import Path
import json
import os
from tqdm import tqdm
import pandas as pd

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

metaFeatureNames = [
    "analysis_sample_rate",
    "bit_rate",
    "codec",
    "downmix",
    "equal_loudness",
    "length",
    "lossless",
    "replay_gain"
]

highVersionFeatures = [
    "essentia",
    "extractor",
    "gaia"
]

lowVersionFeatures = [
    "essentia",
    "extractor"
]

# Acousticbrainz dataset path
dataset = Path("C:/Users/Chris/Documents/Thesis/datasets/acousticbrainz-highlevel-json-20150130/highlevel")
submissions = list(dataset.rglob('*.json'))
res = {}
mbids = []
submissionIDs = []

for submission in tqdm(submissions):
    data = json.loads(submission.read_text())
    stems = submission.stem.split('-')
    mbid = '-'.join(stems[0:-1])
    submissionID = stems[-1]

    if ('highlevel' in data) and ('metadata' in data):
        mbids.append(mbid)
        submissionIDs.append(submissionID)

        for feature in featureNames:
            values = data['highlevel'][feature]['all']
            for subfeature in values:
                try:
                    res[(feature, subfeature)].append(values[subfeature])
                except:
                    res[(feature, subfeature)] = [values[subfeature]]

        for feature in metaFeatureNames:
            value = data['metadata']['audio_properties'][feature]
            try:
                res[feature].append(value)
            except:
                res[feature] = [value]

        for feature in highVersionFeatures:
            value = data['metadata']['version']['highlevel'][feature]
            try:
                res[feature + '_high'].append(value)
            except:
                res[feature + '_high'] = [value]

        for feature in lowVersionFeatures:
            value = data['metadata']['version']['lowlevel'][feature]
            try:
                res[feature + '_low'].append(value)
            except:
                res[feature + '_low'] = [value]

df = pd.DataFrame(res, index=pd.MultiIndex.from_arrays([mbids, submissionIDs]))
df.to_hdf('acousticbrainzV2.h5', key='data')