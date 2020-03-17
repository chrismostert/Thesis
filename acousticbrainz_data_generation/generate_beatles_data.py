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
    "essentia_build_sha",
    "essentia_git_sha",
    "extractor",
    "gaia",
    "gaia_git_sha",
    "models_essentia_git_sha"
]

lowVersionFeatures = [
    "essentia",
    "essentia_build_sha",
    "essentia_git_sha",
    "extractor"
]

tags = [
	"album",
	"artists",
	"artist",
	"title",
	"musicbrainz_albumid"
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
    	tagvalues = data['metadata']['tags']

    	album = None
    	artist = None
    	title = None
    	musicbrainz_albumid = None

    	try:
    		album = tagvalues['album'][0]

    		try:
    			artist = tagvalues['artists'][0]
    		except:
    			try:
    				artist = tagvalues['artist'][0]
    			except:
    				continue

    		title = tagvalues['title'][0]
    		musicbrainz_albumid = tagvalues['musicbrainz_albumid'][0]
    	except:
    		continue

    	if artist == "The Beatles":
	        mbids.append(mbid)
	        submissionIDs.append(submissionID)

	        try:
	            res['album'].append(album)
	        except:
	            res['album'] = [album]

	        try:
	            res['artist'].append(artist)
	        except:
	            res['artist'] = [artist]

	        try:
	            res['title'].append(title)
	        except:
	            res['title'] = [title]

	        try:
	            res['musicbrainz_albumid'].append(musicbrainz_albumid)
	        except:
	            res['musicbrainz_albumid'] = [musicbrainz_albumid]


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
df.to_hdf('beatles.h5', key='data')