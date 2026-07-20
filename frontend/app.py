import streamlit as st
import requests
import plotly.graph_objects as go
from streamlit_lottie import st_lottie

# 1. Page Configuration (Must be the first Streamlit command)
st.set_page_config(page_title="AgroClimatic Risk Mapper", page_icon="🌍", layout="wide")

# API Connection
API_URL = "http://127.0.0.1:8000/api/v1"

# 2. Lottie Animation Helper
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Load a weather/nature animation
weather_anim = load_lottieurl("https://lottie.host/80a240d8-04e3-4d43-9844-cb8ffbc54f5c/4z6y5h3GqP.json")

# 3. Header Section
st.title("🌍 AgroClimatic Risk Mapper 3D")
st.markdown("### Premium AI-Powered Crop Risk Analytics")
st.divider()

# 4. Main Layout (Two Columns)
col1, col2 = st.columns([1.2, 1])

with col1:
    st.markdown("#### Global Climate Monitoring")
    
    # Create the 3D Interactive Globe
    fig = go.Figure(data=go.Scattergeo(
        lon=[77.70], # Longitude for Meerut
        lat=[29.00], # Latitude for Meerut
        text=['Meerut (Active Zone)'],
        mode='markers',
        marker=dict(size=12, color='#00FF00', line=dict(width=2, color='white')) # Neon green marker
    ))
    
    fig.update_layout(
        geo=dict(
            projection_type='orthographic', # Makes it a 3D globe
            showland=True,
            landcolor="#0a2540", # Dark blue land
            showocean=True,
            oceancolor="#041421", # Deep blue ocean
            showcountries=True,
            countrycolor="#1c3a5e",
            bgcolor="rgba(0,0,0,0)"
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=0, b=0)
    )
    
    # Display the globe
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("#### Run Risk Assessment")
    
    # Form layout for inputs
    with st.container():
        district_input = st.text_input("📍 Target District", value="Meerut")
        crop_input = st.text_input("🌱 Target Crop", value="Sugarcane")
        
        if st.button("Run Analytics Engine", type="primary", use_container_width=True):
            with st.spinner("Analyzing climatic conditions..."):
                try:
                    # Ping your FastAPI backend
                    response = requests.get(f"{API_URL}/risk-assessment", params={
                        "district": district_input, 
                        "crop_name": crop_input
                    })
                    
                    if response.status_code == 200:
                        data = response.json()
                        st.success("✅ Analysis Complete")
                        
                        # Display results in columns
                        res_col1, res_col2 = st.columns(2)
                        res_col1.metric("Risk Score", f"{data['risk_score_out_of_10']} / 10")
                        res_col2.metric("Overall Level", data['overall_risk_level'])
                        
                        if data['warnings']:
                            for warning in data['warnings']:
                                st.warning(f"⚠️ {warning}")
                    else:
                        st.error(f"Error: {response.json().get('detail', 'Could not fetch data. Check if district/crop exist.')}")
                
                except requests.exceptions.ConnectionError:
                    st.error("🚨 Connection Error: Is your FastAPI backend running on port 8000?")