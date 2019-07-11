# Deploys an image to the AKS cluster as a WebService.

import argparse, os, sys

from azureml.core import Workspace
from azureml.core.compute import AksCompute, ComputeTarget
from azureml.core.webservice import Webservice, AksWebservice
from azureml.core.image import ContainerImage
from azureml.core.authentication import AzureCliAuthentication

parser = argparse.ArgumentParser()
parser.add_argument("service_name")
parser.add_argument("image_name")
parser.add_argument("image_version")
parser.add_argument("compute_target")
args = parser.parse_args()

# Get a reference the workspace
try:
    cli_auth = AzureCliAuthentication()
    ws = Workspace.from_config(auth=cli_auth)
except Exception as e:
    print("Workspace not accessible.")
    print(e)
    sys.exit(1)

image = ContainerImage(workspace = ws,
                       name = args.image_name,
                       version = args.image_version)

aks_config = AksWebservice.deploy_configuration()
aks_service_name = args.service_name

aks_target = ComputeTarget(ws, args.compute_target)

aks_service = Webservice.deploy_from_image(workspace = ws, 
                                           name = aks_service_name,
                                           image = image,
                                           deployment_config = aks_config,
                                           deployment_target = aks_target)
aks_service.wait_for_deployment(show_output = True)
print(aks_service.state)
