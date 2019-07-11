# Attaches to an existing AKS cluster for it is useable in the AzureML Workspace for dpeloyments.

import sys
from azureml.core import Workspace
from azureml.core.compute import AksCompute, ComputeTarget
from azureml.core.authentication import AzureCliAuthentication

# Set the resource group that contains the AKS cluster and the cluster name
resource_group = 'DogBreeds'
cluster_name = 'DogBreeds'

# Get a reference the workspace
try:
    cli_auth = AzureCliAuthentication()
    ws = Workspace.from_config(auth=cli_auth)
except Exception as e:
    print("Workspace not accessible.")
    print(e)
    sys.exit(1)

# Attach the cluster to your workgroup. If the cluster has less than 12 virtual CPUs then
# specify: cluster_purpose = AksCompute.ClusterPurpose.DEV_TEST
attach_config = AksCompute.attach_configuration(resource_group = resource_group,
                                         cluster_name = cluster_name,
                                         cluster_purpose = AksCompute.ClusterPurpose.DEV_TEST)
aks_target = ComputeTarget.attach(ws, 'dogbreeds-aks', attach_config)

aks_target.wait_for_completion(show_output = True)
print(aks_target.provisioning_state)
print(aks_target.provisioning_errors)
