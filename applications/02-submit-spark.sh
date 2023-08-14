#!/bin/bash

export MASTER=$(oc whoami --show-server)
echo "MASTER = ${MASTER}"

spark-submit \
    --verbose \
    --master k8s://${MASTER} \
    --deploy-mode cluster \
    --name spark-pi \
    --class org.apache.spark.examples.SparkPi \
    --conf spark.executor.instances=1 \
    --conf spark.kubernetes.authenticate.driver.serviceAccountName=spark-service-account \
    --conf spark.kubernetes.authenticate.executor.serviceAccountName=spark-service-account \
    --conf spark.kubernetes.namespace=bkoz-devspaces \
    --conf spark.kubernetes.container.image=gcr.io/spark-operator/spark-py:v3.1.1 \
    local:///opt/spark/examples/src/main/python/pi.py 1000
