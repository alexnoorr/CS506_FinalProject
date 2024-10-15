import json
import urllib.request
import pandas as pd
import matplotlib.pyplot as plt

query_url = 'https://data.boston.gov/api/3/action/datastore_search'

def fetch_311_data(resource_id, limit=1000, offset=0):
    url = f'{query_url}?resource_id={resource_id}&limit={limit}&offset={offset}'
    fileobj = urllib.request.urlopen(url)
    response_dict = json.loads(fileobj.read())
    return response_dict['result']['records']

# Load resource IDs for each year
resource_ids_file_path = '/Users/nathanlee/Desktop/CS506/CS506_FinalProject/Data Collection/resource_ids.csv'
resource_ids_df = pd.read_csv(resource_ids_file_path)

all_years_data = []

# Loop through each year and its associated resource ID
for _, row in resource_ids_df.iterrows():
    year = row['Year']
    resource_id = row['Resource ID']
    
    print(f"Fetching data for {year} with resource ID: {resource_id}")
    
    all_data = []
    offset = 0
    batch_size = 10000
    
    # Fetch all data for the given resource ID
    while True:
        batch_data = fetch_311_data(resource_id, limit=batch_size, offset=offset)
        if not batch_data:
            break
        all_data.extend(batch_data)
        offset += batch_size
        print(f"Fetched {len(all_data)} records so far for {year}")
    
    # Convert to DataFrame and store year information
    df = pd.DataFrame(all_data)
    df['open_dt'] = pd.to_datetime(df['open_dt'], errors='coerce')
    df['year'] = df['open_dt'].dt.year
    df['date'] = df['open_dt'].dt.date
    
    # Append data for this year to the all_years_data list
    all_years_data.append(df)

# Concatenate all years' data into one DataFrame
all_years_df = pd.concat(all_years_data)

# Group by year and date to count the number of unique contacts per day
daily_contacts_by_year = all_years_df.groupby(['year', 'date']).size().reset_index(name='daily_count')

# Calculate the average daily contacts for each calendar year
avg_daily_contacts_by_year = daily_contacts_by_year.groupby('year')['daily_count'].mean().reset_index(name='avg_daily_contacts')

# Plot the average daily contacts by year
plt.figure(figsize=(10, 6))
plt.plot(avg_daily_contacts_by_year['year'], avg_daily_contacts_by_year['avg_daily_contacts'], marker='o', linestyle='-', color='b')
plt.title('Average Number of Daily Contacts by Year')
plt.xlabel('Year')
plt.ylabel('Average Daily Contacts')
plt.grid(True)
plt.xticks(avg_daily_contacts_by_year['year'])  # Ensures all years are shown on the x-axis
plt.tight_layout()

# Show the plot
plt.show()
