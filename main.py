#!/usr/bin/env python

import requests
import json
import yaml
import schedule
import time
import os

config = None
kubeToken = None
prevScalingUp = True
kubernetesServiceHostUrl = os.environ['KUBERNETES_SERVICE_HOST']
kubernetesPort443TCPPort = os.environ['KUBERNETES_PORT_443_TCP_PORT']
url = 'https://' + kubernetesServiceHostUrl + ':' + kubernetesPort443TCPPort + '/apis/extensions/v1beta1/namespaces/default/deployments/'
verify = "/var/run/secrets/kubernetes.io/serviceaccount/ca.crt"

with open("/var/run/secrets/kubernetes.io/serviceaccount/token", 'r') as f:
    kubeToken = f.read()
headers = {'Content-type': 'application/json', 'Authorization': 'Bearer ' + kubeToken}

with open("config.yml", 'r') as f:
    config = yaml.load(f)

def scaleDeployment(amountInstances):
    global headers
    global verify
    fakeWebserverDeploy = requests.get((url + config["schedule"]["name"]), headers=headers, verify=verify).json()
    print("Scaling to: ", str(amountInstances))
    fakeWebserverDeploy["spec"]["replicas"] = amountInstances
    r = requests.put(url + "fake-webserver/", data=json.dumps(fakeWebserverDeploy), headers=headers, verify=verify)
    print(r.status_code)

def alternateUpDownScaling():
    global prevScalingUp
    if prevScalingUp:
        scaleDeployment(config["schedule"]["low"])
    else:
        scaleDeployment(config["schedule"]["high"])
    prevScalingUp = not prevScalingUp

schedule.every(config["schedule"]["interval"]).seconds.do(alternateUpDownScaling)

while True:
    schedule.run_pending()
    time.sleep(1)
