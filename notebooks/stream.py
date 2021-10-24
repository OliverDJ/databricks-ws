# Databricks notebook source
# encrypts the eventhub connection string and creates a dictionary: eventhub_conf that is passed into .readStream.format("eventhubs").options(**eventhub_conf)
#requires maven plibrary installed on cluster: com.microsoft.azure:azure-eventhubs-spark_2.12:2.3.18
def create_eventhub_config(connection_string, consumer_group):
  conf = {}
  encrypted_connection_string = sc._jvm.org.apache.spark.eventhubs.EventHubsUtils.encrypt(connection_string)
  conf["eventhubs.connectionString"] = encrypted_connection_string
  conf["eventhubs.consumerGroup"] = consumer_group
  return conf


# COMMAND ----------

def read_stream(eventhub_conf, stream_name): #, checkpoint_path, storage_path):
  read_df = (
    spark
      .readStream
      .format("eventhubs")
      .options(**eventhub_conf)
      .load()
      .withColumn("body", col("body").cast("string"))
  )
  return read_df
    

# COMMAND ----------


from pyspark.sql.types import *
from pyspark.sql.functions import *


eh_raw_con = "Endpoint=sb://ite-mad-eventhub.servicebus.windows.net/;SharedAccessKeyName=listen;SharedAccessKey=RvfZn2tVJQQBwmQ1+JiiW6BbWsGces1BcfZJ1DFFe18=;EntityPath=databricks-workshop"

consumer_group = "databricks-ws"

eh_conf = create_eventhub_config(eh_raw_con, consumer_group)


# COMMAND ----------

r = read_stream(eh_conf, "my_stream", )

# COMMAND ----------

r.display()
