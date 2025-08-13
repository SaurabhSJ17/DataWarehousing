# Databricks notebook source
# MAGIC %sql
# MAGIC CREATE SCHEMA IF NOT EXISTS dwh_sales;

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE TABLE IF NOT EXISTS dwh_sales_core
# MAGIC AS
# MAGIC SELECT * FROM hive_metastore.sales_wh.core_table;
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM hive_metastore.dwh_sales.sales_core;

# COMMAND ----------

# MAGIC %md
# MAGIC ##customer_dimensions

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE VIEW dwh_sales.customer_dim_view
# MAGIC AS
# MAGIC SELECT *, ROW_NUMBER() OVER(ORDER BY CustomerID) AS DimCustomersKey FROM(
# MAGIC   SELECT  
# MAGIC   DISTINCT( CustomerID) AS CustomerID,
# MAGIC   CustomerName,
# MAGIC   CustomerEmail
# MAGIC   FROM hive_metastore.dwh_sales.sales_core );
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE TABLE IF NOT EXISTS  dwh_sales.DimCustomer
# MAGIC AS 
# MAGIC SELECT * FROM hive_metastore.dwh_sales.customer_dim_view;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM dwh_sales.DimCustomer;

# COMMAND ----------

# MAGIC %md
# MAGIC ## PRODUCT DIMENSION

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE VIEW dwh_sales.product_dim_view
# MAGIC AS
# MAGIC SELECT *, ROW_NUMBER() OVER(ORDER BY ProductID) AS DimProductsKey FROM(
# MAGIC   SELECT  
# MAGIC   DISTINCT( ProductID) AS ProductID,
# MAGIC   ProductName,
# MAGIC   ProductCategory
# MAGIC   FROM hive_metastore.dwh_sales.sales_core );

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE TABLE IF NOT EXISTS dwh_sales.DimProduct
# MAGIC AS 
# MAGIC SELECT * FROM hive_metastore.dwh_sales.product_dim_view;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM dwh_sales.DimProduct;

# COMMAND ----------

# MAGIC %md
# MAGIC ##REGION DIMENSION

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE VIEW dwh_sales.region_dim_view
# MAGIC AS
# MAGIC SELECT *, ROW_NUMBER() OVER(ORDER BY RegionID) AS DimregionKey FROM(
# MAGIC   SELECT  
# MAGIC   DISTINCT( RegionID) AS RegionID,
# MAGIC   RegionName,
# MAGIC   Country
# MAGIC   FROM hive_metastore.dwh_sales.sales_core );

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE TABLE IF NOT EXISTS dwh_sales.DimRegion
# MAGIC AS 
# MAGIC SELECT * FROM hive_metastore.dwh_sales.region_dim_view;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM dwh_sales.DimRegion;

# COMMAND ----------

# MAGIC %md
# MAGIC ##DATE DIMENSION

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE VIEW dwh_sales.date_dim_view
# MAGIC AS
# MAGIC SELECT *, ROW_NUMBER() OVER(ORDER BY OrderDate) AS DimDateKey 
# MAGIC FROM
# MAGIC (
# MAGIC   SELECT  
# MAGIC   DISTINCT( OrderDate) AS OrderDate
# MAGIC   FROM 
# MAGIC   hive_metastore.dwh_sales.sales_core );

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE TABLE IF NOT EXISTS dwh_sales.DimDate
# MAGIC AS 
# MAGIC SELECT * FROM hive_metastore.dwh_sales.date_dim_view;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM dwh_sales.DimDate;
# MAGIC desc 

# COMMAND ----------

# MAGIC %md
# MAGIC ##FACT TABLE (STAR SCHEMA)

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE VIEW dwh_sales.fact_view
# MAGIC AS
# MAGIC SELECT F.OrderID ,
# MAGIC F.Quantity, 
# MAGIC F.UnitPrice,
# MAGIC F.TotalAmount,
# MAGIC DC.DimCustomersKey,
# MAGIC DP.DimProductsKey,
# MAGIC R.DimregionKey,
# MAGIC D.DimDateKey
# MAGIC FROM 
# MAGIC hive_metastore.dwh_sales.sales_core F
# MAGIC LEFT JOIN hive_metastore.dwh_sales.dimcustomer DC 
# MAGIC On DC.CustomerID = F.CustomerID
# MAGIC LEFT JOIN hive_metastore.dwh_sales.dimproduct DP 
# MAGIC On Dp.ProductID = F.ProductID
# MAGIC LEFT JOIN hive_metastore.dwh_sales.dimregion R
# MAGIC On R.RegionID = F.RegionID
# MAGIC LEFT JOIN hive_metastore.dwh_sales.dimdate D
# MAGIC On D.OrderDate = F.OrderDate;
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE TABLE IF NOT EXISTS dwh_sales.Fact_sales
# MAGIC SELECT * FROM dwh_sales.fact_view;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM dwh_sales.fact_view;
