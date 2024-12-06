import unittest
from unittest.mock import patch, mock_open
from arka_python_dev.api import ArkaClient
from unittest.mock import patch, MagicMock
import requests
import os

rpc_url = "http://localhost:26657"
rest_url = "http://localhost:1317"
ipfs_url = "http://127.0.0.1:8080" 

class TestArkaClient(unittest.TestCase):
    # Test the initialization of ArkaClient with default URLs
    def test_initialization(self):
        client = ArkaClient()
        self.assertEqual(client.rpc_url, rpc_url)
        self.assertEqual(client.rest_url, rest_url)
        self.assertEqual(client.ipfs_url, ipfs_url)

    # Test list_files with local IPFS daemon
    def test_list_files_ipfs(self):
        client = ArkaClient()
        test_cid = "QmRmK3fLkmuDUCZD95yM6hgtd4auuo3BTGgkXMfTYuHeCr"

        # Fetch files and directories for the given CID
        files = client.list_files(test_cid)
        
        # Check that files were returned
        self.assertIsInstance(files, list)
        if files:
            for file_info in files:
                self.assertIn("name", file_info)
                self.assertIn("size", file_info)
                self.assertIn("hash", file_info)
                self.assertIn("path", file_info)
                # print(f"File: {file_info['path']} (CID: {file_info['hash']}, Size: {file_info['size']})")
        else:
            print("No files found for CID. Ensure the test CID is correct and available in IPFS.")
            
            
    # Test list_files with a mock IPFS response
    @patch("arka.api.requests.get")
    def test_list_files_mock(self, mock_get):
        client = ArkaClient()
        test_cid = "QmUoFs8eg51KxF5qQHLqk4EfFB9fPHnaPc5vDu13Ps4krP"

        mock_response_data = {
            "Objects": [
                {
                    "Hash": test_cid,
                    "Links": [
                        {
                            "Name": "Dockerfile",
                            "Hash": "QmeEjbRV73WbTmMdNgTssTac8NYjJzDR4kPmGnunrDMmhP",
                            "Size": 724,
                            "Type": 2,
                            "Target": ""
                        },
                        {
                            "Name": "go.mod",
                            "Hash": "QmeZ8TH8qYpwjvpHpymYF7d8wEYq7BTuMTq32oiFjxGr9W",
                            "Size": 37,
                            "Type": 2,
                            "Target": ""
                        },
                        {
                            "Name": "go.sum",
                            "Hash": "QmbFMke1KXqnYyBBWxB74N4c5SBnJMVAiMNRcGu6x1AwQH",
                            "Size": 0,
                            "Type": 2,
                            "Target": ""
                        },
                        {
                            "Name": "main.go",
                            "Hash": "Qmbb65bzTJryVwA2uGZ2VN9LZJnzqBFfxGomHNSfnrdfwc",
                            "Size": 1951,
                            "Type": 2,
                            "Target": ""
                        }
                    ]
                }
            ]
        }

        mock_get.return_value.json.return_value = mock_response_data
        files = client.list_files(test_cid)

        self.assertIsInstance(files, list)
        self.assertEqual(len(files), 4, "The number of files listed should be 4.")

        # check whether each item in the response contains the expected fields.
        expected_keys = {"name", "size", "hash", "path"}
        for file_info in files:
            # print("file_info keys:", file_info.keys())
            self.assertTrue(expected_keys.issubset(file_info.keys()), "Each file info should contain name, size, hash, and path.")

        self.assertEqual(files[0]["name"], "Dockerfile")
        self.assertEqual(files[0]["size"], 724)
        self.assertEqual(files[0]["hash"], "QmeEjbRV73WbTmMdNgTssTac8NYjJzDR4kPmGnunrDMmhP")
        self.assertEqual(files[0]["path"], "/Dockerfile")
        self.assertEqual(client.rpc_url, "http://localhost:26657")
        self.assertEqual(client.rest_url, "http://localhost:1317")
        self.assertEqual(client.ipfs_url, "http://127.0.0.1:8080")

    @patch("arka.api.requests.get")
    def test_download_file_mocked(self, mock_get):
        test_cid = "QmExampleRootHash"
        dest_folder = "test_downloads"
        
        # Mock the IPFS response data
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "Objects": [
                {
                    "Hash": test_cid,
                    "Links": [
                        {
                            "Name": "Dockerfile",
                            "Hash": "QmeEjbRV73WbTmMdNgTssTac8NYjJzDR4kPmGnunrDMmhP",
                            "Size": 724,
                            "Type": 2
                        },
                        {
                            "Name": "go.mod",
                            "Hash": "QmeZ8TH8qYpwjvpHpymYF7d8wEYq7BTuMTq32oiFjxGr9W",
                            "Size": 37,
                            "Type": 2
                        },
                        {
                            "Name": "go.sum",
                            "Hash": "QmbFMke1KXqnYyBBWxB74N4c5SBnJMVAiMNRcGu6x1AwQH",
                            "Size": 0,
                            "Type": 2
                        },
                        {
                            "Name": "main.go",
                            "Hash": "Qmbb65bzTJryVwA2uGZ2VN9LZJnzqBFfxGomHNSfnrdfwc",
                            "Size": 1951,
                            "Type": 2
                        }
                    ]
                }
            ]
        }
        mock_get.return_value = mock_response

        client = ArkaClient(ipfs_url="http://mock-ipfs-url")

        client.download_file(test_cid, dest_folder)

        expected_calls = [
            unittest.mock.call(f"http://mock-ipfs-url/api/v0/ls?arg={test_cid}"),
            unittest.mock.call(f"http://mock-ipfs-url/api/v0/cat?arg=QmeEjbRV73WbTmMdNgTssTac8NYjJzDR4kPmGnunrDMmhP", stream=True),
            unittest.mock.call(f"http://mock-ipfs-url/api/v0/cat?arg=QmeZ8TH8qYpwjvpHpymYF7d8wEYq7BTuMTq32oiFjxGr9W", stream=True),
            unittest.mock.call(f"http://mock-ipfs-url/api/v0/cat?arg=QmbFMke1KXqnYyBBWxB74N4c5SBnJMVAiMNRcGu6x1AwQH", stream=True),
            unittest.mock.call(f"http://mock-ipfs-url/api/v0/cat?arg=Qmbb65bzTJryVwA2uGZ2VN9LZJnzqBFfxGomHNSfnrdfwc", stream=True),
        ]
        mock_get.assert_has_calls(expected_calls, any_order=True)

        # Check if files are created in the destination folder (simulated here)
        for link in mock_response.json()["Objects"][0]["Links"]:
            file_path = os.path.join(dest_folder, link["Name"])
            self.assertTrue(os.path.exists(file_path))

        # Clean up by removing the created folder and files (optional)
        for link in mock_response.json()["Objects"][0]["Links"]:
            file_path = os.path.join(dest_folder, link["Name"])
            if os.path.exists(file_path):
                os.remove(file_path)
        if os.path.exists(dest_folder):
            os.rmdir(dest_folder)

    @patch("arka.api.requests.get")
    def test_version_by_id_mock(self, mock_get):
        # Set up the mock response
        expected_data = {
            'version': [{
                'id': '2',
                'commit_message': 'a simple python api',
                'cid': 'QmdcryKhAb7E8Xxnaziqj8VTBCrnuLdykk8s84NZgbH2aJ',
                'created_at': '2024-11-07T13:11:44.717400950Z',
                'repository_id': '2'
            }]
        }
        repository_id = 2
        version_id = 2

        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = expected_data

        client = ArkaClient(rpc_url, rest_url)
        result = client.get_version_by_id(repository_id, version_id)

        # Set up the mock response for a failed request
        mock_get.return_value.status_code = 404
        mock_get.return_value.raise_for_status.side_effect = requests.exceptions.HTTPError
        # Check if an exception is raised for a non-200 status code
        with self.assertRaises(requests.exceptions.HTTPError):
            client.get_version_by_id(repository_id, version_id)
            
    @patch("arka.api.requests.get")
    def test_get_repository_by_id_mock(self, mock_get):
        # Set up the mock response for a successful request
        expected_data = {
            'id': '3',
            'name': 'repo-3',
            'description': 'this is the description of repo-3',
            'repository_type': 1,
            'tags': ['cosmos', 'ibc', 'golang'],
            'clone_metadata': {
                'repository_id': '3',
                'version_id': '7'
            },
            'inference_metadata': {
                'data': [{
                    'input_fields': [{'field_name': 'request', 'title': 'Enter request'}],
                    'method_name': 'POST',
                    'output_fields': [
                        {'field_name': 'result', 'title': 'Returns result'},
                        {'field_name': 'status', 'title': 'Returns agent response status'}
                    ],
                    'resource': '/predict'
                }]
            },
            'image': 'http://image.com',
            'metadata': 'ewogICAgImhlbGxvIjogIndvcmxkIgp9',
            'created_at': '2024-12-04T11:50:07.783837521Z'
        }
        repository_id = 3

        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = expected_data

        client = ArkaClient(rpc_url, rest_url)
        
        result = client.get_repository_by_id(repository_id)

        self.assertEqual(result, expected_data)
        mock_get.assert_called_once_with(f"{rest_url}/arka/storage/v1beta1/repositories/{repository_id}")

        # Set up the mock response for a failed request
        mock_get.return_value.status_code = 404
        mock_get.return_value.raise_for_status.side_effect = requests.exceptions.HTTPError

        # Check if an exception is raised for a non-200 status code
        with self.assertRaises(requests.exceptions.HTTPError):
            client.get_repository_by_id(repository_id)


    @patch("arka.api.requests.get")
    def test_versions_mock(self, mock_get):
        # Set up the mock response
        expected_data = {
            'versions': [{
                'id': '2',
                'commit_message': 'a simple python api',
                'cid': 'QmdcryKhAb7E8Xxnaziqj8VTBCrnuLdykk8s84NZgbH2aJ',
                'created_at': '2024-11-07T13:11:44.717400950Z',
                'repository_id': '2'
            }]
        }

        repository_id = 2
        
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = expected_data

        client = ArkaClient(rpc_url, rest_url)
        result = client.get_versions(repository_id)

        # Set up the mock response for a failed request
        mock_get.return_value.status_code = 404
        mock_get.return_value.raise_for_status.side_effect = requests.exceptions.HTTPError
        # Check if an exception is raised for a non-200 status code
        with self.assertRaises(requests.exceptions.HTTPError):
            client.get_versions(repository_id)


    @patch("arka.api.requests.get")
    def test_repositories(self, mock_get):
        # Set up the mock response
        expected_data = {
            'repositories': [{
                'id': '2', 
                'name': 'python', 
                'created_at': '2024-11-07T08:48:22.001571465Z', 
                'metadata': 'ewogICAgImhlbGxvIjogIndvcmxkIgp9', 
                'admin': 'arka1kpgtjc7xyqx399f7xetgczfqs90kagmkk35u7z'
            }]
        }
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = expected_data

        client = ArkaClient(rpc_url, rest_url)
        result = client.get_repositories()

        # Set up the mock response for a failed request
        mock_get.return_value.status_code = 404
        mock_get.return_value.raise_for_status.side_effect = requests.exceptions.HTTPError

        # Check if an exception is raised for a non-200 status code
        with self.assertRaises(requests.exceptions.HTTPError):
            client.get_repositories()
        
    @patch("arka.api.requests.post")
    @patch("os.path.exists")
    @patch("os.walk")
    @patch("builtins.open", new_callable=mock_open)
    def test_upload_file_mock(self, mock_open_file, mock_walk, mock_exists, mock_post):
        client = ArkaClient()
        test_directory_path = "mock_directory"
        
        # Setup mock response
        mock_response_text = """{"Name":"file1.txt","Hash":"QmFile1CID","Size":"20"}
                                {"Name":"file2.txt","Hash":"QmFile2CID","Size":"30"}
                                {"Name":"mock_directory","Hash":"QmMockedRootCID","Size":"50"}"""
        mock_post.return_value.status_code = 200
        mock_post.return_value.text = mock_response_text
        
       
        mock_exists.return_value = True
        mock_walk.return_value = [
            (test_directory_path, [], ["file1.txt", "file2.txt"]),
        ]

        result = client.upload_file(test_directory_path)

        self.assertEqual(result, "QmMockedRootCID", "Root CID should match the mocked response.")
        mock_post.assert_called_once()
        self.assertTrue(mock_open_file.called, "Files should be opened for reading.")


if __name__ == "__main__":
    unittest.main()
