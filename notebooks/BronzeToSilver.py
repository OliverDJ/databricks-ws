# Databricks notebook source
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
    ])

# COMMAND ----------

eventhub_message_schema = createEventhubMessageSchema(user_schema)

# COMMAND ----------

import json

df = (
  read_stream.withColumn("eventhubmessage", from_json(col("body"), eventhub_message_schema))
)

# COMMAND ----------

clean_df = df.select(df.eventhubmessage.Version, 'eventhubmessage.Payload.Name', df.eventhubmessage.Payload.Ssn)
