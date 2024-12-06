"""
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
"""
import base64
import logging
import requests
import urllib3
from bits_aviso_python_sdk.helpers import resolve_dns

# suppress InsecureRequestWarning
urllib3.disable_warnings(category=urllib3.exceptions.InsecureRequestWarning)


class Isilon:
    """Class to interact with the Isilon PowerScale API."""

    def __init__(self, username, password, clusters=None, platform_api_version='15', dns_resolve=False,
            dns_server=None):
        """Initializes the Isilon class.

        Args:
            username (str): The username to authenticate with.
            password (str): The password to authenticate with.
            clusters (list): A list containing cluster names. Defaults to None.
            platform_api_version (str, optional): The version of the Isilon API to use. Defaults to '15'.
            dns_resolve (bool, optional): Whether to resolve the DNS. Defaults to False.
            dns_server (str, optional): The DNS server to use for resolution. Defaults to None.
        """
        self.clusters = clusters
        self.headers = {'Authorization': f'Basic {self._encode_credentials(username, password)}'}
        self.platform_api_version = platform_api_version
        self.dns_resolve = dns_resolve
        self.dns_server = dns_server

    @staticmethod
    def _encode_credentials(username, password):
        """Encodes the username and password for use in the API.

        Args:
            username (str): The username to authenticate with.
            password (str): The password to authenticate with.

        Returns:
            str: The encoded credentials.
        """
        return base64.b64encode(f'{username}:{password}'.encode()).decode()

    def build_url(self, cluster, api_endpoint=None):
        """Builds the URL for the given Isilon cluster with no trailing slash. If an API endpoint is provided,
        it will be appended to the URL.

        Args:
            cluster (str, optional): The cluster name.
            api_endpoint (str, optional): The path to the API endpoint. Defaults to None.

        Returns:
            str: The URL for the Isilon API. If DNS resolution fails, None is returned.
        """
        # check if dns resolution is needed
        if self.dns_resolve:
            try:
                cluster_domain = f'{cluster}.broadinstitute.org'
                cluster = resolve_dns(cluster_domain, dns_server=self.dns_server)
                if not cluster:
                    raise ValueError

            except ValueError:
                logging.error(f'Failed to resolve the DNS for {cluster}.')
                return

        if api_endpoint:  # check if an API endpoint is provided
            if api_endpoint.startswith('/'):  # check for a leading slash
                api_endpoint = api_endpoint[1:]  # remove the leading slash bc imma put it MYSELF

            # return the URL with the API endpoint
            return f'https://{cluster}:8080/platform/{self.platform_api_version}/{api_endpoint}'

        else:
            return f'https://{cluster}:8080/platform/{self.platform_api_version}'

    def get_all_quotas(self, clusters=None):
        """Gets the quotas for all clusters.

        Args:
            clusters (list, optional): A list containing the cluster names. Defaults to None.

        Returns:
            list[dict], dict: The quotas for all clusters and error payload if any.
        """
        all_quotas = []
        error_payload = {}

        # if no clusters are provided, use the clusters from the class
        if not clusters:
            if self.clusters:
                clusters = self.clusters
            else:
                error_payload['Error'] = 'No clusters provided. Unable to get any quotas.'
                return [], error_payload

        for cluster in clusters:  # get the name and ip of each cluster
            cluster_quota, error_payload = self.get_quotas_for_cluster(cluster)
            if cluster_quota:
                all_quotas.extend(cluster_quota)

            elif error_payload:
                error_payload.update(cluster_quota)

            else:
                error_payload['Error'] = f'Failed to get quota data for the cluster {cluster}.'

        return all_quotas, error_payload

    def get_all_network_pools(self, clusters=None):
        """Gets the network pools for all clusters.

        Args:
            clusters (dict, optional): A dictionary containing the cluster name as key and IP as value.
                Defaults to None.

        Returns:
            list[dict], dict: The network pools for all clusters and error payload if any.
        """
        all_network_pools = []
        error_payload = {}

        # if no clusters are provided, use the clusters from the class
        if not clusters:
            if self.clusters:
                clusters = self.clusters
            else:
                error_payload['Error'] = 'No clusters provided. Unable to get any network pools.'
                return [], error_payload

        for cluster in clusters:
            cluster_network_pools, error_payload = self.get_network_pools_for_cluster(cluster)
            if cluster_network_pools:
                all_network_pools.extend(cluster_network_pools)

            elif error_payload:
                error_payload.update(cluster_network_pools)

            else:
                error_payload['Error'] = f'Failed to get network pool data for the cluster {cluster}.'

        return all_network_pools, error_payload

    def get_network_pools_for_cluster(self, cluster_name):
        """Gets the network pools for the given cluster.

        Args:
            cluster_name (str): The cluster's name.

        Returns:
            list[dict], dict: The network pool data for the cluster and error payload if any.
        """
        # build the url
        url = self.build_url(cluster_name, api_endpoint='/network/pools')

        # get the network pool data
        network_pools = []
        try:
            response = requests.get(url, headers=self.headers, verify=False)
            response.raise_for_status()
            network_pool_data = response.json().get('pools', {})
            if not network_pool_data:
                raise ValueError(f'No network pools found for {cluster_name}.')

            # add the cluster name to the data
            for np in network_pool_data:
                np['cluster'] = cluster_name
                network_pools.append(np)

            # return the network pool data
            return network_pools, {}

        except (requests.exceptions.RequestException, ValueError) as e:
            err_msg = f'Failed to get network pools for {cluster_name}.\nException Message: {e}'
            logging.error(err_msg)
            return [], {"Error": err_msg}

    def get_quota_data(self, cluster_name, path, list_of_quotas=None):
        """Gets the quota data for the given path.
        If a list of quotas is provided, it will be used instead of fetching the quotas from the cluster.

        Args:
            cluster_name (str): The cluster's name.
            path (str): The path to get the quota data for.
            list_of_quotas (list[dict], optional): The list of quotas to search through. Defaults to None.

        Returns:
            dict, dict: The quota data for the path and error payload if any.
        """
        if list_of_quotas:  # if a list of quotas is provided, use it
            quotas = list_of_quotas

        else:  # if not, get the quota data for the cluster
            quotas, error_payload = self.get_quotas_for_cluster(cluster_name)

            # check if there are any quotas
            if not quotas:
                return {}, error_payload

        # find the quota data for the path
        for quota in quotas:
            if quota.get('path') == path:
                return quota, {}

        return {}, {"Error": f'No quota data found for the path {path}'}

    def get_quota_id(self, cluster_name, path, list_of_quotas=None):
        """Gets the quota id for the given path.
        If a list of quotas is provided, it will be used instead of fetching the quotas from the cluster.

        Args:
            cluster_name (str): The cluster's name.
            path (str): The path to get the quota id for.
            list_of_quotas (list[dict], optional): The list of quotas to search through. Defaults to None.

        Returns:
            str, dict: The quota id for the path and error payload if any.
        """
        if list_of_quotas:  # if a list of quotas is provided, use it
            quotas = list_of_quotas

        else:  # if not, get the quota data for the cluster
            quotas, error_payload = self.get_quotas_for_cluster(cluster_name)

            # check if there are any quotas
            if not quotas:
                return '', error_payload

        # find the quota id for the path
        for quota in quotas:
            if quota.get('path') == path:
                return quota.get('id'), {}

        return '', {"Error": f'No quota id found for the path {path}'}

    def get_quotas_for_cluster(self, cluster_name):
        """Gets the quotas for the given cluster.

        Args:
            cluster_name (str): The cluster's name.

        Returns:
            list[dict], dict: The quota data for the cluster and error payload if any.
        """
        # build the url
        url = self.build_url(cluster_name, api_endpoint='/quota/quotas')

        # get the quota data
        quotas = []
        try:
            # check if the url was built successfully
            if not url:
                raise ValueError(f'Failed to build the URL for {cluster_name}')

            # get the quota data
            response = requests.get(url, headers=self.headers, verify=False)
            response.raise_for_status()
            quota_data = response.json().get('quotas', {})

            # check if there are any quotas
            if not quota_data:
                raise ValueError(f'No quotas found for {cluster_name}')

            # add the cluster name to the data
            for quota in quota_data:
                quota['cluster'] = cluster_name
                quotas.append(quota)

            # return the quota data
            return quotas, {}

        except (requests.exceptions.RequestException, ValueError) as e:
            err_msg = f'Failed to get quota for {cluster_name}. \nException Message: {e}'
            logging.error(err_msg)
            return [], {"Error": err_msg}

    def update_quota(self, cluster_name, quota_id, **kwargs):
        """Updates the quota data for the given quota id.

        Args:
            cluster_name (str): The cluster's name.
            quota_id (str): The id of the quota to update.
            **kwargs: The quota data to update. The key should be the field to update and the value should the value.

        Returns:
            bool, dict: True if the quota was updated successfully and error payload if any.
        """
        # build the url
        url = self.build_url(cluster_name, '/quota/quotas') + f'/{quota_id}'

        # parse the kwargs into a payload
        payload = {}
        for key, value in kwargs.items():
            payload[key] = value

        try:
            # check if the url was built successfully
            if not url:
                raise ValueError(f'Failed to build the URL for {cluster_name}')

            # update the quota data
            response = requests.put(url, headers=self.headers, verify=False, json=payload)
            response.raise_for_status()
            return True, {}

        except (requests.exceptions.RequestException, ValueError) as e:
            err_msg = (f'Failed to update quota for {quota_id}. Cluster: {cluster_name}\n'
                       f'Exception Message: {e}')
            logging.error(err_msg)
            return {}, {"Error": err_msg}
