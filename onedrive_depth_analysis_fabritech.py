import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.io as pio
import os

# Set the OneDrive-like color theme (white background, blue text)
st.markdown(
    """
    <style>
    .stApp {
        background-color: white; /* White Background */
    }
    h1, h2, h3, h4, h5, h6, label, .stText {
        color: #0078d4 !important; /* OneDrive Blue */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Function to detect delimiter (for CSV files)
def detect_delimiter(file):
    # Read a small portion of the file to detect delimiter
    sample = file.read(2048).decode('ISO-8859-1')
    file.seek(0)  # Reset file pointer after reading
    if ';' in sample:
        return ';'
    return ','

# Function to determine if a path points to a file or a folder (based on extensions)
def classify_item(path):
    if os.path.splitext(path)[1]:  # Check if there's a file extension
        return 'File'
    else:
        return 'Folder'

# Title of the app
st.title("Folder Depth Calculator")

# Upload CSV or Excel file
uploaded_file = st.file_uploader("Upload your CSV or Excel file", type=["csv", "xlsx", "xls"])

if uploaded_file is not None:
    # Handle different file types
    if uploaded_file.name.endswith('.csv'):
        # Detect delimiter automatically for CSV
        delimiter = detect_delimiter(uploaded_file)
        # Read the CSV file
        df = pd.read_csv(uploaded_file, delimiter=delimiter, encoding='ISO-8859-1')

    elif uploaded_file.name.endswith('.xlsx') or uploaded_file.name.endswith('.xls'):
        # Read Excel file
        df = pd.read_excel(uploaded_file)

    # Preview the first few rows
    st.write("Preview of the first 30 entries in the file:")
    st.dataframe(df.head(30))

    # Check if this is a local folder structure (look for the 'Folder Path' column) or OneDrive ('Percorso')
    if 'Folder Path' in df.columns:
        st.write("Local folder structure detected.")
        # Ask user to select the folder from which depth calculation should begin
        folder_input = st.text_input("Enter the folder name from which depth calculation should begin:")

        if folder_input:
            # For local folders, calculate depth based on 'Folder Path' and user-specified folder
            def calculate_depth_local(path, folder_name):
                if folder_name in path:
                    # Only count folders after the specified folder name
                    return path.split(folder_name, 1)[1].count('\\')
                else:
                    return 0

            df['depth_level'] = df['Folder Path'].apply(lambda x: calculate_depth_local(x, folder_input))
            # Classify each entry as either 'File' or 'Folder'
            df['Item Type'] = df['Folder Path'].apply(classify_item)

            # Plot: Depth Level Distribution (with distinction between Files and Folders)
            plot_1 = px.histogram(df, x='depth_level', color='Item Type', title="Depth Level Distribution (Local Folders and Files)",
                                  color_discrete_sequence=['#0078d4', '#00a1f1'])  # Blue theme
            st.plotly_chart(plot_1)

    elif 'Percorso' in df.columns:
        st.write("OneDrive folder structure detected.")
        # Display first 30 rows of the 'Percorso' column in a scrollable view
        st.write("Preview of the first 30 entries in 'Percorso' column:")
        st.dataframe(df['Percorso'].head(30))

        # Ask user to select the folder from which depth calculation should begin
        folder_input = st.text_input("Enter the folder name from which depth calculation should begin:")

        if folder_input:
            # Calculate the depth level based on user input
            def calculate_depth_onedrive(path, folder_name):
                if folder_name in path:
                    return path.split(folder_name, 1)[1].count('/')
                else:
                    return 0

            df['depth_level'] = df['Percorso'].apply(lambda x: calculate_depth_onedrive(x, folder_input))

            # Plot: Depth Level vs Tipo di elemento
            plot_1 = px.histogram(df, x='depth_level', color='Tipo di elemento', title="Depth Level vs Tipo di elemento",
                                  color_discrete_sequence=['#0078d4', '#00a1f1'])
            st.plotly_chart(plot_1)

            # Plot: Depth Level vs Modificato da
            plot_2 = px.histogram(df, x='depth_level', color='Modificato da', title="Depth Level vs Modificato da",
                                  color_discrete_sequence=['#0078d4', '#00a1f1'])
            st.plotly_chart(plot_2)

    # Button to download the updated CSV
    @st.cache_data
    def convert_df_to_csv(df):
        return df.to_csv(index=False).encode('utf-8')

    csv_data = convert_df_to_csv(df)
    st.download_button(
        label="Download Updated CSV",
        data=csv_data,
        file_name='updated_depth_levels.csv',
        mime='text/csv',
    )
