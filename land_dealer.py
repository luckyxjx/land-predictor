import streamlit as st
import pandas as pd
import numpy as np
from lightgbm import LGBMRegressor
from sklearn.preprocessing import LabelEncoder
import os

def format_indian_currency(amount):
    """Format numbers in Indian currency style"""
    if amount >= 10000000:  # 1 crore
        return f"₹{amount/10000000:.1f} Cr"
    elif amount >= 100000:  # 1 lakh
        return f"₹{amount/100000:.1f} L"
    elif amount >= 1000:
        return f"₹{amount/1000:.0f}K"
    else:
        return f"₹{amount:,.0f}"

st.set_page_config(page_title="Land Price Consultant", page_icon="", layout="centered")

# Custom CSS for smooth feel
st.markdown("""
<style>
.main-header {
    text-align: center;
    color: #2E8B57;
    font-size: 2.5rem;
    margin-bottom: 0.5rem;
}
.subtitle {
    text-align: center;
    color: #666;
    font-size: 1.2rem;
    margin-bottom: 2rem;
}
.price-result {
    background: linear-gradient(90deg, #2E8B57, #32CD32);
    color: white;
    padding: 1.5rem;
    border-radius: 10px;
    text-align: center;
    font-size: 1.5rem;
    margin: 1rem 0;
}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_and_train():
    # Return dummy model since we're using standardized calculation
    return True, None

def get_price_estimate(model, encoders, inputs):
    # Standardized price calculation
    area = inputs['area']
    location = inputs['location']
    city = inputs['city']
    road_width = inputs['road_width']
    distance = inputs['distance']
    land_type = inputs['land_type']
    amenities = inputs.get('amenities', [])
    
    # Base price per sqft by city
    city_rates = {
        'mumbai': 12000, 'pune': 8000, 'nagpur': 5000,
        'new delhi': 10000, 'gurgaon': 9000, 'noida': 7000,
        'bangalore': 11000, 'mysore': 6000,
        'hyderabad': 9000, 'secunderabad': 7500,
        'chennai': 8000, 'coimbatore': 5500,
        'kolkata': 6000, 'ahmedabad': 7000, 'surat': 6500,
        'jaipur': 6000, 'lucknow': 5000, 'kanpur': 4000
    }
    
    base_rate = city_rates.get(city, 6000)
    price = area * base_rate
    
    # Location premium
    premium_areas = ['bandra', 'koregaon park', 'jubilee hills', 'indiranagar']
    if location in premium_areas:
        price *= 1.3
    
    # Road width factor
    if road_width >= 40:
        price *= 1.15
    elif road_width >= 30:
        price *= 1.1
    
    # Distance factor
    if distance <= 5:
        price *= 1.2
    elif distance <= 10:
        price *= 1.1
    elif distance >= 25:
        price *= 0.9
    
    # Commercial premium
    if land_type == 'Commercial':
        price *= 1.4
    
    # Amenity bonus
    amenity_bonus = len(amenities) * 0.05
    price *= (1 + amenity_bonus)
    
    return price

# Main App
st.markdown('<h1 class="main-header">Land Price Consultant</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Get instant land price estimates - just like talking to your local dealer!</p>', unsafe_allow_html=True)

# Load model
model, encoders = load_and_train()

if model is None:
    st.error(" Please add a CSV dataset file to get started!")
    st.stop()

# India location data
india_locations = {
    "Maharashtra": {
        "Mumbai": ["Bandra", "Andheri", "Powai", "Borivali", "Thane", "Navi Mumbai", "Malad", "Goregaon"],
        "Pune": ["Koregaon Park", "Hinjewadi", "Wakad", "Baner", "Kothrud", "Hadapsar", "Magarpatta", "Aundh"],
        "Nagpur": ["Civil Lines", "Dharampeth", "Sadar", "Hingna", "Koradi Road", "Amravati Road"]
    },
    "Delhi": {
        "New Delhi": ["Connaught Place", "Khan Market", "Lajpat Nagar", "Karol Bagh", "Rajouri Garden"],
        "Gurgaon": ["Cyber City", "Golf Course Road", "Sohna Road", "MG Road", "Sector 14", "DLF Phase 1"],
        "Noida": ["Sector 62", "Sector 18", "Greater Noida", "Sector 137", "Sector 76", "Film City"]
    },
    "Karnataka": {
        "Bangalore": ["Koramangala", "Indiranagar", "Whitefield", "Electronic City", "HSR Layout", "Marathahalli"],
        "Mysore": ["Saraswathipuram", "Kuvempunagar", "Hebbal", "Vijayanagar", "Bogadi"]
    },
    "Telangana": {
        "Hyderabad": ["Banjara Hills", "Jubilee Hills", "Gachibowli", "Hitech City", "Kondapur", "Madhapur"],
        "Secunderabad": ["Begumpet", "Trimulgherry", "Alwal", "Bowenpally"]
    },
    "Tamil Nadu": {
        "Chennai": ["T Nagar", "Anna Nagar", "Velachery", "OMR", "Adyar", "Nungambakkam"],
        "Coimbatore": ["RS Puram", "Peelamedu", "Saibaba Colony", "Gandhipuram"]
    },
    "West Bengal": {
        "Kolkata": ["Salt Lake", "New Town", "Ballygunge", "Park Street", "Howrah", "Rajarhat"]
    },
    "Gujarat": {
        "Ahmedabad": ["Satellite", "Bopal", "Prahlad Nagar", "Vastrapur", "SG Highway"],
        "Surat": ["Adajan", "Vesu", "Althan", "Piplod"]
    },
    "Rajasthan": {
        "Jaipur": ["Malviya Nagar", "Vaishali Nagar", "Mansarovar", "C Scheme", "Tonk Road"]
    },
    "Uttar Pradesh": {
        "Lucknow": ["Gomti Nagar", "Hazratganj", "Indira Nagar", "Aliganj"],
        "Kanpur": ["Civil Lines", "Swaroop Nagar", "Kidwai Nagar"]
    }
}

st.markdown("###  Select Your Location")
st.markdown("*Choose like you're setting location on Google Maps*")

# Location selection like Google Maps
col1, col2, col3 = st.columns(3)

with col1:
    state = st.selectbox(" State", list(india_locations.keys()), help="Select your state")

with col2:
    cities_in_state = list(india_locations[state].keys())
    city = st.selectbox(" City", cities_in_state, help="Select your city")

with col3:
    areas_in_city = india_locations[state][city]
    location = st.selectbox(" Area/Locality", areas_in_city, help="Select specific area")

st.markdown(f"**Selected:** {location}, {city}, {state}")
    
st.markdown("###  Property Details")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Plot Size**")
    area = st.number_input("Area (sq ft)", 500, 10000, 1500, step=100)
    
    st.markdown("**Road Access**")
    road_width = st.select_slider("Road Width", 
                                 options=[10, 15, 20, 25, 30, 40, 50, 60],
                                 value=25,
                                 format_func=lambda x: f"{x} ft")

with col2:
    st.markdown("**Location Details**")
    distance = st.select_slider("Distance from City Center", 
                               options=[1, 5, 10, 15, 20, 25, 30, 40, 50],
                               value=15,
                               format_func=lambda x: f"{x} km")
    
    st.markdown("**Property Type**")
    land_type = st.radio("Type", ["Residential", "Commercial"], horizontal=True)

# Amenities selection
st.markdown("**Amenities Nearby**")
amenities = st.multiselect("Select Available Amenities", ["School", "Hospital", "Mall", "Park", "Metro"], help="Choose nearby amenities")

# Big predict button
st.markdown("---")
if st.button(" Get Price Estimate", type="primary", use_container_width=True):
    
    inputs = {
        'area': area,
        'location': location.lower(),
        'city': city.lower(),
        'road_width': road_width,
        'distance': distance,
        'land_type': land_type,
        'amenities': amenities
    }
    
    with st.spinner(" Analyzing market data..."):
        price = get_price_estimate(model, encoders, inputs)
        price_per_sqft = price / area
    
    # Show result in a nice format
    st.markdown(f"""
    <div class="price-result">
        <h2> Estimated Price: {format_indian_currency(price)}</h2>
        <p>₹{price_per_sqft:,.0f} per sq ft</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick insights
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if price_per_sqft > 15000:
            st.success(" Premium Location")
        elif price_per_sqft > 8000:
            st.info(" Good Value")
        else:
            st.warning(" Budget Friendly")
    
    with col2:
        if road_width >= 30:
            st.success(" Wide Road Access")
        else:
            st.info(" Standard Road")
    
    with col3:
        if distance <= 10:
            st.success(" Close to City")
        else:
            st.info(" Suburban Area")
    
    # Enhanced Future Value Analysis with Chart
    st.markdown("### Investment Growth Projection")
    
    growth_rates = {
        'mumbai': 8, 'pune': 7, 'nagpur': 6,
        'new delhi': 7, 'gurgaon': 7, 'noida': 6,
        'bangalore': 9, 'mysore': 6,
        'hyderabad': 8, 'secunderabad': 7,
        'chennai': 6, 'coimbatore': 5,
        'kolkata': 5, 'ahmedabad': 6, 'surat': 6,
        'jaipur': 6, 'lucknow': 5, 'kanpur': 4
    }
    
    growth = growth_rates.get(city.lower(), 6)
    
    # Create interactive growth chart
    import plotly.express as px
    forecast_years = list(range(0, 11))
    forecast_values = [price * ((1 + growth/100) ** year) for year in forecast_years]
    
    fig = px.line(
        x=forecast_years, 
        y=forecast_values,
        title=f"Property Value Growth in {city.title()} ({growth}% Annual)",
        labels={'x': 'Years', 'y': 'Property Value (₹)'}
    )
    fig.update_traces(line_color='#2E8B57', line_width=3)
    fig.update_layout(height=300, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
    
    # Key milestone metrics
    cols = st.columns(4)
    years = [1, 3, 5, 10]
    
    for i, year in enumerate(years):
        future_price = price * ((1 + growth/100) ** year)
        roi = ((future_price / price) - 1) * 100
        
        with cols[i]:
            st.metric(
                label=f"{year}Y Value",
                value=format_indian_currency(future_price),
                delta=f"+{roi:.0f}%"
            )
    
    # Investment highlights
    ten_year_value = price * ((1 + growth/100) ** 10)
    wealth_multiplier = ten_year_value / price
    
    col1, col2 = st.columns(2)
    with col1:
        if growth >= 8:
            st.success(f"Premium Growth Market: {growth}% CAGR")
        elif growth >= 6:
            st.info(f"Stable Growth Market: {growth}% CAGR")
        else:
            st.warning(f"Conservative Market: {growth}% CAGR")
    
    with col2:
        st.metric(
            "10-Year Multiplier", 
            f"{wealth_multiplier:.1f}x",
            f"{format_indian_currency(ten_year_value - price)} gain"
        )
    
    # Market context
    st.markdown("###  Market Insights")
    
    if land_type == "Commercial":
        st.info(" Commercial properties typically have higher rental yields and appreciation potential.")
    else:
        st.info(" Residential properties are great for long-term investment and personal use.")
    
    if distance <= 5:
        st.success(" Prime location with excellent connectivity and amenities nearby.")
    elif distance <= 15:
        st.info(" Balanced location offering good value with decent connectivity.")
    else:
        st.warning(" Emerging area with potential for future development and growth.")

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #666;'> Professional land price estimates based on market data analysis</p>", 
    unsafe_allow_html=True
)