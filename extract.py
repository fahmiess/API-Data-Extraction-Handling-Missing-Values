import requests
import pandas as pd
import os
import streamlit as st

@st.cache_data
def fetch_data(api_url):
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error {response.status_code}: Unable to fetch data")
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
    st.success(f"Data saved to {output_path}")

def main():
    st.title("Power BI Data Extractor")
    api_url = st.text_input("Enter API URL", "https://jsonplaceholder.typicode.com/users")
    
    if st.button("Fetch Data"):
        raw_data = fetch_data(api_url)
        if raw_data:
            cleaned_data = process_data(raw_data)
            st.write("### Processed Data", cleaned_data)
            save_to_csv(cleaned_data)
            st.download_button("Download CSV", cleaned_data.to_csv(index=False), "powerbi_data.csv", "text/csv")

if __name__ == "__main__":
    main()
