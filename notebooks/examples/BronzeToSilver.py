# Databricks notebook source
from pyspark.sql.types import *
from pyspark.sql.functions import *
import json

# COMMAND ----------

# MAGIC %md 
# MAGIC 
# MAGIC ```
# MAGIC type EventhubMessage<'T> = 
# MAGIC     {
# MAGIC         Version: string
# MAGIC         Payload: 'T
# MAGIC     }
# MAGIC 
# MAGIC type User = 
# MAGIC     {
# MAGIC         Name: string
# MAGIC         Ssn: string
# MAGIC         LastName: string
# MAGIC     }
# MAGIC ```

# COMMAND ----------

def createEventhubMessageSchema(payload_schema):
    eventhub_message_schema = (
        StructType(
            [
                StructField('Version', StringType(), True),
                StructField('Payload', payload_schema, True)
            ]
        ))      
    return eventhub_message_schema

# COMMAND ----------

user_schema = StructType(
    [
        StructField('Name', StringType(), True)
      , StructField('Ssn', StringType(), True)
      , StructField('LastName', StringType(), True)
    ])

# COMMAND ----------

eventhub_message_schema = createEventhubMessageSchema(user_schema)

# COMMAND ----------

# MAGIC %md 
# MAGIC ## Stream

# COMMAND ----------

bronze_stream = (
    spark.readStream
      .format("delta")
      .table('users_bronze')
  )

# COMMAND ----------

deserialized_df = (
  bronze_stream
    .withColumn("eventhubmessage", from_json(col("body"), eventhub_message_schema))
)

# COMMAND ----------

clean_df = (
  deserialized_df.select(
      deserialized_df.eventhubmessage.Version
    , 'eventhubmessage.Payload.Name'
    , deserialized_df.eventhubmessage.Payload.Ssn
    , 'eventhubmessage.Payload.LastName'
  )
)

# COMMAND ----------

renamed_df = (
  clean_df
    .withColumnRenamed('eventhubmessage.Version', 'Version')
    .withColumnRenamed('eventhubmessage.Payload.Ssn', 'Ssn')
)

# COMMAND ----------

def ssnToGender(ssn):
    marker = int(ssn[8])
    if (marker % 2 == 0):
        return "female"
    else: return "male"
    
ssnToGender_udf = udf(ssnToGender, StringType())

# COMMAND ----------

transformed = (
  renamed_df
    .withColumn('Gender', ssnToGender_udf(col('Ssn')))
    .withColumn('Country', lit('Norway'))
)
  

# COMMAND ----------

gdpr_safe = transformed.drop('Ssn')

# COMMAND ----------

path = "user_data"
silver_mount_point = "/mnt/db-ws-lake/silver"
silver_checkpoint_path = "{0}/{1}.checkpoint".format(silver_mount_point, path)
silver_storage_path = "{0}/{1}.delta".format(silver_mount_point, path)

# COMMAND ----------

gdpr_safe.display()

# COMMAND ----------


(gdpr_safe.writeStream 
    .format("delta") 
    .option("checkpointLocation", silver_checkpoint_path) 
    .outputMode("append") 
    .trigger(once=True)
    .start(silver_storage_path)
)
