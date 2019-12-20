import pandas as pd
from pathlib import Path
from tqdm import tqdm
import os.path

# Get paths for dataframe
def getPaths(folder):
	return list(folder.glob("**/*.pkl"))

# Returns chunks of paths of size N
def chunks(paths, N):
	for i in range(0, len(paths), N):
		yield paths[i:i + N]

def mergeChunk(chunk, chunkno, location):
	frames = []
	name = 'part-{no}.h5'.format(no=chunkno)
	if os.path.isfile(location / name):
		print("Chunk already merged, skipping...")
		return
	print("Reading in frames for chunk {no}".format(no=chunkno))
	for frame in tqdm(chunk):
		frames.append(pd.read_pickle(frame))
	print("Concatinating and writing to {filename}".format(filename=name))
	pd.concat(frames).to_hdf(Path.cwd() / name, key='data')


if __name__ == "__main__":
	inputFolder = Path.cwd() / 'out'
	outputFolder = Path.cwd()
	print("Fetching dataframes...")
	paths = getPaths(inputFolder)
	total = len(paths)
	print("{c} dataframes to be processed".format(c=total))

	NOCHUNKS = 10
	chunkSize = int(total/NOCHUNKS)
	print("Using chunksize {s}".format(s=chunkSize))

	chunkNo = 0
	for chunk in chunks(paths, chunkSize):
		mergeChunk(chunk, chunkNo, outputFolder)
		chunkNo += 1

	print("Merging parts into one dataframe...")
	frames = []
	for frame in outputFolder.glob("**/part-*.h5"):
		frames.append(pd.read_hdf(frame))
	pd.concat(frames).to_hdf(outputFolder / 'acousticbrainz.h5', key='data')