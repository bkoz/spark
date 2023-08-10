#
# A simple Kubernetes PySpark job that computes Pi.
#
import os
import socket
from pyspark import SparkConf
from pyspark.sql import SparkSession
from random import random
from operator import add
import time

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

# Initialize the Spark cluster. This will create the executor pods.
spark = SparkSession.builder.config(conf=sparkConf).getOrCreate()
sc = spark.sparkContext

#
# Create a Spark job that computes Pi using the Monte Carlo method.
#
partitions = 7
n = 10000000 * partitions


def f(_):
    """
    The point in circle of radius = 1 test.
    """
    x = random() * 2 - 1
    y = random() * 2 - 1
    return 1 if x ** 2 + y ** 2 <= 1 else 0


t0 = time.time()
count = sc.parallelize(range(1, n + 1), partitions).map(f).reduce(add)
elapsed = time.time() - t0
print(f"=> Elapsed time = {elapsed:.3f} secs. Pi ~ {4.0 * count / n}")

sc.stop()
