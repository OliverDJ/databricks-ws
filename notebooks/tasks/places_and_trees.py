# Databricks notebook source
places_csv_path = "/mnt/db-ws-lake/bronze/places.csv"
trees_csv_path = "/mnt/db-ws-lake/bronze/trees.csv"

# COMMAND ----------

# MAGIC %md
# MAGIC 
# MAGIC 1. How many tries does each place have
# MAGIC 2. Which place has the most trees?
# MAGIC 3. Which place has the the most amount of trees based on the height? (sum of heights per place)
# MAGIC 4. Which place has the most amount of trees based X = (girth^2) / (4*Volume) (sum of X per place)
