import json
import urllib.request
import pandas as pd


query_url = 'https://data.boston.gov/api/3/action/datastore_search'  # query url
resource_id = '382e10d9-1864-40ba-bef6-4eea3c75463c'  # resource id for 311 calls in 2012 - CHANGE PER YEAR

def fetch_311_data(resource_id, limit=1000, offset=0):
    url = f'{query_url}?resource_id={resource_id}&limit={limit}&offset={offset}'
    fileobj = urllib.request.urlopen(url)
    response_dict = json.loads(fileobj.read())
    return response_dict['result']['records']


all_data = []
offset = 0
batch_size = 1000

while True:
    batch_data = fetch_311_data(resource_id, limit=batch_size, offset=offset)
    if not batch_data: 
        break
    all_data.extend(batch_data)
    offset += batch_size  
    print(f"Fetched {len(all_data)} records so far")

df = pd.DataFrame(all_data)

df['case_status'] = df['case_status'].str.lower().str.strip()

closed_count = df['case_status'].eq('closed').sum()
unresolved_count = df['case_status'].eq('open').sum()
no_data_count = df['case_status'].isnull().sum()

total_count = len(df)

closed_percentage = (closed_count / total_count) * 100 if total_count > 0 else 0
unresolved_percentage = (unresolved_count / total_count) * 100 if total_count > 0 else 0
no_data_percentage = (no_data_count / total_count) * 100 if total_count > 0 else 0

print(f"Closed Requests: {closed_percentage:.2f}%")
print(f"No Data (Null) Requests: {no_data_percentage:.2f}%")
print(f"Unresolved (Open) Requests: {unresolved_percentage:.2f}%")
