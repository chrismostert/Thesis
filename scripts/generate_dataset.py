from pathlib import Path
import re
import requests
import time
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from multiprocessing import Pool
import os
import functools
import tarfile
import gzip
import shutil
from multiprocessing import Pool
from tqdm import tqdm

def create_data(url):
    # Check if url is already processed
    outputPath = Path.cwd() / "data"
    stem = url.split("/")[-1].split(".")[0]
    if not os.path.exists(outputPath):
        os.makedirs(outputPath)
    if os.path.isfile(outputPath / (stem + '.pkl')):
        print("{file} was already processed, skipping...".format(file=stem))
    else:
        download(url)
        process(url)
    
def download(url):
    if not os.path.exists(Path.cwd() / "temp"):
        os.makedirs(Path.cwd() / "temp")

    code = 0
    filename = url.split("/")[-1]
    
    while not code is 200:
        s = requests.Session()  
        print("Downloading {filename}".format(filename=filename))
        s.get("http://bit.ly/MLHD-Dataset", allow_redirects=True, headers={'User-agent': 'Mozilla/5.0'})
        r = s.get(url, allow_redirects=True, headers={'User-agent': 'Mozilla/5.0'})
        code = r.status_code

    with open(Path.cwd() / "temp" / filename, 'wb') as f:
        f.write(r.content)

def process(url):
    stem = url.split("/")[-1].split(".")[0]
    filename = Path.cwd() / "temp" / url.split("/")[-1]
    path = Path.cwd() / "temp" / stem
    outputPath = Path.cwd() / "data"
    
    # Create path
    if not os.path.exists(path):
        os.makedirs(path)

    # Unzip all files
    print("Unzipping {file}".format(file=url.split("/")[-1]))
    tarfile.open(filename).extractall(path=path)
    for gz in path.glob('**/*.gz'):
        with gzip.open(gz, 'rb') as f_in:
            with open(path / gz.stem, 'wb') as f_out:
                f_out.write(f_in.read())
        os.remove(gz)
    print("Deleting {name}".format(name=stem + '.tar'))
    os.remove(filename)

    # Process each user, append the dataframes
    df = pd.DataFrame()
    for user in path.iterdir():
        print("Processing {usr}".format(usr=user.stem))
        df = df.append(process_user(user))
    
    # Save data to disk
    print("Saving {name} to data folder".format(name=stem))
    df.to_pickle(outputPath / (stem + '.pkl'))

    # Remove temp files
    shutil.rmtree(path)

def process_user(userFile):
    # Regex to only select items from user files that have a MBID
    p = re.compile(r'(\w+)\x09(.*)\x09(.*)\x09(.+)')
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    cols = ["sad", "not_sad", "happy", "not_happy"]

    data = {}
    for col in cols:
        data[col] = {}
        for m in months:
            data[col][m] = 0

    tuples = p.findall(userFile.read_text())

    for t in tuples:
        features = mood_features.get(t[3])
        if features:
            month = pd.to_datetime(t[0], unit='s').strftime('%b')
            value_sad = features['mood_sad']
            value_happy = features['mood_happy']

            # Increase counts
            data[value_sad][month] += 1
            data[value_happy][month] += 1

    df = pd.DataFrame(data, columns=cols)
    df.index = pd.MultiIndex.from_tuples(map(lambda x: (userFile.stem, x), months))
    return df

baseURL = "https://mcgill-my.sharepoint.com/personal/augusto_vigliensonimartin_mail_mcgill_ca/Documents/MLHD/MLHD_{id}.tar"
URLS = [baseURL.format(id=str(x).zfill(3)) for x in range(0, 576)]
print('Loading mood features into memory...')
mood_features = json.loads((Path.cwd() / 'data' / 'datasets' / 'mood_features.json').read_text())

if __name__ == '__main__':
    pool = Pool(os.cpu_count())
    pool.map(create_data, URLS)