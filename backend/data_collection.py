import os
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
PEPY_API_KEY = os.getenv("PEPY_API_KEY")


def fetch_download_data(lang_lib):

    langauge = lang_lib['language']
    library = lang_lib['library']
    url = ''

    if langauge == 'python':

        url = f'https://api.pepy.tech/api/v2/projects/{library}'
        headers = {'X-API-Key': PEPY_API_KEY}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
        
            data = response.json()
            downloads = data['downloads']

            df = pd.DataFrame.from_dict(downloads, orient='index')
            df['downloads'] = df.sum(axis=1)
            df = df[df['downloads']]
            df['library'] = library
            df.index = pd.to_datetime(df.index)

            return df
        
        else:
            print(f"Error fetching data for {library}: {response.status_code}")
        
    if langauge == 'javascript':

        url = f'https://api.npmjs.org/downloads/range/2023-09-12:2025-03-12/{library}'
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            downloads = data['downloads']

            df = pd.DataFrame.from_dict(downloads)
            df = df.set_index('day')
            df['library'] = library
            df.index = pd.to_datetime(df.index)

            return df
        
        else:
            print(f"Error fetching data for {library}: {response.status_code}")

data_to_fetch = {'python': ['requests', 'numpy', 'pandas', 'matplotlib', 'scikit-learn', 'flask', 'django', 'tensorflow', 'fastapi', 'pytest'], \
                 'javascript': ['react', 'express', 'lodash', 'axios', 'vue', 'moment', 'webpack', 'd3', 'redux', 'jquery']}

for language in data_to_fetch:
    language_data = []

    for library in data_to_fetch[language]:
        data = fetch_download_data({'language': language, 'library': library})
        language_data.append(data)

        if data is not None:
            language_data.append(data)

    language_data_df = pd.concat(language_data)
    language_data_df.to_csv(f'{language}download_data.csv')

    print(f"Download data saved to '{language}download_data.csv'")