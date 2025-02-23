import pandas as pd
import streamlit as st

# Simple Styling
st.set_page_config(page_title="CSV Data Processor", page_icon="📊", layout="wide")
st.markdown("""
    <style>
    .big-font {font-size:20px !important;}
    .stButton>button {border-radius: 10px; background-color: #4CAF50; color: white;}
    .stTextInput>div>div>input {border-radius: 10px; border: 2px solid #4CAF50;}
    </style>
    """, unsafe_allow_html=True)

def process_data(df):
    """Custom Data Cleaning Function"""
    if 'id' in df.columns:
        df.rename(columns={'id': 'User ID'}, inplace=True)
    if 'name' in df.columns:
        df.rename(columns={'name': 'Full Name'}, inplace=True)
    df.replace([None, "", "Unknown", "None"], pd.NA, inplace=True)
    return df

def handle_missing_values(df):
    """Suggest and apply solutions for missing values."""
    missing_values = df.isna().sum()
    if missing_values.any():
        st.warning("⚠️ Missing, null, unknown, or None values detected:")
        st.write(missing_values)
        
        for column in df.columns:
            if df[column].isna().sum() > 0:
                st.write(f"### Suggested Solutions for {column}")
                if pd.api.types.is_float_dtype(df[column]) or pd.api.types.is_integer_dtype(df[column]):
                    mean_value = df[column].mean()
                    median_value = df[column].median()
                    mode_value = df[column].mode()[0] if not df[column].mode().empty else None
                    
                    option = st.radio(
                        f"Choose a solution for {column}",
                        ("Mean", "Median", "Mode", "Delete Rows"),
                        key=f"missing_{column}"
                    )
                    
                    if option == "Mean":
                        df[column].fillna(mean_value, inplace=True)
                    elif option == "Median":
                        df[column].fillna(median_value, inplace=True)
                    elif option == "Mode" and mode_value is not None:
                        df[column].fillna(mode_value, inplace=True)
                    elif option == "Delete Rows":
                        df.dropna(subset=[column], inplace=True)
    else:
        st.success("✅ No missing, null, unknown, or None values detected.")
    
    return df

def main():
    st.title("📊 CSV Data Processor")
    st.write("Upload and process data.")
    
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        
        cleaned_data = process_data(df)
        
        # Side-by-side comparison
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("### 📊 Before Cleaning")
            st.dataframe(cleaned_data)
            st.write("#### 🔍 Data Types (Before)")
            st.write(cleaned_data.dtypes)
            st.write("#### 🛑 Missing Values (Before)")
            st.write(cleaned_data.isna().sum())
        
        cleaned_data = handle_missing_values(cleaned_data)
        
        with col2:
            st.write("### 📊 After Cleaning")
            st.dataframe(cleaned_data)
            st.write("#### 🔍 Data Types (After)")
            st.write(cleaned_data.dtypes)
            st.write("#### ✅ Missing Values (After)")
            st.write(cleaned_data.isna().sum())
        
        # Save file with user input
        file_name = st.text_input("Enter file name (without extension):", "cleaned_data")
        if st.button("⬇️ Download Data"):
            csv_path = f"{file_name}.csv"
            cleaned_data.to_csv(csv_path, index=False)
            with open(csv_path, "rb") as f:
                st.download_button("Download Data", f, file_name=csv_path, mime="text/csv")

if __name__ == "__main__":
    main()
