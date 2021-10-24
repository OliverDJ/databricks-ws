# Databricks notebook source
from pyspark.sql.functions import *
from pyspark.sql.types import *
import json
import datetime

# COMMAND ----------

user_schema = StructType(
    [
        StructField('Id', IntegerType(), True)
      , StructField('Name', StringType(), True)
      , StructField('Age', IntegerType(), True)
      , StructField('SSN', StringType(), True)
      , StructField('CreatedAt', TimestampType(), True)
    ])

# COMMAND ----------

# import pyspark class Row from module sql
from pyspark.sql import *

# COMMAND ----------

columns = ['migration_id', 'product_version', 'created_at']
vals = [(migration_name, version, datetime.now())]
df = spark.createDataFrame(vals, columns)

# COMMAND ----------

# MAGIC %md
# MAGIC # Json

# COMMAND ----------

user_dict =(
  {
    "Id": 1, 
    "Name": "Kim",
    "Age": 39,
    "SSN": "01013900244",
    "CreatedAt": datetime.datetime.now() 
  }
)

user_json = from_json(user_dict, user_schema)

# COMMAND ----------

# import pyspark class Row from module sql
from pyspark.sql import *


