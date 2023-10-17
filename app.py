import streamlit as st
import pandas as pd
import warnings
warnings.filterwarnings("ignore")
from app_p0 import Streamlit_Page0
from app_p1 import Streamlit_Page1



st.set_page_config(
    page_title="Stocks prediction",  # Set the page title
    page_icon="📈",  # Set a custom page icon
    layout="wide",  # Use wide layout
    initial_sidebar_state="collapsed",  # Start with the sidebar collapsed
)

# Title
st.markdown(
    "<h1 style='text-align: center'>Stocks prediction</h1>", unsafe_allow_html=True
)

# Page selction
selected_page = st.sidebar.selectbox(
    "Go to Page",
    ["Portfolio", "Company"],
)

# Navigate to the selected page
if selected_page == "Portfolio":
    Streamlit_Page0().page_portfolio()