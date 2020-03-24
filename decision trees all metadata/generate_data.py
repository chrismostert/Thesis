import pandas as pd
from pathlib import Path

cols = [
	'analysis_sample_rate',
                                      'bit_rate',
                                         'codec',
                                       'downmix',
                                'equal_loudness',
                                        'length',
                                      'lossless',
                                   'replay_gain',
                                 'essentia_high',
                       'essentia_build_sha_high',
                         'essentia_git_sha_high',
                                'extractor_high',
                                     'gaia_high',
                             'gaia_git_sha_high',
                  'models_essentia_git_sha_high',
                                  'essentia_low',
                        'essentia_build_sha_low',
                          'essentia_git_sha_low',
                                 'extractor_low',
                                 'label'
]

acousticbrainz = pd.read_hdf(Path.cwd() / '..' / 'datasets' / 'acousticbrainzV3.h5')

# Spike in acousticness at 0.09 - 0.10
acoust_spike = acousticbrainz[acousticbrainz[('mood_acoustic', 'acoustic')].between(0.09, 0.10, inclusive=True)]
acoust_rest_low = acousticbrainz[acousticbrainz[('mood_acoustic', 'acoustic')].between(0.00, 0.09, inclusive=False)]
acoust_rest_high = acousticbrainz[acousticbrainz[('mood_acoustic', 'acoustic')].between(0.10, 1.00, inclusive=False)]

acoust_spike['label'] = 'anomaly'
acoust_rest_low['label'] = 'non-anomaly'
acoust_rest_high['label'] = 'non-anomaly'

acoust_anomalies = pd.concat([acoust_spike, acoust_rest_low, acoust_rest_high])
acoust_anomalies = acoust_anomalies[cols].reset_index(drop=True)
acoust_anomalies.to_csv('acousticness_anomalies.csv', index=False)

# Spike in mood relaxed at 0.805 - 0.815
relaxed_spike = acousticbrainz[acousticbrainz[('mood_relaxed', 'relaxed')].between(0.805, 0.815, inclusive=True)]
relaxed_spike_low = acousticbrainz[acousticbrainz[('mood_relaxed', 'relaxed')].between(0.00, 0.805, inclusive=False)]
relaxed_spike_high = acousticbrainz[acousticbrainz[('mood_relaxed', 'relaxed')].between(0.815, 1.00, inclusive=False)]

relaxed_spike['label'] = 'anomaly'
relaxed_spike_low['label'] = 'non-anomaly'
relaxed_spike_high['label'] = 'non-anomaly'

relaxed_anomalies = pd.concat([relaxed_spike, relaxed_spike_low, relaxed_spike_high])
relaxed_anomalies = relaxed_anomalies[cols].reset_index(drop=True)
relaxed_anomalies.to_csv('relaxed_anomalies.csv', index=False)

# Spike in mood electronic at 0.972 - 0.982
electronic_spike = acousticbrainz[acousticbrainz[('mood_electronic', 'electronic')].between(0.972, 0.982, inclusive=True)]
electronic_spike_low = acousticbrainz[acousticbrainz[('mood_electronic', 'electronic')].between(0.00, 0.972, inclusive=False)]
electronic_spike_high = acousticbrainz[acousticbrainz[('mood_electronic', 'electronic')].between(0.982, 1.00, inclusive=False)]

electronic_spike['label'] = 'anomaly'
electronic_spike_low['label'] = 'non-anomaly'
electronic_spike_high['label'] = 'non-anomaly'

electronic_anomalies = pd.concat([electronic_spike, electronic_spike_low, electronic_spike_high])
electronic_anomalies = electronic_anomalies[cols].reset_index(drop=True)
electronic_anomalies.to_csv('electronic_anomalies.csv', index=False)