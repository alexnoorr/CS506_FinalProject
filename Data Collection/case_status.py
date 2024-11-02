import json
import urllib.request
import pandas as pd

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

import matplotlib.pyplot as plt

case_status_data = {"Open/Unresolved Cases": unresolved_percentage, "Closed Cases": closed_percentage}

labels = list(case_status_data.keys())
sizes = list(case_status_data.values())

plt.figure(figsize=(6, 6))
plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
plt.title('Case Status Distribution')
plt.show()
