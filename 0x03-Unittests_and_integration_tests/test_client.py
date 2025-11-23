#!/usr/bin/env python3
"""
Unit tests and integration tests for GithubOrgClient
"""

import unittest
from unittest.mock import Mock, patch, PropertyMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """Test cases for GithubOrgClient class"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns the correct value"""
        # Set up mock return value
        mock_get_json.return_value = {"login": org_name, "id": 12345}
        
        # Create client instance and call method
        client = GithubOrgClient(org_name)
        result = client.org
        
        # Assertions
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )
        self.assertEqual(result, {"login": org_name, "id": 12345})

    def test_public_repos_url(self):
        """Test that _public_repos_url returns the correct value"""
        # Mock payload for org
        expected_payload = {
            "repos_url": "https://api.github.com/orgs/testorg/repos"
        }
        
        # Patch the org property to return our mock payload
        with patch.object(
            GithubOrgClient, 
            'org', 
            new_callable=PropertyMock, 
            return_value=expected_payload
        ):
            client = GithubOrgClient("testorg")
            result = client._public_repos_url
            
            self.assertEqual(result, "https://api.github.com/orgs/testorg/repos")

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test that public_repos returns the correct list of repos"""
        # Mock payload for repos
        mock_repos_payload = [
            {"name": "repo1", "license": {"key": "mit"}},
            {"name": "repo2", "license": {"key": "apache-2.0"}},
            {"name": "repo3", "license": None},
        ]
        mock_get_json.return_value = mock_repos_payload
        
        # Mock the _public_repos_url property
        with patch.object(
            GithubOrgClient,
            '_public_repos_url',
            new_callable=PropertyMock,
            return_value="https://api.github.com/orgs/testorg/repos"
        ):
            client = GithubOrgClient("testorg")
            
            # Test without license filter
            repos = client.public_repos()
            expected_repos = ["repo1", "repo2", "repo3"]
            self.assertEqual(repos, expected_repos)
            
            # Test with license filter
            repos_with_license = client.public_repos(license="mit")
            expected_repos_with_license = ["repo1"]
            self.assertEqual(repos_with_license, expected_repos_with_license)
            
            # Verify mocks were called
            mock_get_json.assert_called_once_with(
                "https://api.github.com/orgs/testorg/repos"
            )

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
        ({}, "my_license", False),
        ({"license": None}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test that has_license returns the correct boolean value"""
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)


@parameterized_class([
    {
        'org_payload': TEST_PAYLOAD[0][0],
        'repos_payload': TEST_PAYLOAD[0][1],
        'expected_repos': TEST_PAYLOAD[0][2],
        'apache2_repos': TEST_PAYLOAD[0][3],
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient"""

    @classmethod
    def setUpClass(cls):
        """Set up class fixtures before running tests"""
        cls.get_patcher = patch('client.get_json')
        cls.mock_get_json = cls.get_patcher.start()
        
        # Configure side_effect to return different payloads based on URL
        def side_effect(url):
            if url == "https://api.github.com/orgs/google":
                return cls.org_payload
            elif url == cls.org_payload["repos_url"]:
                return cls.repos_payload
            return None
        
        cls.mock_get_json.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop the patcher after all tests"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Integration test for public_repos method"""
        client = GithubOrgClient("google")
        repos = client.public_repos()
        self.assertEqual(repos, self.expected_repos)

    def test_public_repos_with_license(self):
        """Integration test for public_repos with license filter"""
        client = GithubOrgClient("google")
        repos = client.public_repos(license="apache-2.0")
        self.assertEqual(repos, self.apache2_repos)


if __name__ == '__main__':
    unittest.main()