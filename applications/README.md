# Pyspark Sample Applications

To deploy a simple PySpark application that computes the value of pi.
```
oc apply -f applications/01-pyspark-pi.yaml
``` 

The driver pod and a single executor should be running:
```
oc get pods
```
```
NAME                                                      READY   STATUS    RESTARTS   AGE
pyspark-pi-driver                                         1/1     Running   0          7s
pythonpi-3b511789dbab1045-exec-1                          1/1     Running   0          2s
spark-helm-operator-controller-manager-5b75d4bddb-n8hlq   2/2     Running   0          20m
spark-operator-5fbb6f7f67-8hg9s                           1/1     Running   0          20m
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

When the application is submitted, a pod should get scheduled for each instance.
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