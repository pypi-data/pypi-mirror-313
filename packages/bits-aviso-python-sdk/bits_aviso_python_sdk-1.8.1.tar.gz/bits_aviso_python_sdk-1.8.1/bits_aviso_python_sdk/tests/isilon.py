import unittest
from unittest.mock import patch, MagicMock
from bits_aviso_python_sdk.helpers.files import write_json
from bits_aviso_python_sdk.services.isilon import Isilon
from bits_aviso_python_sdk.services.google.secretmanager import SecretManager


class TestIsilon(unittest.TestCase):
    """Unit Tests for the Isilon class"""
    def setUp(self):
        """Set up test fixtures. Enter credentials to use."""
        self.secret_manager = SecretManager()
        self.google_project = ''
        self.credentials_secret = ''
        self.clusters_secret = ''
        self.credentials = self.secret_manager.get_secret(self.google_project, self.credentials_secret)
        self.clusters = self.secret_manager.get_secret(self.google_project, self.clusters_secret)
        self.username = self.credentials.get('username')
        self.password = self.credentials.get('password')
        self.isilon = Isilon(self.username, self.password, self.clusters)

    def test_build_url(self):
        """Test the build_url method."""
        cluster_ip = self.clusters.get('iron')
        expected_url = f"https://{cluster_ip}:8080/platform/15/some/endpoint"
        self.assertEqual(self.isilon.build_url(cluster_ip, 'some/endpoint'), expected_url)

    @patch('bits_aviso_python_sdk.services.isilon.requests.get')
    def test_get_quotas_for_cluster(self, mock_get):
        """Test the get_quotas_for_cluster method."""
        cluster_name = 'iron'
        cluster_ip = self.clusters.get(cluster_name)
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "quotas": [
                {
                    "container": True,
                    "efficiency_ratio": 0.8203882132455211,
                    "enforced": True,
                    "id": "NU_3LwEAAAZZZZZZAAAAQAoAAZZZZAAA",
                    "include_snapshots": False,
                    "linked": False,
                    "notifications": "custom",
                    "path": "/test/path/to/somewhere",
                    "persona": "None",
                    "ready": True,
                    "reduction_ratio": 1.000021514880976,
                    "thresholds": {
                        "advisory": 1688842346263936,
                        "advisory_exceeded": False,
                        "advisory_last_exceeded": "None",
                        "hard": 2046612346312723,
                        "hard_exceeded": False,
                        "hard_last_exceeded": "None",
                        "percent_advisory": "None",
                        "percent_soft": "None",
                        "soft": "None",
                        "soft_exceeded": False,
                        "soft_grace": "None",
                        "soft_last_exceeded": "None"
                    },
                    "thresholds_on": "fslogicalsize",
                    "type": "directory",
                    "usage": {
                        "applogical": 912432633811231,
                        "applogical_ready": True,
                        "fslogical": 912681145347068,
                        "fslogical_ready": True,
                        "fsphysical": 1112498543218672,
                        "fsphysical_ready": True,
                        "inodes": 60632562,
                        "inodes_ready": True,
                        "physical": 11523141468672,
                        "physical_data": 912612562693376,
                        "physical_data_ready": True,
                        "physical_protection": 194941568653512,
                        "physical_protection_ready": True,
                        "physical_ready": True,
                        "shadow_refs": 0,
                        "shadow_refs_ready": True
                    }
                },

            ],
            "resume": "None"
        }
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response
        quota_data, error_payload = self.isilon.get_quotas_for_cluster(cluster_name, cluster_ip)
        self.assertEqual(len(quota_data[0]), 16)  # number of keys in a quota
        self.assertEqual(error_payload, {})  # there should be no error payload on a successful run

    @patch('bits_aviso_python_sdk.services.isilon.requests.get')
    def test_get_all_quotas(self, mock_get):
        """Test the get_all_quotas method."""
        mock_response = MagicMock()
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response
        mock_response.json.return_value = {
            "quotas": [
                {
                    "container": True,
                    "efficiency_ratio": 0.8203882132455211,
                    "enforced": True,
                    "id": "NU_3LwEAAAZZZZZZAAAAQAoAAZZZZAAA",
                    "include_snapshots": False,
                    "linked": False,
                    "notifications": "custom",
                    "path": "/test/path/to/somewhere",
                    "persona": "None",
                    "ready": True,
                    "reduction_ratio": 1.000021514880976,
                    "thresholds": {
                        "advisory": 1688842346263936,
                        "advisory_exceeded": False,
                        "advisory_last_exceeded": "None",
                        "hard": 2046612346312723,
                        "hard_exceeded": False,
                        "hard_last_exceeded": "None",
                        "percent_advisory": "None",
                        "percent_soft": "None",
                        "soft": "None",
                        "soft_exceeded": False,
                        "soft_grace": "None",
                        "soft_last_exceeded": "None"
                    },
                    "thresholds_on": "fslogicalsize",
                    "type": "directory",
                    "usage": {
                        "applogical": 912432633811231,
                        "applogical_ready": True,
                        "fslogical": 912681145347068,
                        "fslogical_ready": True,
                        "fsphysical": 1112498543218672,
                        "fsphysical_ready": True,
                        "inodes": 60632562,
                        "inodes_ready": True,
                        "physical": 11523141468672,
                        "physical_data": 912612562693376,
                        "physical_data_ready": True,
                        "physical_protection": 194941568653512,
                        "physical_protection_ready": True,
                        "physical_ready": True,
                        "shadow_refs": 0,
                        "shadow_refs_ready": True
                    }
                },

            ],
            "resume": "None"
        }
        quota_data, error_payload = self.isilon.get_all_quotas()
        # self.assertEqual(len(quota_data), 4602)  # number of quotas. commented out bc this can change any time
        self.assertEqual(len(quota_data[0]), 16)  # number of keys in a quota
        self.assertEqual(error_payload, {})  # there should be no error payload on a successful run


def test():
    """Manually test the Isilon class."""
    secret_manager = SecretManager()
    google_project = ''
    credentials_secret = ''
    clusters_secret = ''
    credentials = secret_manager.get_secret(google_project, credentials_secret)
    clusters = secret_manager.get_secret(google_project, clusters_secret)
    username = credentials.get('username')
    password = credentials.get('password')
    isilon = Isilon(username, password, clusters)
    quota_data, _ = isilon.get_all_quotas()
    write_json(quota_data, 'quota_data.json')
    network_pool_data, _ = isilon.get_all_network_pools()
    write_json(network_pool_data, 'network_pool_data.json')


if __name__ == '__main__':
    test()
