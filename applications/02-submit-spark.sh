#!/bin/bash

MASTER=$(oc whoami --show-server)
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
    local:///opt/spark/examples/src/main/python/pi.py

#$ ./bin/spark-submit \
#    --master k8s://https://<k8s-apiserver-host>:<k8s-apiserver-port> \
#    --deploy-mode cluster \
#    --name spark-pi \
#    --class org.apache.spark.examples.SparkPi \
#    --conf spark.executor.instances=5 \
#    --conf spark.kubernetes.container.image=<spark-image> \
#    local:///path/to/examples.jar

#    --conf spark.kubernetes.authenticate.driver.serviceAccountName=spark-service-account \
