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
		
		for node in nodes:
			# Every two whitespaces are one level, level 5 is the highest level and has 0 whitespaces
			# and will get a score of 5, level 4 has two whitespaces and will get a score of 4 etc...
			# Since each node occurs twice, one for every split, divide the score by two
			score = (5 - (len(node[0]) / 2)) / 2
			name = node[1]

			# Add the scores
			if name in res:
				res[name] += score
			else:
				res[name] = score

		# And add to the main scores dictionary, sorted by score
		scores[file.stem] = res

df = pd.DataFrame(scores).fillna(value=0).astype('int32').sort_values(
	by='acoust_spike', ascending=False)
print(df)
print()

with open(OUTFILE, 'w') as f:
	f.write(df.to_latex())
print(f'Latex table for scores written to {OUTFILE}')
