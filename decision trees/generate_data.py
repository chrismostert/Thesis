from pathlib import Path
import pandas as pd

# Load in the acousticbrainz dataset into the variable 'acousticbrainz'
acousticbrainz = pd.read_hdf(Path.cwd().parents[0] / 'datasets' / 'acousticbrainzV3.h5')

# Metadata to consider
variables = ['analysis_sample_rate', 'bit_rate', 'codec', 'downmix', 'equal_loudness', 'length', 'lossless',
			'replay_gain', 'essentia_high', 'extractor_high', 'gaia_high', 'essentia_low', 'essentia_git_sha_low',
			'essentia_build_sha_low', 'extractor_low']

## Define the spikes 
# Spike in acousticness at 0.09 - 0.10
acoust_spike = acousticbrainz[acousticbrainz[('mood_acoustic', 'acoustic')].between(0.09, 0.10, inclusive=True)]

# Spike in mood relaxed at 0.805 - 0.815
relaxed_spike = acousticbrainz[acousticbrainz[('mood_relaxed', 'relaxed')].between(0.805, 0.815, inclusive=True)]

# Spike in mood electronic at 0.972 - 0.982
electronic_spike = acousticbrainz[acousticbrainz[('mood_electronic', 'electronic')].between(0.972, 0.982, inclusive=True)]

# Small spike in sad at 0.346 - 0.362
sad_spike = acousticbrainz[acousticbrainz[('mood_sad', 'sad')].between(0.346, 0.362, inclusive=True)]

# Baseline contains all submission not in either of the three spikes
spike_ids = set(acoust_spike.index).union(relaxed_spike.index, electronic_spike.index, sad_spike.index)
nonspike_ids = set(acousticbrainz.index).difference(spike_ids)
baseline = acousticbrainz.loc[list(nonspike_ids)]


## Write datasets
spike_names = ['acoust_spike', 'relaxed_spike', 'electronic_spike', 'sad_spike']
spikes = [acoust_spike, relaxed_spike, electronic_spike, sad_spike]
baseline['label'] = 'non-anomaly'

for i in range(0, len(spikes)):
	print(f"Labeling data for {spike_names[i]}...")
	spike_data = spikes[i][variables].copy(deep=True)
	spike_data['label'] = 'anomaly'
	
	out = spike_data.append(baseline[variables + ['label']])
	out = out.reset_index(drop=True)
	out.to_csv(spike_names[i] + '.csv', index=False)