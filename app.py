import streamlit as st
import pandas as pd

import sector_list as sector_list
import concern as concern
import grok as grok
# Set the page configuration
st.set_page_config(page_title="CityPulse", layout="wide")
st.markdown(
    """
    <style>
    .card {
        background-color: #333333;
        padding: 20px;
        margin: 10px 0;
        border-radius: 10px;
        border: 1px solid #444444;
        box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.5);
    }
    .card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .card h4 {
        color: #ffffff;
        margin: 0;
        font-size: 24px;
    }
    .badge {
        display: inline-block;
        padding: 5px 10px;
        border-radius: 5px;
        color: #ffffff;
        font-size: 14px;
        font-weight: bold;
    }
    .degree-level-1 {
        background-color: #28a745; /* Green */
    }
    .degree-level-2 {
        background-color: #ffc107; /* Amber */
        color: #333333; /* Dark text for better contrast */
    }
    .degree-level-3 {
        background-color: #dc3545; /* Red */
    }
    .card p {
        color: #dddddd;
        font-size: 18px;
        margin: 10px 0;
    }
    .card strong {
        color: #ffffff;
    }
    </style>
    """,
    unsafe_allow_html=True
)



# Load US cities data from the CSV file
@st.cache_data
def load_us_cities():
    print('Loading cities data...')
    df = pd.read_csv('assets/cities.csv',encoding='utf-8')
    return df

us_cities_df = load_us_cities()

st.write("An AI assistant to monitor and analyze social media concerns in your city.")

# City input with autocomplete
city = st.selectbox("Select a US city:", [""] + us_cities_df)
if city == "":
    st.warning("Please select a city.")
else:
    selected_city = city[0]
    
# Create a dictionary to map sector names to Sector objects
sector_dict = {sector.sector: sector for sector in sector_list.SECTOR_LIST}

# Sector selection in the Streamlit app
st.write("### Select Sectors of Interest:")
sector_names = [sector.sector for sector in sector_list.SECTOR_LIST]
selected_sector_names = st.multiselect("", sector_names)

# Corrected line
selected_sectors = [sector_dict[name] for name in selected_sector_names]


# Button to get concerns
if st.button("Get Concerns"):
    if not city:
        st.warning("Please select a city.")
    elif not selected_sectors:
        st.warning("Please select at least one sector.")
    else:
        with st.spinner("Analyzing concerns..."):
            try:
                concerns = grok.get_concerns_mock(selected_sectors, city)
                # concerns = grok.get_concerns(selected_sectors, city)
                # Sort concerns by degree_level
                concerns.sort(key=lambda x: x.degree_level, reverse=True)
                # Display the concerns
                for concern in concerns:
                    st.markdown(
                        f"""
                            <div class='card'>
                                <div class='card-header'>
                                    <h4>Sector: {concern.sector}</h4>
                                    <span class='badge degree-level-{concern.degree_level}'>{concern.degree}</span>
                                </div>
                                <p><strong>Department:</strong> {concern.department}</p>
                                <p><strong>Concern:</strong> {concern.concern}</p>
                            </div>
                            """,
                        unsafe_allow_html=True
                    )

            except Exception as e:
                st.error(f"An error occurred: {e}")