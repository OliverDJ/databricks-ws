# Databricks notebook source
from pyspark.sql.functions import *
from pyspark.sql.types import *
import json
from datetime import datetime
from pyspark.sql import *

# COMMAND ----------

# import pyspark class Row from module sql
from pyspark.sql import *

# COMMAND ----------

columns = ['product_id', 'version', 'name', 'created_at']
vals = [
    (1337, '1.0.1', 'chocolate chip', datetime.now()), 
    (87, '1.0.1', 'peanutbutter fudge', datetime.now()),
    (12, '2.0.3', 'vanilla extreme', datetime.now())
]
df = spark.createDataFrame(vals, columns)

# COMMAND ----------

df.display()

# COMMAND ----------

v1 = df.filter(col('version') == '1.0.1')

# COMMAND ----------

v1.display()
