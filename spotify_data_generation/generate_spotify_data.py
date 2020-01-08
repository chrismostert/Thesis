import pandas as pd
from pathlib import Path
import requests
import base64
import json
import argparse
import time
from tqdm import tqdm

# Get API keys
import config
clientID = config.clientID
clientSecret = config.clientSecret

# String to base64
def getB64(string):
	return base64.b64encode(string.encode('utf-8')).decode('utf-8')

# Get authentication token from spotify server
def getAuth():
	response = requests.post(
		"https://accounts.spotify.com/api/token",
		headers={"Authorization": "Basic {b64}".format(
				b64 = getB64(clientID + ":" + clientSecret)
			)
		},
		data={"grant_type": "client_credentials"}
	)
	if response.status_code == 200:
		print("Authenticated with the spotify API!")
		return response.json()['access_token']
	else:
		raise RuntimeError("Could not authenticate with the spotify server, check your client ID and secret")

# Read a file of newline separated IDs, return chunks of 100 (max per request for spotify)
def read_ids(id_filepath):
	ids = id_filepath.read_text().split('\n')
	res = []

	for i in range(0, len(ids), 100):
		res.append(ids[i:i+100])

	return res

# Get spotify features for list of spotify IDs (max 100)
def get_features(ids, auth):
	assert(len(ids) < 101)

	# Send the request
	response = requests.get(
		"https://api.spotify.com/v1/audio-features",
		headers={"Authorization": "Bearer " + auth},
		params={'ids': ','.join(ids)}
	)

	# Success
	if response.status_code == 200:
		return response.json()

	# Rate limited
	if response.status_code == 429:
		retryafter = response.headers['Retry-After']
		print(" Rate limited, waiting {s} seconds before trying again.".format(
				s = retryafter
			)
		)
		# Retry
		time.sleep(int(retryafter) + 1)
		return get_features(ids, auth)

	# Unknown error
	else:
		raise RuntimeError("Could not fetch chunk {c}".format(c=ids))

# Returns the index of features that could not be fetched from spotify
def get_noneindexes(features):
	res = []
	for index, track in enumerate(features['audio_features']):
		if track is None:
			res.append(index)
	return res

# Main
if __name__ == '__main__':
	# Input arguments
	parser = argparse.ArgumentParser()
	parser.add_argument('ids', help="Path to the file containing spotify IDs to fetch data for (separated by newlines, one ID per line)")
	args = parser.parse_args()

	# Authenticate and read in the ids from the supplied file
	auth = getAuth()
	ids = read_ids(Path(args.ids))

	# Set up progress bar
	pbar = tqdm(ids)
	pbar.set_description("Fetching features from spotify")

	# List of frames
	frames = []
	# List of ids that were not found
	notfound = []

	# For each chunk of ids, fetch the spotify features and add them to the list
	# as a pandas dataframe
	for chunkindex, chunk in enumerate(pbar):
		resp = get_features(chunk, auth)
		nones = get_noneindexes(resp)

		# One of the features could not be found, need to remove it
		if len(nones) > 0:
			for noneindex in nones:
				print(
					" ERROR: Spotify did not give back features for {noneindex}".format(
						noneindex = ids[chunkindex][noneindex]
					)
				)
				# Remove it (and make sure it was actually none, sanity check)
				assert(resp['audio_features'].pop(noneindex) is None)

				# Save it so we know which indexes were not found
				notfound.append(ids[chunkindex][noneindex])

		frames.append(
			pd.DataFrame(
				resp['audio_features'],
				columns=[
					'id', 'duration_ms', 'key', 'mode', 'time_signature', 
					'acousticness', 'danceability', 'energy', 'instrumentalness',
					'liveness', 'loudness', 'speechiness', 'valence', 'tempo'
				]
			)
		)

	print(" Writing to disk...")
	# Write the concatinated dataframe to disk
	pd.concat(frames, ignore_index=True).to_hdf(Path.cwd() / 'spotify.h5', key='data')
	pd.Series(notfound).to_csv(Path.cwd() / 'spotify-notfound.csv', header=False, index=False)
	print(" Done!")