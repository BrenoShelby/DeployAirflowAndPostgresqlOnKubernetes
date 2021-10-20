# Deploy Airflow and Postgresql on Kubernetes

## Requirements

- Minikube
- Kubectl
- Helm
- Docker

## Set up the environment

### Airflow

1. Start up the Minikube node.
```
minikube start
```
2. Check the cluster info
```
kubectl cluster-info
```
3. Add the official repository of the Apache Airflow Helm Chart
```
helm repo add apache-airflow https://airflow.apache.org
``` 
4. Update the Helm
```
helm repo update
```
5. Create a namespace to Airflow
```
kubectl create namespace airflow
```
6. Install the Airflow Helm Chart
```
helm install airflow apache-airflow/airflow --namespace airflow --debug --timeout 15m0s
```
7. Check the pods on namespace airflow
```
kubectl get pods -n airflow
```
8. Get the settings values from helm chart Airflow as values.yaml
```
helm show values apache-airflow/airflow > values.yaml
```

### Postgresql

1. Add the repository of the Postgresql
```
helm repo add bitnami https://charts.bitnami.com/bitnami
```
2. Create a namespace to Postgresql
```
helm create namespace postgresql
```
3. Install the Postgresql Helm Chart
```
helm install postgresql-dev bitnami/postgresql --namespace postgresql
```
4. Check the installation
```
kubectl get all
```