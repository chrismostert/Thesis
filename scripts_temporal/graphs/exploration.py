from pathlib import Path
import re
import requests
import time
import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

## Now only looks at the first submission !!!
def find_features(id, folder):
    index = id[0:2]
    p = folder / index[0] / index / (id + '-0.json')
    if p.exists():
        return json.loads(p.read_text())
    else:
        return None


# Hacky hard coded for demonstration sake
user_id = "0aaec7e6-00b2-4a66-b6aa-94cf6954344f"
user_data_folder = Path("E:/Datasets")
acousticbrainz_folder = Path("E:/Datasets/acousticbrainz-highlevel-json-20150130") / "highlevel"
userFile = user_data_folder / (user_id + ".txt")

# Read in the tab delimited lines
lines = userFile.read_text()
p = re.compile(r'(\w+)\x09(.*)\x09(.*)\x09(.+)')

# Index 0 contains the timestamp, 1 the MBID for the artist, 2 the MBID for the album and 3 the MBID for the recording
tuples = p.findall(lines)

# Statistics
no_logs = len(lines.split('\n'))
no_logs_songid = len(tuples)
print(f"{no_logs_songid} of {no_logs} had a title MBID")

features = [find_features(mbid, acousticbrainz_folder) for mbid in (t[3] for t in tuples)]
no_logs_features = sum((x is not None for x in features))
print(f"Of those songs, {no_logs_features} had AcousticBrainz features")

# Creates a pandas dataframe

# Define data dictionary
data = {
    'User_ID': [],
    'Timestamp': [],
    'MBID': [],
    'Artist': [],
    'Album': [],
    'Title': [],
    'Danceable': [],
    'Acoustic': [],
    'Aggressive': [],
    'Electronic': [],
    'Happy': [],
    'Party': [],
    'Relaxed': [],
    'Sad': []
}

# Populate data dictionary
for i in range(0, len(features)):
    if features[i]:
        # When loading multiple files this should be changed!
        data['User_ID'].append(user_id)

        data['Timestamp'].append(tuples[i][0])
        data['MBID'].append(tuples[i][3])
        if 'artist' in features[i]['metadata']['tags'].keys():
            data['Artist'].append(features[i]['metadata']['tags']['artist'][0])
        elif 'artists' in features[i]['metadata']['tags'].keys():
            data['Artist'].append(features[i]['metadata']['tags']['artists'][0])        
        data['Album'].append(features[i]['metadata']['tags']['album'][0])
        data['Title'].append(features[i]['metadata']['tags']['title'][0])
        data['Danceable'].append(features[i]['highlevel']['danceability']['all']['danceable'])
        data['Acoustic'].append(features[i]['highlevel']['mood_acoustic']['all']['acoustic'])
        data['Aggressive'].append(features[i]['highlevel']['mood_aggressive']['all']['aggressive'])
        data['Electronic'].append(features[i]['highlevel']['mood_electronic']['all']['electronic'])
        data['Happy'].append(features[i]['highlevel']['mood_happy']['all']['happy'])
        data['Party'].append(features[i]['highlevel']['mood_party']['all']['party'])
        data['Relaxed'].append(features[i]['highlevel']['mood_relaxed']['all']['relaxed'])
        data['Sad'].append(features[i]['highlevel']['mood_sad']['all']['sad'])

df = pd.DataFrame(data, columns=['User_ID', 'Timestamp', 'MBID', 'Artist', 'Album', 'Title', 'Danceable',
    'Acoustic', 'Aggressive', 'Electronic', 'Happy', 'Party', 'Relaxed', 'Sad'])
df['Timestamp'] = pd.to_datetime(df['Timestamp'], unit='s')
df.head()

# Make some plots
sns.lmplot(x='Timestamp', y='Happy', data=df, lowess=True)
plt.show()