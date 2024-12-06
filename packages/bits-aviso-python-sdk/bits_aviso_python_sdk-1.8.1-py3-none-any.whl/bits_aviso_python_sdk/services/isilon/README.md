# Isilon

The `isilon` module provides a set of tools to interact with Isilon clusters using the PowerScale API.
It includes methods to retrieve and update quotas and network pools for the clusters.

---

## Installation

To install the `isilon` module, use `pip`:

```sh
pip install bits_aviso_python_sdk
```

---

## Usage

### Initialization

To use the `isilon` module, you need to initialize the `Isilon` class with the necessary parameters:

```python
from bits_aviso_python_sdk.services.isilon import Isilon

isilon = Isilon(username='username', password='password', clusters=['cluster1', 'cluster2'])
```

### Examples

---

#### Get All Quotas

Retrieve all quotas for all clusters:

```python
all_quotas, errors = isilon.get_all_quotas()
print(all_quotas)
print(errors)
```

---

#### Get All Quotas for a Cluster

Retrieve all quotas in a specific cluster:

```python
quotas, error = isilon.get_quotas_for_cluster('cluster1',)
print(quotas)
print(error)
```

---

#### Update a Specific Quota

Updates a specific quota. The cluster and quota ID must be provided, along with any parameters you wish to update:

```python
updated_quota, error = isilon.update_quota('cluster1', '8380451k3hjkhjasf', description='new quota description')
print(updated_quota)
print(error)
```
See the [Isilon API documentation](https://developer.dell.com/apis/4088/versions/9.5.0/9.5.0.0_ISLANDER_OAS2.json/paths/~1platform~115~1quota~1quotas~1%7Bv15QuotaQuotaId%7D/put) for more details on the available parameters.

---

#### Get Network Pools for All Clusters

Retrieve network pools for all clusters:

```python
all_network_pools, errors = isilon.get_all_network_pools()
print(all_network_pools)
print(errors)
```

---

#### Get Network Pools for a Specific Cluster

Retrieve network pools for a specific cluster:

```python
network_pools, error = isilon.get_network_pools_for_cluster('cluster1')
print(network_pools)
print(error)
```

---


## Error Handling

Each method returns a tuple containing the result and an error payload.
The error payload will contain details if any errors occurred during the execution of the method.

```json
{
    "Error": "An error message will be here."
}
```
---
