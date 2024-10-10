import json
import urllib.request
import pandas as pd

#Step 1:Make the API call to CKAN
query_url = 'https://data.boston.gov/api/3/action/datastore_search' #query url
resource_id = '382e10d9-1864-40ba-bef6-4eea3c75463c'  #resource id for 311 calls in 2012 - CHANGE PER YEAR

def fetch_311_data(resource_id, limit = 1000, offset = 0):
    url = f'{query_url}?resource_id={resource_id}&limit={limit}&offset={offset}'
    fileobj = urllib.request.urlopen(url)
    response_dict = json.loads(fileobj.read())
    return response_dict['result']['records']


#Step 2: Fetch all the data
all_data = []
offset = 0
batch_size = 1000

while True:
    # Fetch a batch of data
    batch_data = fetch_311_data(resource_id, limit=batch_size, offset=offset)
    if not batch_data:  # No more data to fetch
        break
    all_data.extend(batch_data)
    offset += batch_size  # Move to the next batch
    print(f"Fetched {len(all_data)} records so far")

df = pd.DataFrame(all_data)


#Step 3: Process data and query what you need
#get the year for the current data set
df['open_dt'] = pd.to_datetime(df['open_dt'], errors='coerce') #coerce converts invalid dates to NaT
df['year'] = df['open_dt'].dt.year #get the year using pandas datetime

#How is the case volume changing by submission channel SOURCE?


df['source'] = df.get('source', pd.Series()).fillna('Unknown')

case_volume_by_source = df.groupby(['year', 'source']).size().reset_index(name='case_count') #grouping by source and year, and getting the size (count) of cases for each source

print(case_volume_by_source)


