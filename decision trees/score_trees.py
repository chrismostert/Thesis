import re
from pathlib import Path
import json
import pandas as pd

OUTFILE = 'scores.tex'

# Save the scores
scores = dict()

# For all tree .txt files...
filelist = list(Path.cwd().rglob('*.txt'))
for file in filelist:
	with open(file, 'r') as f:
		# Read in the R output
		tree = f.read()
		# Find all the nodes using regex... the amount of whitespace denotes the depth
		# of the node and is captured in the first group, the second group denotes the
		# name of the metadata field
		nodes = re.findall('( *).*\) (\w+)', tree)

		# Dictionary to save the scores for this peak in
		res = dict()
		
		# Get amount of levels
		nolevels = 0
		for node in nodes:
			level = (len(node[0]) / 2)+1
			if level > nolevels:
				nolevels = level

		for node in nodes:
			# Every two whitespaces are one level, the highest level has 0 whitespaces
			# and will get a score of nolevels, the next level has two whitespaces and will get a score of nolevels-1 etc...
			score = nolevels - (len(node[0]) / 2)
			name = node[1]

			# Set the highest level we've seen for every node
			if name in res:
				if score > res[name]:
					res[name] = score
			else:
				res[name] = score

		# And add to the main scores dictionary
		scores[file.stem] = res

df = pd.DataFrame(scores).fillna(value=0).astype('int32')
df['total'] = df.sum(axis=1)
df = df.sort_values(by='total', ascending=False)
print(df)
print()

with open(OUTFILE, 'w') as f:
	f.write(df.to_latex())
print(f'Latex table for scores written to {OUTFILE}')
