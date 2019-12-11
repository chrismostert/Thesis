from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# Use seaborn style defaults and set the default figure size
sns.set(rc={'figure.figsize':(10, 4)})

seasons_n = {
    'Jan': 'Winter',
    'Feb': 'Winter',
    'Mar': 'Spring',
    'Apr': 'Spring',
    'May': 'Spring',
    'Jun': 'Summer',
    'Jul': 'Summer',
    'Aug': 'Summer',
    'Sep': 'Autumn',
    'Oct': 'Autumn',
    'Nov': 'Autumn',
    'Dec': 'Winter'
}

seasons_s = {
    'Jan': 'Summer',
    'Feb': 'Summer',
    'Mar': 'Autumn',
    'Apr': 'Autumn',
    'May': 'Autumn',
    'Jun': 'Winter',
    'Jul': 'Winter',
    'Aug': 'Winter',
    'Sep': 'Spring',
    'Oct': 'Spring',
    'Nov': 'Spring',
    'Dec': 'Summer'
}

# Load in country data
countries = pd.read_csv(Path.cwd() / 'data' / 'datasets' / 'countries.csv')
demographics = pd.read_csv(Path.cwd() / 'data' / 'datasets' / 'MLHD_demographics.csv', delimiter='\t')

# Normalize the dataframe so that instead of counts we get ratios
def normalize(df):
    res = pd.DataFrame()
    res['sad'] = df['sad'] / (df['sad'] + df['not_sad'])
    res['not_sad'] = df['not_sad'] / (df['sad'] + df['not_sad'])
    res['happy'] = df['happy'] / (df['happy'] + df['not_happy'])
    res['not_happy'] = df['not_happy'] / (df['happy'] + df['not_happy'])
    return res

# Get the hemisphere for a given user. Only a distinction between northern and southern hemisphere is made
def getHemisphere(user_id):
    try:
        country = demographics.loc[demographics['uuid'] == user_id, 'country'].values[0]
        latitude = countries.loc[countries['country'] == country, 'latitude'].values[0]

        if latitude >= 0:
            return 'n'
        else:
            return 's'
    except:
        return None

# Add values of keys of two dictionaries to each other
def addDictValues(dict1, dict2):
    assert(dict1.keys() == dict2.keys())
    res = {}

    for key in dict1.keys():
        res[key] = dict1[key] + dict2[key]
    
    return res

# Check for which months the user had higher than average values of the given column (for single user)
def higherMonths(df, col):
    mean = df[col].mean()
    return df[col].map(lambda x: x >= mean)

# Given a mapping of month -> true/false, give back 'True' counts per season (for single user)
def perSeason(df, hemisphere):
    res = {
        'Winter': 0,
        'Spring': 0,
        'Summer': 0,
        'Autumn': 0
    }

    for month in df.index:
        if df[month]:
            if hemisphere == 'n':
                res[seasons_n[month]] += 1
            elif hemisphere == 's':
                res[seasons_s[month]] += 1
            else:
                raise("Invalid hemisphere")
    
    return res

# Give back 'True' counts for all users per season
def perSeasonGraph(df, col):
    counts = {}
    for user, selected in df.groupby(level=0):
        monthCounts = higherMonths(selected.loc[user], col)
        hemisphere = getHemisphere(user)

        if hemisphere:
            seasonCounts = perSeason(monthCounts, hemisphere)

            if counts:
                counts = addDictValues(counts, seasonCounts)
            else:
                counts = seasonCounts
    
    pd.DataFrame([counts]).plot(kind='bar')
    plt.show()



# Draw a stacked bargraph of a user dataframe, stacking the given columns (for single user)
def stackedGraph(df, col1, col2):
    df[[col1, col2]].plot(kind='bar', stacked=True)
    plt.show()

# Draw a graph of the sum of higher than average months for the selected column (for all users)
def higherMonthGraph(df, col):
    toGraph = pd.DataFrame()
    for user, selected in df.groupby(level=0):
        toGraph = toGraph.append(higherMonths(selected.loc[user], col))
    toGraph.sum(axis=0).reindex(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']).plot()
    plt.show()


df = pd.read_pickle(Path.cwd() / 'data' / 'MLHD_001.pkl')
df = normalize(df)

perSeasonGraph(df, 'sad')
