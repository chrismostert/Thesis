from pathlib import Path
import pandas as pd

dataset = Path("C:/Users/Chris/Documents/Thesis/datasets/acousticbrainz-highlevel-json-20150130/highlevel")
files = dataset.rglob("*.json")

metadata = {
	mbids = [],
	submissionIDs = []
}

analysis_sample_rate = []
bit_rate = []
codec = []
downmix = []
equal_loadness = []
length = []
lossless = []
replay_gain = []
sample_rate = []

for file in files:
	stem = file.stem
	mbid = stem[0]
	submissionID = stem[1]
