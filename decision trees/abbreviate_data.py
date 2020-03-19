import pandas as pd
from pathlib import Path
import hashlib

files = list(Path.cwd().rglob('*_anomalies.csv'))
to_abbreviate = ['essentia_git_sha_low', 'essentia_build_sha_low']

# essentia_git_sha_low and essentia_build_sha_low have very long fields
# these fields are abbreviated so that the decision tree can be plotted
# more clearly

# Fields are shortened by calculating the SHA-1 checksum of the field
# and then taking the smallest substring of that hash that still
# allows us to uniquely identify the different version strings
for file in files:
	print(f"Processing dataset {file.stem}")
	
	df = pd.read_csv(file)

	for col in to_abbreviate:
		print(f"Shortening {col}")
		n_unique = len(df[col].unique())
		n_abbrev = 0
		lim = 1

		while n_abbrev != n_unique:
			abbrev = df[col].apply(lambda x: hashlib.sha1(bytes(x, encoding='utf-8')).hexdigest()[0:lim])
			n_abbrev = len(abbrev.unique())
			lim += 1

		print(f"Shortened to {lim-1} characters")
		df[col] = abbrev

	df.to_csv(f"{file.stem}_abbrev.csv")

