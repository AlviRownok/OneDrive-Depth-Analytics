import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Set the background color to match OneDrive theme
st.markdown(
    """
    <style>
    .stApp {
        background-color: #0078d4; /* OneDrive Blue */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title of the app
st.title("OneDrive Folder Depth Calculator")

# Upload CSV file
uploaded_file = st.file_uploader("Upload your CSV file", type="csv")

if uploaded_file is not None:
    # Read the CSV file
    df = pd.read_csv(uploaded_file, encoding='ISO-8859-1')

    # Display first 30 rows of the 'Percorso' column in a scrollable view
    st.write("Preview of the first 30 entries in 'Percorso' column:")
    st.dataframe(df['Percorso'].head(30))

    # Ask user to select the folder from which depth calculation should begin
    folder_input = st.text_input("Enter the folder name from which depth calculation should begin:")

    # If a folder is specified, calculate the depth
    if folder_input:
        # Calculate the depth level based on user input
        def calculate_depth_from_folder(path, folder_name):
            if folder_name in path:
                # Only count folders after the specified folder name
                return path.split(folder_name, 1)[1].count('/')
            else:
                return 0

        df['depth_level'] = df['Percorso'].apply(lambda x: calculate_depth_from_folder(x, folder_input))

        # Show the updated dataframe with depth level
        st.write("Depth Level Calculated from '{}' folder:".format(folder_input))
        st.dataframe(df[['Percorso', 'depth_level']].head(30))

        # Plot: Depth Level vs Tipo di elemento
        st.write("Plot: Depth Level vs Tipo di elemento")
        plt.figure(figsize=(10, 6))
        df.groupby('depth_level')['Tipo di elemento'].value_counts().unstack().plot(kind='bar', stacked=True)
        plt.title('Depth Level vs Tipo di elemento (Starting from {})'.format(folder_input))
        plt.xlabel('Depth Level')
        plt.ylabel('Count')
        st.pyplot(plt)

        # Plot: Depth Level vs Modificato da
        st.write("Plot: Depth Level vs Modificato da")
        plt.figure(figsize=(10, 6))
        df.groupby('depth_level')['Modificato da'].value_counts().unstack().plot(kind='bar', stacked=True)
        plt.title('Depth Level vs Modificato da (Starting from {})'.format(folder_input))
        plt.xlabel('Depth Level')
        plt.ylabel('Count')
        st.pyplot(plt)
