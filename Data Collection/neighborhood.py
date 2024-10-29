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


df['open_dt'] = pd.to_datetime(df['open_dt'], errors='coerce')
df['closed_dt'] = pd.to_datetime(df['closed_dt'], errors='coerce')
df['sla_target_dt'] = pd.to_datetime(df['sla_target_dt'], errors='coerce')

# Calculate resolution time in days
df['resolution_time'] = (df['closed_dt'] - df['sla_target_dt']).dt.total_seconds() / 86400

# Ensure 'neighborhood' field is treated as a string and fill any NaNs with 'Unknown'
df['neighborhood'] = df['neighborhood'].fillna('Unknown')

# Calculate average resolution time by queue and neighborhood
avg_resolution_time_by_queue_neighborhood = df.groupby(['queue', 'neighborhood'])['resolution_time'].mean().reset_index()
avg_resolution_time_by_queue_neighborhood.columns = ['Queue', 'Neighborhood', 'Average Resolution Time (days)']

# Display the average resolution time by queue and neighborhood
print(avg_resolution_time_by_queue_neighborhood)


# Pivot the data for heatmap; using median resolution time for each queue and neighborhood
pivot_table = df.pivot_table(index='queue', columns='neighborhood', values='resolution_time', aggfunc=np.median)

# Visualization: Heatmap of median resolution times
plt.figure(figsize=(14, 10))
sns.heatmap(pivot_table, annot=True, fmt=".1f", cmap="YlGnBu", linewidths=.5)
plt.title('Median Resolution Times by Queue and Neighborhood')
plt.ylabel('Queue')
plt.xlabel('Neighborhood')
plt.xticks(rotation=45)  # Rotate neighborhood labels to avoid overlap
plt.tight_layout()  # Adjust layout to make room for label rotation
plt.show()
