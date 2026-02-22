-- Create dim_date
CREATE TABLE IF NOT EXISTS `supply-chain-dw.supply_chain_dw.dim_date` (
    date_key INT64,
    full_date DATE,
    year INT64,
    quarter INT64,
    month INT64,
    day INT64
);

-- Create dim_customer
CREATE TABLE IF NOT EXISTS `supply-chain-dw.supply_chain_dw.dim_customer` (
    customer_key INT64,
    customer_id STRING,
    customer_name STRING,
    segment STRING
);

-- Create dim_location
CREATE TABLE IF NOT EXISTS `supply-chain-dw.supply_chain_dw.dim_location` (
    location_key INT64,
    country STRING,
    state STRING,
    city STRING,
    region STRING
);

-- Create dim_product
CREATE TABLE IF NOT EXISTS `supply-chain-dw.supply_chain_dw.dim_product` (
    product_key INT64,
    product_id STRING,
    category STRING,
    sub_category STRING,
    product_name STRING,
    product_price FLOAT64,
    rating_rate FLOAT64,
    rating_count INT64
);

-- Create fact_orders
CREATE TABLE IF NOT EXISTS `supply-chain-dw.supply_chain_dw.fact_orders` (
    order_key INT64,
    order_id STRING,
    date_key INT64,
    customer_key INT64,
    location_key INT64,
    product_key INT64,
    sales FLOAT64,
    quantity INT64,
    discount FLOAT64,
    profit FLOAT64,
    lead_time_days INT64
);