# GBB MLOps Workshop Solutions

## Overview

**This repository should remain private as it's not for participants to see.**

Use this repository for solutions files, scripts, utilities, additional notes for the [GBB-MLOps-Workshop](https://github.com/clarenceb/GBB-MLOps-Workshop).

## Resources

* [Slide deck](https://microsoft-my.sharepoint.com/:p:/p/clbakirt/ESuhM9B18wxOuVya5Pkbxy4B0CPy1_FvmIsRAyYF8lgFgw?e=inh7Os) for workshop
* Workshop [repo](https://github.com/clarenceb/GBB-MLOps-Workshop) for attendees

## Solution notes

### Attach to existing AKS cluster

```sh
#!/bin/bash
source workspace-env.sh
python workspace.py
python attach_cluster.py
```

After attach to new cluster (basic networking), the following objects will be installed:

```sh
(dogbreeds) C:\Users\clbakirt\dev\azureml\dogbreeds\GBB-MLOps-Workshop\solution>kubectl get pod,svc,deploy                                                                                NAME                              READY     STATUS    RESTARTS   AGE                                                                                                                      pod/azureml-ba-5d4d4cd886-5znf9   1/1       Running   0          4m                                                                                                                       pod/azureml-fe-65b7486dd9-l8tkw   2/2       Running   1          10m                                                                                                                                                                                                                                                                                                                NAME                          TYPE           CLUSTER-IP    EXTERNAL-IP     PORT(S)                      AGE                                                                               service/azureml-fe            LoadBalancer   10.0.84.138   <service_ip>   80:32103/TCP,443:31716/TCP   10m                                                                               service/azureml-fe-int-http   ClusterIP      10.0.34.191   <none>          9001/TCP                     10m                                                                               service/kubernetes            ClusterIP      10.0.0.1      <none>          443/TCP                      2h                                                                                                                                                                                                                                                                          NAME                               DESIRED   CURRENT   UP-TO-DATE   AVAILABLE   AGE                                                                                                       deployment.extensions/azureml-ba   1         1         1            1           4m                                                                                                        deployment.extensions/azureml-fe   1         1         1            1           10m                               
```

**Service**:
- Load balancer endpoint with public IP

**Deployment**:
- You get a billing agent (*not sure what this is for exactly*)
- Front end reverse proxy

### Deploy ML model as a WebService

```sh
python deploy_svc.py dogbreeds-aks dogbreedsvc 1 dogbreeds-aks
```

After deploying service, the following objects are created in a namespace `azureml-<workspace_lowercased>`:

```sh
kubectl get svc,deploy,pod -n azureml-dogbreeds                                                           NAME                    TYPE       CLUSTER-IP    EXTERNAL-IP   PORT(S)        AGE                                                                                                         service/dogbreeds-aks   NodePort   10.0.86.146   <none>        80:30916/TCP   16m                                                                                                                                                                                                                                                                                                   NAME                                  DESIRED   CURRENT   UP-TO-DATE   AVAILABLE   AGE                                                                                                    deployment.extensions/dogbreeds-aks   1         1         1            1           16m                                                                                                                                                                                                                                                                                              NAME                                 READY     STATUS    RESTARTS   AGE                                                                                                                   pod/dogbreeds-aks-5959b6f995-dfw6v   1/1       Running   0          16m 
```

### Test the WebService

```sh
python test_svc.py http://<service_ip>/api/v1/service/dogbreeds-aks/score ..\breeds-10\val\n02091032-Italian_greyhound\n02091032_8093.jpg niaL0ME9iWIJ2G04YXIexiX6kHz1ojD7
```

Result:

```json
{"label": "Italian_greyhound", "probability": "0.9723086"}
```
