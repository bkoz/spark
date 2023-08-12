# Pyspark 

## Sample Applications

1) Run the Pyspark SDK example using Openshift DevSpaces

Run the devfile task to build the python environment:

=> View => Command Pallete => Tasks: Run Task

=> Just below + Configure a Task => choose the devfile folder icon

=> devfile: run application

From the file explorer, open the `01-pyspark-pi.py` file. It should
pick up the new python environment (see lower right). Next 
click the `Run` arrow in the upper right to run the program.

2) Deploy a similiar example using a SparkApplication Custom Resource.

=> Terminal => New Terminal

This needs to be tested for a non-cluster-admin user.

Create a service account and grant it admin privs for your namespace.

```
oc create sa spark-service-account
oc adm policy add-role-to-user admin -z spark-service-account
```

- OR

```
oc apply -f applications/00-spark-role.yaml
```

To deploy a simple PySpark application that computes the value of pi.
```
oc apply -f applications/01-pyspark-pi.yaml
``` 

The driver pod and a single executor should be running along with the
operator and helm-operator.
```
oc get pods
```
```
NAME                                                      READY   STATUS    RESTARTS   AGE
pyspark-pi-driver                                         1/1     Running   0          7s
pythonpi-3b511789dbab1045-exec-1                          1/1     Running   0          2s
```

The logs of the pyspark driver pod should indicate the job completed.
```
oc logs pyspark-pi-driver
```
```
23/08/09 19:15:05 INFO DAGScheduler: Job 0 finished: reduce at /opt/spark/examples/src/main/python/pi.py:42, took 101.093822 s
Pi is roughly 3.143160
```

To scale out the application, modify the `executor.instances` key and apply the `applications/01-pyspark-pi.yaml` file again. Your cluster must have enough free cpu cores to support this. Its best to start with `2` and work up from there.
```
  executor:
    instances: 2
```

When the application is submitted, a pod should get scheduled for each executor instance.
```
oc apply -f applications/01-pyspark-pi.yaml
``` 

```
NAME                                                      READY   STATUS    RESTARTS   AGE
pyspark-pi-driver                                         1/1     Running   0          32s
pythonpi-cbfc6489dbc23b32-exec-1                          1/1     Running   0          26s
pythonpi-cbfc6489dbc23b32-exec-2                          1/1     Running   0          26s
```

By using 2 executors the total run time is nearly cut in half as expected.
```
23/08/09 19:25:44 INFO DAGScheduler: Job 0 finished: reduce at /opt/spark/examples/src/main/python/pi.py:42, took 51.578457 s
Pi is roughly 3.145080
```

Submit via `spark-submit`.

Testing this now.

```
bash applications/02-submit-spark.sh
```

[Spark on k8s api docs](https://github.com/GoogleCloudPlatform/spark-on-k8s-operator/blob/master/docs/api-docs.md)
