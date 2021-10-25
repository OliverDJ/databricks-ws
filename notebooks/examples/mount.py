# Databricks notebook source
def mount_external_storage(source, mount_point, config):
  try:
    dbutils.fs.unmount(mount_point)
    print("unmounted:", mount_point)
  except:
    print("exception!")
    pass
  dbutils.fs.mount(
    source = source,
    mount_point = mount_point,
    extra_configs = config)

# COMMAND ----------

storage_account_name = 'dbwslakedev'
virtual_storage_name = 'db-ws-lake'
storage_account_access_key = 'xvXgNgqW+jFqK/8lRxk5HTHEPmAkEHomexI1lKsrwToV2Uy6/QbgjBKxvypTkbzHw+NF25k8KF3bUCV3xjvi8g=='
# storage_account_access_key = dbutils.secrets.get(scope=secret_scope_name, key='StorageAccountAccessKey')

storage_account_url = "fs.azure.account.key.{0}.blob.core.windows.net".format(storage_account_name)
extra_config = {storage_account_url: storage_account_access_key}

containerNames = ['bronze', 'silver', 'gold']
for container_name in containerNames:
  storage_url = "wasbs://{0}@{1}.blob.core.windows.net/".format(container_name, storage_account_name)
  storage_mount_point = "/mnt/{0}/{1}/".format(virtual_storage_name, container_name)
  mount_external_storage(storage_url, storage_mount_point, extra_config)
