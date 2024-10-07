import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.io as pio

# Set the OneDrive-like color theme (white background, blue text)
st.markdown(
    """
    <style>
    .stApp {
        background-color: white; /* White Background */
    }
    .stTextInput {
        color: #0078d4; /* OneDrive Blue Text */
    }
    h1, h2, h3, h4, h5, h6, label, .stText {
        color: #0078d4 !important; /* OneDrive Blue */
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

        # Prepare interactive plots using Plotly
        # Plot: Depth Level vs Tipo di elemento
        plot_1 = px.histogram(df, x='depth_level', color='Tipo di elemento', title="Depth Level vs Tipo di elemento",
                              color_discrete_sequence=['#0078d4', '#00a1f1'])  # Blue theme

        # Plot: Depth Level vs Modificato da
        plot_2 = px.histogram(df, x='depth_level', color='Modificato da', title="Depth Level vs Modificato da",
                              color_discrete_sequence=['#0078d4', '#00a1f1'])

        # Show the plots
        st.plotly_chart(plot_1)
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

        # Button to download the plots
        pio.write_image(plot_1, "plot_depth_vs_tipo_elemento.png", format='png')
        pio.write_image(plot_2, "plot_depth_vs_modificato_da.png", format='png')

        with open("plot_depth_vs_tipo_elemento.png", "rb") as file1, open("plot_depth_vs_modificato_da.png", "rb") as file2:
            st.download_button(
                label="Download Plot: Depth Level vs Tipo di elemento",
                data=file1,
                file_name="plot_depth_vs_tipo_elemento.png",
                mime="image/png"
            )
            st.download_button(
                label="Download Plot: Depth Level vs Modificato da",
                data=file2,
                file_name="plot_depth_vs_modificato_da.png",
                mime="image/png"
            )
