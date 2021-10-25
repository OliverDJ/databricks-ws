# Databricks notebook source
trees = spark.read.csv("/mnt/db-ws-lake/bronze/trees.csv", header="true", inferSchema="true")

# COMMAND ----------

trees.display()

# COMMAND ----------

from pyspark.sql.functions import *
from pyspark.sql.types import *
# udf = user defined function
def heightDivGirth(girth, height):
  return girth / height

heightDivGirth_udf = udf(heightDivGirth, DoubleType())

# COMMAND ----------


trees2 = (trees
  .withColumnRenamed("index", "id")
  .withColumn('Height/Girth', heightDivGirth_udf(col('Height'), col('Girth')))
  .withColumn('Type', lit('Oak'))
 )

# COMMAND ----------

trees2.display()

# COMMAND ----------

trees2
  .write
  .format("com.databricks.spark.csv")
  .option("header", "true")
  .save("/mnt/db-ws-lake/bronze/trees2.csv")
