import json
import urllib.request
import pandas as pd
import pickle
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.preprocessing.text import Tokenizer
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.utils import to_categorical
import os

if os.path.exists('boston_311_data.pkl'):
    with open('boston_311_data.pkl', 'rb') as f:
        df_filtered = pickle.load(f)
    print("Data loaded from pickle file.")
else:
    
    query_url = 'https://data.boston.gov/api/3/action/datastore_search'

    def fetch_311_data(resource_id, limit=1000, offset=0):
        url = f'{query_url}?resource_id={resource_id}&limit={limit}&offset={offset}'
        fileobj = urllib.request.urlopen(url)
        response_dict = json.loads(fileobj.read())
        return response_dict['result']['records']

    # Accesses the resource ids for each year's data in the API request
    resource_ids_file_path = 'https://raw.githubusercontent.com/alexnoorr/CS506_FinalProject/refs/heads/DataCollection-3/Data%20Collection/resource_ids.csv'
    resource_ids_df = pd.read_csv(resource_ids_file_path)

    all_data = []

    # THIS SHOULD RUN FOR A FEW MINUTES IT'S NORMAL
    for _, row in resource_ids_df.iterrows():
        year = row['Year']
        resource_id = row['Resource ID']

        print(f"Fetching data for {year} with resource ID: {resource_id}")

        offset = 0
        batch_size = 10000

        while True:
            batch_data = fetch_311_data(resource_id, limit=batch_size, offset=offset)
            if not batch_data:
                break
            all_data.extend(batch_data)
            offset += batch_size
    df = pd.DataFrame(all_data)
    df['open_dt'] = pd.to_datetime(df['open_dt'], errors='coerce')
    df['year'] = df['open_dt'].dt.year
    print(f'This should be 3,031,846: {len(df)}')
    df_filtered = df[df['year'] != 2010]
    print(len(df_filtered)) #Smaller than 3,031,646
    
    with open('boston_311_data.pkl', 'wb') as f:
        pickle.dump(df_filtered, f)
    print("Data processed and saved to pickle file.")