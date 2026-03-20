# 🇮🇹 Renewable Power Plants Extraction (Italy)

This repository contains a simple Python script to extract wind and solar power plant data for Italy using the Resource Watch API.

## 📌 Overview

The script:
- Defines a geographic area (Italy) using GeoJSON
- Creates a geostore via the Resource Watch API
- Queries the Global Power Plant Database
- Exports the results to a CSV file

## Data Source

- Resource Watch API  
- Dataset: Global Power Plant Database  
- https://resourcewatch.org/

## Requirements

- Python 3.x
- Required libraries:
  ```bash
  pip install requests pandas
