# 🌍 European Power Plants Dashboard

 **Live App**: https://resource-watch-renewables.streamlit.app/

An interactive web application to explore renewable power plants across Europe, built using real-world geospatial data and deployed with Streamlit.

This project combines **data engineering, API integration, and interactive visualization**, with a focus on applications in energy markets.

---

## What you can do

- Explore renewable power plants across Europe
- Filter data by:
  - Country
  - Energy source (wind, solar, etc.)
- Visualize plants on an interactive map
- Analyze installed capacity distribution

---

##  Why this matters

Renewable generation is increasingly driving price dynamics in European electricity markets.

Understanding:
- where assets are located  
- how capacity is distributed  
- which technologies dominate  

is critical for:
- energy trading
- price forecasting
- market analysis

---

## Data Source

Data is retrieved via the **Resource Watch API**, providing access to global environmental datasets.

The dataset includes:
- Latitude & Longitude
- Plant type
- Installed capacity
- Country

---

## Architecture

- Data stored on **AWS S3**
- Secure access via environment variables
- Loaded dynamically into the app
- Processed with **Pandas**
- Visualized with **Plotly**
- Served via **Streamlit**

---

## Tech Stack

- Python
- Pandas
- Streamlit
- Plotly
- AWS S3
