# Databricks notebook source
# MAGIC %md 
# MAGIC ## Eventhub Config

# COMMAND ----------

your_name = "fill-in-you-name"
eh_connection_string = "Endpoint=sb://ite-mad-eventhub.servicebus.windows.net/;SharedAccessKeyName=listen;SharedAccessKey=RvfZn2tVJQQBwmQ1+JiiW6BbWsGces1BcfZJ1DFFe18=;EntityPath=databricks-workshop"
consumergroup = your_name

eventhub_config = {}
# Create a eventhub configuration dictionairy

# COMMAND ----------

# MAGIC %md
# MAGIC ## Storage Config

# COMMAND ----------


path = '{0}/userdata/'.format(your_name)

bronze_mount_point = "/mnt/db-ws-lake/bronze"
bronze_checkpoint_path = "{0}/{1}.checkpoint".format(bronze_mount_point, path)
bronze_storage_path = "{0}/{1}.delta".format(bronze_mount_point, path)


silver_mount_point = "/mnt/db-ws-lake/silver"
silver_checkpoint_path = "{0}/{1}.checkpoint".format(silver_mount_point, path)
silver_storage_path = "{0}/{1}.delta".format(silver_mount_point, path)

gold_mount_point = "/mnt/db-ws-lake/silver"
gold_checkpoint_path = "{0}/{1}.checkpoint".format(gold_mount_point, path)
gold_storage_path = "{0}/{1}.delta".format(gold_mount_point, path)

bronze_table_name = "users_bronze"
silver_table_name = "users_silver"
gold_table_name = "users_gold"

# COMMAND ----------

# MAGIC %md 
# MAGIC ## Tasks
# MAGIC 
# MAGIC ### Eventhub To Bronze
# MAGIC 1. Create an eventhub configuration dictionairy
# MAGIC 2. Read the eventhub as a stream to the bronze container
# MAGIC 3. Create a Delta Table over the bronze data folder called 'bronze_table_name'
# MAGIC 
# MAGIC ### Bronze To Silver
# MAGIC 1. Read the bronze table as a stream
# MAGIC 2. deserialize the data into a clean and structured data format
# MAGIC 3. apply transformation function on columns you would like to alter (e.g. Ssn -> Age and Gender)
# MAGIC 4. store the stream into the silver storage
# MAGIC 5. Create a Delta Table over the silver data folder called 'silver_table_name'
# MAGIC 
# MAGIC ### Silver To Gold (Optional as we have a very small data set)
# MAGIC 1. Read the silver table as a stream
# MAGIC 2. find any aggregation or grouping you find interesting
# MAGIC 4. create some aggregate or business (e.g. bucket on age, or last name)
# MAGIC 5. store the stream into the gold storage
# MAGIC 6. Create a Delta Table over the gold data folder called 'gold_table_name'
