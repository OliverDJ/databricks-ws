# Databricks notebook source
# MAGIC %md
# MAGIC ## Eventhub Conf

# COMMAND ----------

from pyspark.sql.types import *
from pyspark.sql.functions import *

eh_connection_string = "Endpoint=sb://ite-mad-eventhub.servicebus.windows.net/;SharedAccessKeyName=listen;SharedAccessKey=RvfZn2tVJQQBwmQ1+JiiW6BbWsGces1BcfZJ1DFFe18=;EntityPath=databricks-workshop"
consumer_group = "databricks-ws"

eventhub_conf = {}
encrypted_connection_string = sc._jvm.org.apache.spark.eventhubs.EventHubsUtils.encrypt(eh_connection_string)
eventhub_conf["eventhubs.connectionString"] = encrypted_connection_string
eventhub_conf["eventhubs.consumerGroup"] = consumer_group

# COMMAND ----------

# MAGIC %md
# MAGIC ## Read Stream

# COMMAND ----------

read_stream =  (
    spark
      .readStream
      .format("eventhubs")
      .options(**eventhub_conf)
      .load()
      .withColumn("body", col("body").cast("string"))
  )

# COMMAND ----------

# MAGIC %md
# MAGIC ## Storage Conf

# COMMAND ----------

path = 'eventhub/userdata'
mount_point = "/mnt/db-ws-lake/bronze"
checkpoint_path = "{0}/{1}.checkpoint".format(mount_point, path)
storage_path = "{0}/{1}.delta".format(mount_point, path)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Write Stream

# COMMAND ----------

r = (
  read_stream
  .writeStream 
        .format("delta") 
        .option("checkpointLocation", checkpoint_path) 
        .outputMode("append") 
        .queryName('stream_name')
        .trigger(once=True)
        .start(storage_path)
)
