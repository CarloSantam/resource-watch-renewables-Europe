# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 11:02:15 2026

@author: Admin
"""

import os
import requests
import pandas as pd
 
# ==============================
# CONFIG
# ==============================
 
JWT = os.getenv("JWT")
API_KEY = os.getenv("API_RESOURCE_WATCH")
 
if not JWT or not API_KEY:
    raise ValueError("Missing JWT or API key. Set them as environment variables.")
 
GEOSTORE_URL = "https://api.resourcewatch.org/v1/geostore"
DATASET_ID = "a86d906d-9862-4783-9e30-cdb68cd808b8"
QUERY_URL = f"https://api.resourcewatch.org/v1/query/{DATASET_ID}"
 
 
headers = {
    "Authorization": f"Bearer {JWT}",
    "x-api-key": API_KEY,
    "Content-Type": "application/json"
}
 
# ==============================
# LOAD ITALY GEOJSON
# ==============================

def fetch_data(country): 
    print(f"Loading {country} GeoJSON...")
     
    geojson_url = f"https://raw.githubusercontent.com/johan/world.geo.json/master/countries/{country}.geo.json"
    geojson = requests.get(geojson_url).json()
     
    # ==============================
    # CREATE GEOSTORE
    # ==============================
     
    print(f"Creating geostore for {country}...")
     
    resp = requests.post(
        GEOSTORE_URL,
        headers=headers,
        json={"geojson": geojson}
    )
     
    resp.raise_for_status()
    geostore_id = resp.json()["data"]["id"]
     
    print(f"Geostore ID: {geostore_id}")
     
    # ==============================
    # QUERY DATA
    # ==============================
     
    sql_query = """
    SELECT 
        name,
        latitude,
        longitude,
        capacity_mw,
        primary_fuel
        
    FROM data
    """
    
    
    params = {
        "sql": sql_query,
        "geostore": geostore_id,
        "format": "json"
    }
     
    print("Querying dataset...")
     
    response = requests.get(
        QUERY_URL,
        headers=headers,
        params=params
    )
     
    response.raise_for_status()
    data = response.json().get("data", [])
     
    # ==============================
    # SAVE RESULTS
    # ==============================
     
    df = pd.DataFrame(data)
     
    print(f"Number of plants found: {len(df)}")
          
    print(f"Data saved to: {OUTPUT_FILE}")
    print(df.head())
    
    return df

EUROPE_MAJOR = [
    "DEU",  # Germany
    "FRA",  # France
    "ITA",  # Italy
    "ESP",  # Spain
    "GBR",  # United Kingdom
    "NLD",  # Netherlands
    "BEL",  # Belgium
    "POL",  # Poland
    "SWE",  # Sweden
    "NOR",  # Norway
    "DNK",  # Denmark
    "FIN"   # Finland
]

df_=pd.DataFrame([])    
for country in EUROPE_MAJOR:
    df=fetch_data(country)
    df['country']=country
    df_=pd.concat([df,df_])
    

access_key=os.getenv("AWS_ACCESS_KEY_ID")

aws_s3_key=os.getenv("AWS_SECRET_ACCESS_KEY")

bucket_name='loadforecastingdata'

df_.to_csv(
    f"s3://{bucket_name}/Data/data_tot.csv",
    index=False,  # Avoid writing index column
    storage_options={
        "key": access_key,
        "secret": aws_s3_key,
        "client_kwargs": {
            "region_name": "eu-west-1"
        }
    }

)


