import streamlit as st
import pandas as pd
import plotly.express as px
import os


st.set_page_config(layout="wide")

access_key=os.getenv("AWS_ACCESS_KEY_ID")

aws_s3_key=os.getenv("AWS_SECRET_ACCESS_KEY")

bucket_name='loadforecastingdata'

# =========================
# LOAD DATA
# =========================
@st.cache_data
def load_data(bucket_name,access_key,aws_s3_key):
    Plants = pd.read_csv(
        f"s3://{bucket_name}/Data/data_tot.csv",
        
        storage_options={
           "key": f"{access_key}",
           "secret": f"{aws_s3_key}",
           "client_kwargs": {
               "region_name": "eu-west-1"
           }
           }
        )
    return Plants

df = load_data(bucket_name,access_key,aws_s3_key)

df['renewables']='Non renewables'

df.loc[df['primary_fuel'].isin(['Wind','Solar','Hydro']),'renewables']='Renewables'


st.title("European Power Plants Dashboard")

# =========================
# FILTRI
# =========================
countries = st.sidebar.multiselect(
    "Select countries",
    df["country"].unique(),
    default='ITA'
)

fuels = st.sidebar.multiselect(
    "Select fuel type",
    df["primary_fuel"].unique(),
    default=df["primary_fuel"].unique()
)

df_filtered = df[
    (df["country"].isin(countries)) &
    (df["primary_fuel"].isin(fuels))
]

# =========================
# KPI
# =========================
st.subheader("Key Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Total Plants", len(df_filtered))
col2.metric("Total Capacity (MW)", round(df_filtered["capacity_mw"].sum(), 2))
col3.metric("Avg Capacity (MW)", round(df_filtered["capacity_mw"].mean(), 2))

# =========================
# MAPPA EUROPA
# =========================
st.subheader("Map")

col1,col2=st.columns(2, gap="small")

map_style=st.sidebar.selectbox('Select Map style', [
    "carto-positron",
    "carto-darkmatter",
    "open-street-map",
    "white-bg"
],index=0)

with col1:
            
    fig_map = px.scatter_mapbox(
        df_filtered,
        lat="latitude",
        lon="longitude",
        size="capacity_mw",
        color="primary_fuel",
        hover_name="name",
        zoom=3,
        height=500
    )
    
    fig_map.update_layout(mapbox_style=map_style)
    
    st.plotly_chart(fig_map, use_container_width=True)
    
    # =========================
    # CAPACITÀ PER PAESE
    # =========================
    
    df_country = df_filtered.groupby(["country","primary_fuel"])["capacity_mw"].sum().reset_index()
    
    st.subheader("Capacity by Country")
    
    fig_bar = px.bar(
        df_country,
        x="country",
        y="capacity_mw",
        color="primary_fuel"
    )
    
    st.plotly_chart(fig_bar, use_container_width=True)
    
with col2:
    
    
    
    fig_map = px.scatter_mapbox(
        df_filtered,
        lat="latitude",
        lon="longitude",
        size="capacity_mw",
        color="renewables",
        hover_name="name",
        zoom=3,
        height=500
    )
    
    fig_map.update_layout(mapbox_style=map_style)
    
    st.plotly_chart(fig_map, use_container_width=True)
    
    # =========================
    # CAPACITÀ PER PAESE
    # =========================
    
    df_country = df_filtered.groupby(["country","renewables"])["capacity_mw"].sum().reset_index()
    
    st.subheader("Capacity by Country")
    
    fig_bar = px.bar(
        df_country,
        x="country",
        y="capacity_mw",
        color="renewables"
    )
    
    st.plotly_chart(fig_bar, use_container_width=True)
