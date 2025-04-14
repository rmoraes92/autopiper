import unittest
from unittest.mock import patch, mock_open
import os
import shutil

import requests

from autopiper.download_github_release_asset import (
    download_github_release_asset,
)
from autopiper.exceptions import GithubReleaseAssetNotFoundError


class DownloadGitHubReleaseAssetTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Create a temporary directory for testing downloads
        cls.test_output_path = "test_downloads"
        os.makedirs(cls.test_output_path, exist_ok=True)

    @classmethod
    def tearDownClass(cls):
        # Clean up the temporary directory after all tests
        shutil.rmtree(cls.test_output_path)

    def setUp(self):
        # This method is called before each test
        self.owner = "test_owner"
        self.repo = "test_repo"
        self.tag_name = "v1.0"
        self.asset_name = "test_asset.txt"
        self.download_url = "https://example.com/download/test_asset.txt"
        self.api_url = f"https://api.github.com/repos/{self.owner}/{self.repo}/releases/tags/{self.tag_name}"
        self.output_file_path = os.path.join(self.test_output_path, self.asset_name)

    def tearDown(self):
        # This method is called after each test
        if os.path.exists(self.output_file_path):
            os.remove(self.output_file_path)

    @patch("requests.get")
    def test_successful_download(self, mock_get):
        # Mock the API response for release info
        mock_release_response = unittest.mock.Mock()
        mock_release_response.raise_for_status.return_value = None
        mock_release_response.json.return_value = {
            "assets": [{"name": self.asset_name, "url": self.download_url}]
        }
        mock_get.side_effect = [mock_release_response]

        # Mock the download response
        mock_download_response = unittest.mock.Mock()
        mock_download_response.raise_for_status.return_value = None
        mock_download_response.iter_content.return_value = [b"Test content"]
        mock_get.side_effect = [mock_release_response, mock_download_response]

        file_path = download_github_release_asset(
            self.owner,
            self.repo,
            self.tag_name,
            self.asset_name,
            self.test_output_path,
        )

        self.assertTrue(file_path is not None)
        self.assertTrue(os.path.exists(file_path))

        with open(self.output_file_path, "r") as f:
            self.assertEqual(f.read(), "Test content")

    @patch("requests.get")
    def test_asset_not_found(self, mock_get):
        # Mock the API response for release info where the asset is not found
        mock_release_response = unittest.mock.Mock()
        mock_release_response.raise_for_status.return_value = None
        mock_release_response.json.return_value = {"assets": []}
        mock_get.return_value = mock_release_response

        with self.assertRaises(GithubReleaseAssetNotFoundError):
            download_github_release_asset(
                self.owner,
                self.repo,
                self.tag_name,
                self.asset_name,
                self.test_output_path,
            )

    @patch("requests.get")
    def test_release_not_found(self, mock_get):
        # Mock the API response for release info returning a 404 error
        mock_release_response = unittest.mock.Mock()
        mock_release_response.raise_for_status.side_effect = (
            requests.exceptions.HTTPError("Not Found")
        )
        mock_get.return_value = mock_release_response

        with self.assertRaises(requests.exceptions.HTTPError):
            download_github_release_asset(
                self.owner,
                self.repo,
                self.tag_name,
                self.asset_name,
                self.test_output_path,
            )

    @patch("requests.get")
    def test_download_request_error(self, mock_get):
        # Mock the API response for release info
        mock_release_response = unittest.mock.Mock()
        mock_release_response.raise_for_status.return_value = None
        mock_release_response.json.return_value = {
            "assets": [{"name": self.asset_name, "url": self.download_url}]
        }

        # Mock the download response to raise an HTTP error
        mock_download_response = unittest.mock.Mock()
        mock_download_response.raise_for_status.side_effect = (
            requests.exceptions.HTTPError("Download Failed")
        )
        mock_download_response.iter_content.return_value = [b"Test content"]
        mock_get.side_effect = [mock_release_response, mock_download_response]

        with self.assertRaises(requests.exceptions.HTTPError):
            download_github_release_asset(
                self.owner,
                self.repo,
                self.tag_name,
                self.asset_name,
                self.test_output_path,
            )

    @patch("requests.get")
    def test_general_request_exception(self, mock_get):
        # Mock the API response to raise a general RequestException
        mock_get.side_effect = requests.exceptions.RequestException("Network Error")

        with self.assertRaises(requests.exceptions.RequestException):
            download_github_release_asset(
                self.owner,
                self.repo,
                self.tag_name,
                self.asset_name,
                self.test_output_path,
            )


if __name__ == "__main__":
    unittest.main()
