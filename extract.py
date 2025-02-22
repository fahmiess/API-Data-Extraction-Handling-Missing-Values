import requests
import pandas as pd
import os

def fetch_data(api_url):
    """Fetch data from an API and return as JSON"""
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error {response.status_code}: Unable to fetch data")
        return None

def process_data(data):
    """Convert JSON data to a Pandas DataFrame and clean it"""
    df = pd.DataFrame(data)
    # Example: Rename columns, drop unnecessary ones, fill missing values
    df = df.rename(columns={'id': 'User ID', 'name': 'Full Name'})
    df = df.fillna('Unknown')
    return df

def save_to_csv(df, filename="powerbi_data.csv"):
    """Save DataFrame to a CSV file"""
    output_path = os.path.join(os.getcwd(), filename)
    df.to_csv(output_path, index=False)
    print(f"Data saved to {output_path}")

if __name__ == "__main__":
    API_URL = "https://jsonplaceholder.typicode.com/users"  # Replace with actual API
    raw_data = fetch_data(API_URL)
    
    if raw_data:
        cleaned_data = process_data(raw_data)
        save_to_csv(cleaned_data)
