# Supply Chain Data Integration System

![Python](https://img.shields.io/badge/Python-3.12-blue)
![BigQuery](https://img.shields.io/badge/BigQuery-Data%20Warehouse-yellow)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen)

## Overview

- This project implements a Supply Chain Data Integration System using a dimensional data warehouse architecture in Google BigQuery and a real-time analytics dashboard built with Streamlit.

- The system integrates structured sales data and simulated product metadata, applies transformations using Python, models the data into a star schema, and exposes business insights through interactive visualizations.


## Architecture

Raw Data (CSV + API)
        ↓
Python ETL (Transformation & Surrogate Keys)
        ↓
Star Schema in BigQuery
        ↓
Analytical Views
        ↓
Streamlit Dashboard

## Architecture Diagram

![Architecture](assets/architecture.png)


## Data Model

### Fact Table
- fact_orders

### Dimension Tables
- dim_product
- dim_customer
- dim_date
- dim_location


## Tech Stack

- Python (ETL & Transformation)
- Google BigQuery (Data Warehouse)
- Streamlit (Dashboard)
- Plotly (Visualization)
- Pandas (Data Processing)
- Google Cloud SDK



## Run Locally

1. Clone the repository
2. Create virtual environment
3. Install dependencies:

   pip install -r requirements.txt

4. Set environment variables in .env

5. Run dashboard:

   streamlit run dashboard/app.py


## Dashboard Screenshots Preview

<p align="center">
  <img src="assets/monthly_sales_trend.png" width="800"><br><br>
  <img src="assets/state_sales_map.png" width="800">
</p>


## Future Enhancements
- Add CI/CD pipeline
- Add Docker containerization
- Implement automated testing
- Deploy to Streamlit Cloud
