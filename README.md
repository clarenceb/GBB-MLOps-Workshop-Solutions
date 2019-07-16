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
(dogbreeds) C:\Users\clbakirt\dev\azureml\dogbreeds\GBB-MLOps-Workshop\solution>kubectl get pod,svc,deploy
NAME                              READY     STATUS    RESTARTS   AGE
pod/azureml-ba-5d4d4cd886-5znf9   1/1       Running   0          4m
pod/azureml-fe-65b7486dd9-l8tkw   2/2       Running   1          10m

NAME                          TYPE           CLUSTER-IP    EXTERNAL-IP     PORT(S)                      AGE
service/azureml-fe            LoadBalancer   10.0.84.138   <service_ip>   80:32103/TCP,443:31716/TCP    10m
service/azureml-fe-int-http   ClusterIP      10.0.34.191   <none>          9001/TCP                     10m
service/kubernetes            ClusterIP      10.0.0.1      <none>          443/TCP                      2h

NAME                               DESIRED   CURRENT   UP-TO-DATE   AVAILABLE   AGE
deployment.extensions/azureml-ba   1         1         1            1           4m
deployment.extensions/azureml-fe   1         1         1            1           10m
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
kubectl get svc,deploy,pod -n azureml-dogbreeds
NAME                    TYPE       CLUSTER-IP    EXTERNAL-IP   PORT(S)        AGE
service/dogbreeds-aks   NodePort   10.0.86.146   <none>        80:30916/TCP   16m

NAME                                  DESIRED   CURRENT   UP-TO-DATE   AVAILABLE   AGE
deployment.extensions/dogbreeds-aks   1         1         1            1           16m

NAME                                 READY     STATUS    RESTARTS   AGE
pod/dogbreeds-aks-5959b6f995-dfw6v   1/1       Running   0          16m
```

### Test the WebService

```sh
python test_svc.py \
    http://<service_ip>/api/v1/service/dogbreeds-aks/score \
    ..\breeds-10\val\n02091032-Italian_greyhound\n02091032_8093.jpg \
    niaL0ME9iWIJ2G04YXIexiX6kHz1ojD7
```

Result:

```json
{"label": "Italian_greyhound", "probability": "0.9723086"}
```

### Deploying directly to AKS

```sh
kubectl create ns dogbreeds-test
kubectl apply -f dogbreeds.yaml -n dogbreeds-test

curl https://s3.amazonaws.com/cdn-origin-etr.akc.org/wp-content/uploads/2017/11/12213613/Chihuahua-onWhite-13.jpg -o /tmp/dog.jpg

(echo -n '{"data": "'; base64 /tmp/dog.jpg; echo '"}') | curl -sX POST -H "Content-Type: application/json" -d @-  http://<ingress_ip>/dogbreeds/score
```

Clean-up:

```sh
kubectl delete ns dogbreeds-test
```

### Creating a Helm Chart

```sh
helm create dogbreeds-ml
```

Populate the generated files to be similar to the file `dogbreeds.yaml`.

### Deploy the Helm Chart

```sh
kubectl create ns dogbreeds-ml
helm install -n dogbreeds-demo --namespace dogbreeds-ml ./charts/dogbreeds-ml
kubectl get ingress,svc,deploy -n dogbreeds-ml
```

### Test the Helm Chart

Get the Ingress external IP:

```sh
kubectl get service -l app=nginx-ingress --namespace ingress-nginx
```

Test the service:

```sh
curl https://s3.amazonaws.com/cdn-origin-etr.akc.org/wp-content/uploads/2017/11/12213613/Chihuahua-onWhite-13.jpg -o /tmp/dog.jpg
(echo -n '{"data": "'; base64 /tmp/dog.jpg; echo '"}') | curl -sX POST -H "Host: dogbreeds-ml.local" -H "Content-Type: application/json" -d @-  http://<ingress_external_ip>/dogbreeds/score
```
Result:

```json
"{\"label\": \"Chihuahua\", \"probability\": \"0.99925846\"}"
```

**Note**:

* If you [configure a DNS name](https://docs.microsoft.com/en-us/azure/aks/ingress-tls#configure-a-dns-name) for the Ingress external IP then you should update the `ingress.hosts` field in the file `charts/dogbreeds-ml/templates/ingress.yaml` with this FQDN.  You can then omit the header `Host: dogbreeds-ml.local` in your HTTP requests.
* You can also [setup TLS](https://docs.microsoft.com/en-us/azure/aks/ingress-tls#install-cert-manager) on the Ingress using Let's Encrypt and the Cert-Manager Helm chart.  Make sure you updatr the `ingress.tls` field in the file `charts/dogbreeds-ml/templates/ingress.yaml`.

Clean-up:

```sh
helm delete --purge dogbreeds-demo
```
