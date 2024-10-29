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

#Process data and calculate average goal resolution time by queue
# Convert date fields to datetime
df['open_dt'] = pd.to_datetime(df['open_dt'], errors='coerce')
df['closed_dt'] = pd.to_datetime(df['closed_dt'], errors='coerce')
df['sla_target_dt'] = pd.to_datetime(df['sla_target_dt'], errors='coerce')

# Calculate resolution time in days
df['resolution_time'] = (df['closed_dt'] - df['sla_target_dt']).dt.total_seconds() / 86400

# Calculate average resolution time by queue
avg_resolution_time_by_queue = df.groupby('queue')['resolution_time'].mean().reset_index()
avg_resolution_time_by_queue.columns = ['Queue', 'Average Resolution Time (days)']

# Display the average resolution time by queue
print(avg_resolution_time_by_queue)

# Visualization: Box plot of resolution times by queue
plt.figure(figsize=(12, 8))
sns.boxplot(x='queue', y='resolution_time', data=df)
plt.xticks(rotation=45)  # Rotate labels to avoid overlap
plt.title('Distribution of Resolution Times by Queue')
plt.ylabel('Resolution Time (days)')
plt.xlabel('Queue')
plt.tight_layout()  # Adjust layout to make room for label rotation
plt.show()
