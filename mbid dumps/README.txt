MBIDS correspond to acousticbrainz-highlevel-json-20150130.tar.bz2 (ftp://ftp.acousticbrainz.org/pub/acousticbrainz/acousticbrainz-highlevel-json-20150130.tar.bz2)

--- all.txt ---
Contains the MBIDs of the entire dataset.

--- filtered_multiple_submissions.txt ---
Contains the MBIDs of the recordings for which at least two submissions were present in the dataset

Used for calculating variance metrics

--- filtered_beatles_songs.txt ---
Contains the MBIDs of recordings for which artist == 'The Beatles'.

Used for further analysis on a more genre consistent dataset

--- genre_dataset_intersection.txt ---
Contains the MBIDs that were present in all three of the Discogs, LastFM and Tagtraum sets downloaded from:
(https://github.com/MTG/acousticbrainz-genre-dataset) (https://drive.google.com/drive/folders/15MDGFj7yo01xHHfNO_oQV43jKBk0sTm6)
Filenames: acousticbrainz-mediaeval2017-discogs-train.tsv, acousticbrainz-mediaeval2017-lastfm-train.tsv, acousticbrainz-mediaeval2017-tagtraum-train.tsv

Used for comparing genre distributions of data slices in the AcousticBrainz data


--- spotify_msd_intersection.txt ---
Contains the MBIDs that were able to be mapped to spotify IDs through the MSD data (http://millionsongdataset.com/).

Used for calculating correlations between high-level classifiers in Acousticbrainz and classifiers provided by Spotify (https://developer.spotify.com/documentation/web-api/reference/tracks/get-audio-features/)