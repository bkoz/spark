#
# Read a DeltaTable from hdfs.
#
# Python config:
#
# pip install pip -Uq
# pip install pyspark==3.4.1 delta-spark==2.4.0 elasticsearch -q
#
# certifi==2023.7.22
# delta-spark==2.4.0
# elastic-transport==8.4.0
# elasticsearch==8.9.0
# importlib-metadata==6.8.0
# numpy==1.25.2
# pandas==2.0.3
# py4j==0.10.9.7
# pyspark==3.4.1
# python-dateutil==2.8.2
# pytz==2023.3
# six==1.16.0
# tzdata==2023.3
# urllib3==1.26.16
# zipp==3.16.2
#
# https://docs.delta.io/latest/api/python/index.html
#

from pyspark.sql import SparkSession
from pyspark import SparkConf
from pyspark.sql.functions import col
from delta.tables import DeltaTable
from elasticsearch import Elasticsearch, helpers
import csv
import os
import socket

# Populate some variables that will be useful later on.
hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)

with open('/var/run/secrets/kubernetes.io/serviceaccount/namespace', 'r') as f:
    current_namespace = f.readline()

print(f'=> Namespace = {current_namespace}')

# Create Spark config for our Kubernetes based cluster manager
sparkConf = SparkConf()

# Kubernetes and image settings
sparkConf.setMaster("k8s://https://" + os.environ["KUBERNETES_SERVICE_HOST"] + ":443")
sparkConf.set("spark.submit.deployMode", "client")
sparkConf.set("spark.kubernetes.container.image", "quay.io/opendatahub-contrib/pyspark:s3.3.1-h3.3.4_v0.1.1")
sparkConf.set("spark.pyspark.python", "3")
sparkConf.set("spark.pyspark.driver.python", "3")
sparkConf.set("spark.kubernetes.namespace", current_namespace)
sparkConf.set("spark.driver.blockManager.port", "7777")
sparkConf.set("spark.driver.host", IPAddr)
sparkConf.set("spark.driver.port", "2222")
sparkConf.set("spark.driver.bindAddress", "0.0.0.0")

#
# Executors configuration
#
# The target Kubernetes cluster must be able to
# provide the resources requested or the executors
# will not get scheduled.
#
sparkConf.set("spark.executor.instances", "1")
sparkConf.set("spark.executor.memory", "512m")
sparkConf.set("spark.executor.cores", "1")

# Initialize Spark Session
spark = SparkSession.builder \
    .appName("KafkaSparkDeltaElasticAutoEncoder") \
    .config("spark.jars.packages", "io.delta:delta-core_2.12:2.4.0") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
    .getOrCreate()

#
# Replace with your hdfs endpoint
#
delta_path = "hdfs://my_hdfsf900.domain.org/my_delta_table"

# Load Delta table from the specified path # loop here
delta_table = DeltaTable.forPath(spark, delta_path)
print()
print(f'==> isDeltaTable : {DeltaTable.isDeltaTable(spark, delta_path)}')
print(f'==> detail = {delta_table.detail()}')
# dfc = delta_table.to_dataframe().limit(1500) #sample or limit pickup size
dfc = delta_table.toDF()
print(f'==> count() = {dfc.count()} rows')
print(f'==> head(5) = {dfc.head(5)}')
print(f'==> Saving csv ...')
dfc.write.csv('./overheating-csv')
print(f'==> Finished.')
# print(f'dfc.show(): {dfc.show()}')
# dfc.to_csv('./overheating.csv', header=True, separator=',')
