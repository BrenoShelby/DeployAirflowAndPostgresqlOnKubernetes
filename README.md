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
helm install airflow apache-airflow/airflow --namespace airflow --debug --timeout 10m0s
```
7. Check the pods on namespace airflow
```
kubectl get pods -n airflow
```
8. Get the settings values from helm chart Airflow as values.yaml
```
helm show values apache-airflow/airflow > values.yaml
```
9. Open the port 8080:8080
```
kubectl port-forward svc/airflow-webserver 8080:8080 -n airflow --context minikube
```

### Postgresql

1. Access the airflow-postgres
```
kubectl exec -it airflow-postgresql-0 bash -n airflow
```
2. Now, access the Postgres terminal
```
psql -U postgres
```
3. Create the schema
```
CREATE SCHEMA bigquery;
```
4. Create the table
```
CREATE TABLE bigquery.tokens (
            address BIGINT, 
            symbol VARCHAR(5), 
            name VARCHAR(20), 
            decimals BIGINT, 
            total_supply BIGINT, 
            block_timestamp TIMESTAMP, 
            block_number BIGINT, 
            block_hash BIGINT
);
```
5. Check the table
```
SELECT * FROM bigquery.tokens;
```

### Configure gitSync

1. Enter in values.yaml that you created before
2. Search for **dags** and paste it.
```
# Git sync
dags:
  persistence:
    # Enable persistent volume for storing dags
    enabled: false
    # Volume size for dags
    size: 1Gi
    # If using a custom storageClass, pass name here
    storageClassName:
    # access mode of the persistent volume
    accessMode: ReadWriteOnce
    ## the name of an existing PVC to use
    existingClaim:
  gitSync:
    enabled: true

    repo: https://github.com/BrenoShelby/DeployAirflowAndPostgresqlOnKubernetes.git
    branch: master
    rev: HEAD
    depth: 1
    maxFailures: 3
    subPath: "dags/"
    wait: 60
    containerName: git-sync
    uid: 65533
    extraVolumeMounts: []
    env: []
    resources: {}
```
3. Save it and type in terminal
```
helm upgrade --install airflow apache-airflow/airflow -f values.yaml -n airflow --debug
```