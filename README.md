# Rubrik Data Enrichment

This repository contains instructions and examples to begin using Rubrik's API to gain information about workloads protected by Rubrik.

## Setup
  - To Authenticate to the Rubrik API, follow the steps in [Adding a Service Account](https://docs.rubrik.com/en-us/saas/saas/adding_a_service_account.html)
  - Create environment variables for RSC_FQDN, RSC_CLIENT_ID, and RSC_CLIENT_SECRET using the service account
  - NOTE: RSC_FQDN is the FQDN of the RSC instance, NOT the client_token_uri from the service account details.

```bash
export RSC_CLIENT_ID="your-client-id"
export RSC_CLIENT_SECRET="your-client-secret"
export RSC_FQDN="https://YOUR_INSTANCE.my.rubrik.com"
```

`setup.sh` will create a python environment and install the required python modules needed for all the examples in this repo.

Run the following to set up the python environment:
```bash
chmod +x setup.sh
./setup.sh
```

## Queries
The queries folder contains GraphQL queries to retrieve information from Rubrik.

 - `protectedObjects.gql` uses the `snappableConnection` query to retrieve the protectable objects in Rubrik. It is currently set to filter on VMware Virtual Machines, but this filter can be removed if needed. The `snappableConnection` query can retrieve the protection status, policy (SLA Domain), usage, last backup time, and compliance status with its assigned SLA.

 - `vSphereVirtualMachines.gql` uses the `vsphereVmNewConnection` query to retrieve all VMware virtual machines known by Rubrik. It is set up to retrieve the datastore and the logical path of the VM (vSphere Cluster, etc)

## Executing the queries using rsc.py

```python
import rsc
# The client will use the credentials from the environment variables created in the setup instructions.
rsc_client = rsc.Client()
result = rsc_client.invoke("queries/protectedObjects.gql")
print(result)
```

example output:
```python
[{'name': 'sh1-mysql-2', 'id': 'VirtualMachine:::c56905a2-dee0-41e0-8810-b3ef3ebd957f-vm-137482', 'objectType': 'VmwareVirtualMachine', 'lastSnapshot': '2025-01-24T20:12:57.000Z', 'slaDomain': {'name': '12hr-30d-AWS_sh1-PaloAlto'}}, {'name': 'sh1-mysql-2-old', 'id': 'VirtualMachine:::c56905a2-dee0-41e0-8810-b3ef3ebd957f-vm-3368', 'objectType': 'VmwareVirtualMachine', 'lastSnapshot': '2023-08-23T19:15:06.000Z', 'slaDomain': {'name': 'Do Not Protect'}}, {'name': 'sh1-ncd-01', 'id': 'VirtualMachine:::c56905a2-dee0-41e0-8810-b3ef3ebd957f-vm-86449', 'objectType': 'VmwareVirtualMachine', 'lastSnapshot': '2024-11-15T13:11:45.000Z', 'slaDomain': {'name': 'Unprotected'}}, {'name': 'sh1-ncd-02', 'id': 'VirtualMachine:::c56905a2-dee0-41e0-8810-b3ef3ebd957f-vm-88210', 'objectType': 'VmwareVirtualMachine', 'lastSnapshot': '2024-05-24T04:40:52.000Z', 'slaDomain': {'name': 'Do Not Protect'}}]
```

## Running the Flask example
Included in this repo is a Python Flask app that uses `rsc.py` and `protectedObjects.gql` to plot lastSnapshot times on a scatter plot. 

To run the example using `run.sh`:
```bash
chmod +x run.sh
./run.sh
```

Flask will start a web server and run at `https://localhost:5000`