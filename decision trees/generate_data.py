import pandas as pd
from pathlib import Path

acousticbrainz = pd.read_hdf(Path.cwd() / '..' / 'datasets' / 'acousticbrainzV3.h5')

# Spike in acousticness at 0.09 - 0.10
acoust_spike = acousticbrainz[acousticbrainz[('mood_acoustic', 'acoustic')].between(0.09, 0.10, inclusive=True)]
acoust_rest_low = acousticbrainz[acousticbrainz[('mood_acoustic', 'acoustic')].between(0.00, 0.09, inclusive=False)]
acoust_rest_high = acousticbrainz[acousticbrainz[('mood_acoustic', 'acoustic')].between(0.10, 1.00, inclusive=False)]

acoust_spike['label'] = 'anomaly'
acoust_rest_low['label'] = 'non-anomaly'
acoust_rest_high['label'] = 'non-anomaly'

acoust_anomalies = pd.concat([acoust_spike, acoust_rest_low, acoust_rest_high])
acoust_anomalies = acoust_anomalies[['codec', 'bit_rate', 'essentia_low', 'essentia_git_sha_low', 'essentia_build_sha_low', 'label']]
acoust_anomalies.to_csv('acousticness_anomalies.csv')

# Spike in mood relaxed at 0.805 - 0.815
relaxed_spike = acousticbrainz[acousticbrainz[('mood_relaxed', 'relaxed')].between(0.805, 0.815, inclusive=True)]
relaxed_spike_low = acousticbrainz[acousticbrainz[('mood_relaxed', 'relaxed')].between(0.00, 0.805, inclusive=False)]
relaxed_spike_high = acousticbrainz[acousticbrainz[('mood_relaxed', 'relaxed')].between(0.815, 1.00, inclusive=False)]

relaxed_spike['label'] = 'anomaly'
relaxed_spike_low['label'] = 'non-anomaly'
relaxed_spike_high['label'] = 'non-anomaly'

relaxed_anomalies = pd.concat([relaxed_spike, relaxed_spike_low, relaxed_spike_high])
relaxed_anomalies = relaxed_anomalies[['codec', 'bit_rate', 'essentia_low', 'essentia_git_sha_low', 'essentia_build_sha_low', 'label']]
relaxed_anomalies.to_csv('relaxed_anomalies.csv')

# Spike in mood electronic at 0.972 - 0.982
electronic_spike = acousticbrainz[acousticbrainz[('mood_electronic', 'electronic')].between(0.972, 0.982, inclusive=True)]
electronic_spike_low = acousticbrainz[acousticbrainz[('mood_electronic', 'electronic')].between(0.00, 0.972, inclusive=False)]
electronic_spike_high = acousticbrainz[acousticbrainz[('mood_electronic', 'electronic')].between(0.982, 1.00, inclusive=False)]

electronic_spike['label'] = 'anomaly'
electronic_spike_low['label'] = 'non-anomaly'
electronic_spike_high['label'] = 'non-anomaly'

electronic_anomalies = pd.concat([electronic_spike, electronic_spike_low, electronic_spike_high])
electronic_anomalies = electronic_anomalies[['codec', 'bit_rate', 'essentia_low', 'essentia_git_sha_low', 'essentia_build_sha_low', 'label']]
electronic_anomalies.to_csv('electronic_anomalies.csv')