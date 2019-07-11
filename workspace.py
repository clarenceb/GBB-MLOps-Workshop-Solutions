# Connect to an existing AzureML Workspace

import os, sys

from azureml.core import Workspace
from azureml.core.authentication import AzureCliAuthentication

subscription_id = os.getenv("SUBSCRIPTION_ID", default="<my-subscription-id>")
resource_group = os.getenv("RESOURCE_GROUP", default="<my-resource-group>")
workspace_name = os.getenv("WORKSPACE_NAME", default="<my-workspace-name>")
workspace_region = os.getenv("WORKSPACE_REGION", default="australiaeast")

try:
    cli_auth = AzureCliAuthentication()
    ws = Workspace.get(name=workspace_name,
                       subscription_id=subscription_id,
                       resource_group=resource_group,
                       auth=cli_auth)
except Exception as e:
    print("Workspace not accessible.")
    print(e)
    sys.exit(1)

# Persist config for subsequent steps to use
ws.write_config()
print(ws.name, ws.resource_group, ws.location, ws.subscription_id, sep="\n")
