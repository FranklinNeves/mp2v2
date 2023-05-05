from kubernetes import client, config
from flask import Flask,request
from os import path
import yaml, random, string, json
import sys
import json

# Configs can be set in Configuration class directly or using helper utility
config.load_kube_config()
v1 = client.CoreV1Api()
batch_v1 = client.BatchV1Api()
app = Flask(__name__)
# app.run(debug = True)

@app.route('/config', methods=['GET'])
def get_config():
    pods = []

    # your code here
    ret = v1.list_pod_for_all_namespaces(watch=False)
    for item in ret.items:
        currentPod = dict()
        currentPod["node"] = item.spec.node_name
        currentPod["ip"] = item.status.pod_ip
        currentPod["namespace"] = item.metadata.namespace
        currentPod["name"] = item.metadata.name
        currentPod["status"] = item.status.phase
        pods.append(currentPod)

    output = {"pods": pods}
    output = json.dumps(output)

    return output

@app.route('/img-classification/free',methods=['POST'])
def post_free():
    # your code here
    create_quota()
    job = create_job_object("free-service-job", "mnist ", "cnn")
    api_response = batch_v1.create_namespaced_job(
        body=job,
        namespace="free-service")

    return "success"


@app.route('/img-classification/premium', methods=['POST'])
def post_premium():
    # your code here
    job = create_job_object("premium-job", "kmnist", "cnn")
    api_response = batch_v1.create_namespaced_job(
        body=job,
        namespace="default")
    client.V1Job
    client.V1JobStatus

    return "success"

def create_quota():
    resource_quota = client.V1ResourceQuota(
        spec = client.V1ResourceQuotaSpec(
            hard={"requests.cpu": "0.9", "requests.memory": "1Gi", "limits.cpu": "2", "limits.memory": "2Gi", "requests.storage": "1Gi", "services.nodeports": "0"}))
    resource_quota.metadata = client.V1ObjectMeta(namespace="free-service", name="free-service-quota")
    v1.create_namespaced_resource_quota("free-service", resource_quota)



def create_job_object(JOB_NAME, dataSetParam, typeParam):
    # Configurate Pod template container
    limits, requests = {}, {}
    limits["cpu"] = "0.9"
    requests["cpu"] = "0.9"
    resource_requirements = client.V1ResourceRequirements(limits=limits, requests=requests)

    container = client.V1Container(
        name=JOB_NAME,
        image="nevesfranklin/mp12:1.0",
        env=[client.V1EnvVar(name="DATASET", value=dataSetParam), client.V1EnvVar(name="TYPE", value=typeParam)],
        resources=resource_requirements
        )
    # Create and configure a spec section
    template = client.V1PodTemplateSpec(
        metadata=client.V1ObjectMeta(labels={"app": "pi"}),
        spec=client.V1PodSpec(restart_policy="Never", containers=[container]))
    # Create the specification of deployment
    spec = client.V1JobSpec(
        template=template,
        backoff_limit=4)
    # Instantiate the job object
    job = client.V1Job(
        api_version="batch/v1",
        kind="Job",
        metadata=client.V1ObjectMeta(name=JOB_NAME),
        spec=spec)

    return job

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000)
