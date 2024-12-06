import requests
import ipfshttpclient
import os
import json
from tqdm import tqdm
class ArkaClient:
    # Initializes the ArkaClient with given RPC, REST and IPFS endpoints.
    def __init__(self, rpc_url="http://localhost:26657", rest_url="http://localhost:1317", ipfs_url="http://127.0.0.1:8080", ipfs_ip="164.92.97.19", ipfs_port=5001):
        self.rpc_url = rpc_url
        self.rest_url = rest_url
        self.ipfs_url = ipfs_url
        self.ipfs_ip = ipfs_ip
        self.ipfs_port = ipfs_port
    
    # query version w.r.t given version_id and repository_id
    def get_version_by_id(self, repository_id, version_id):
        response = requests.get(f"{self.rest_url}/arka/storage/v1beta1/repositories/{repository_id}/versions/{version_id}")
        response.raise_for_status()
        return response.json()
    
    # query repository w.r.t given repository_id
    def get_repository_by_id(self, repository_id):
        response = requests.get(f"{self.rest_url}/arka/storage/v1beta1/repositories/{repository_id}")
        response.raise_for_status()
        return response.json()

    # Fetch all the versions of a repository from arka
    def get_versions(self, repository_id=None, pagination=None):
        base_url = f"{self.rest_url}/arka/storage/v1beta1/versions"
        params = {"limit": 30}
        
        if repository_id:
                params["repository_id"] = repository_id
        if pagination:
                if "offset" in pagination:
                        params["pagination.offset"] = pagination["offset"]
                if "key" in pagination:
                        params["pagination.key"] = pagination["key"]
                if "limit" in pagination:
                        params["pagination.limit"] = pagination["limit"]
                if "count_total" in pagination:
                        params["pagination.count_total"] = pagination["count_total"]
                if "reverse" in pagination:
                        params["pagination.reverse"] = pagination["reverse"]
                
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        return response.json()
    
    # Fetch all the repositories from Arka
    def get_repositories(self, owner=None, pagination=None):
        base_url = f"{self.rest_url}/arka/storage/v1beta1/repositories"
        params = {"limit": 30}

        if owner:
                params["address"] = owner
        if pagination:
                if "offset" in pagination:
                        params["pagination.offset"] = pagination["offset"]
                if "key" in pagination:
                        params["pagination.key"] = pagination["key"]
                if "limit" in pagination:
                        params["pagination.limit"] = pagination["limit"]
                if "count_total" in pagination:
                        params["pagination.count_total"] = pagination["count_total"]
                if "reverse" in pagination:
                        params["pagination.reverse"] = pagination["reverse"]

        response = requests.get(base_url, params=params)
        response.raise_for_status()
        return response.json()

    # List all files and subdirectories for a given version CID in IPFS
    def list_files(self, cid, path=""):
        try:
            # Make an HTTP request to the IPFS API to list directory contents for the CID
            response = requests.get(f"{self.ipfs_url}/api/v0/ls?arg={cid}")
            result = response.json()

            all_files = []
            if "Objects" in result:
                for obj in result["Objects"]:
                    if "Links" in obj:
                        for link in obj["Links"]:
                            file_info = {
                                "name": link.get("Name", ""),
                                "size": link.get("Size", 0),
                                "hash": link.get("Hash", ""),
                                "path": f"{path}/{link.get('Name', '')}"
                            }

                            if link.get("Type") == 1:
                                sub_files = self.list_files(link["Hash"], path=file_info["path"])
                                all_files.extend(sub_files)
                            else:
                                all_files.append(file_info)

            return all_files
        except Exception as e:
            print(f"Error fetching files for CID {cid}: {e}")
            return []
    
    # Download the files uploaded on ipfs using cid
    def download_file(self, cid, dest_folder):
        url = f"{self.ipfs_url}/api/v0/ls?arg={cid}"

        os.makedirs(dest_folder, exist_ok=True)

        response = requests.get(url)
        response.raise_for_status()

        data = response.json()
        if "Objects" not in data or not data["Objects"]:
            print("No files found for this CID.")
            return

        for link in data["Objects"][0].get("Links", []):
            file_name = link["Name"]
            file_hash = link["Hash"]
            file_size = link["Size"]
            file_type = link["Type"]
            file_path = os.path.join(dest_folder, file_name)

            if file_type == 1:
                os.makedirs(file_path, exist_ok=True)
                print(f"Entering directory: {file_path}")
                self.download_file(file_hash, file_path)
            elif file_type == 2:
                # Download the file with a progress bar
                file_url = f"{self.ipfs_url}/api/v0/cat?arg={file_hash}"
                with requests.get(file_url, stream=True) as r:
                    r.raise_for_status()
                    with open(file_path, "wb") as f, tqdm(
                        desc=f"Downloading {file_name}",
                        total=file_size,
                        unit="B",
                        unit_scale=True,
                        unit_divisor=1024,
                    ) as bar:
                        for chunk in r.iter_content(chunk_size=1024):
                            f.write(chunk)
                            bar.update(len(chunk))
                print(f"Downloaded {file_name} to {file_path}")
                
    def upload_file(self, path):         
        if not os.path.exists(path):
            raise FileNotFoundError(f"Path not found: {path}")
        
        # url = f"{self.ipfs_api}/api/v0/add"
        url = f"http://{self.ipfs_ip}:{self.ipfs_port}/api/v0/add"
        is_dir = os.path.isdir(path)

        files = []
        if is_dir:
            for root, _, filenames in os.walk(path):
                for filename in filenames:
                    full_path = os.path.join(root, filename)
                    relative_path = os.path.relpath(full_path, path)
                    files.append(('file', (relative_path, open(full_path, 'rb'))))
        else:
            files.append(('file', (os.path.basename(path), open(path, 'rb'))))

        try:
            # make post request to ipfs
            response = requests.post(
                url,
                params={"recursive": "true", "wrap-with-directory": "true"},
                files=files
            )
            
            for f in files:
                f[1][1].close()

            response.raise_for_status()
            print("uploaded files:\n", response.text)
            
            file_hashes = []
            for line in response.text.splitlines():
                try:
                    response_data = json.loads(line)
                    file_hashes.append(response_data["Hash"])
                except json.JSONDecodeError as e:
                    print(f"Error decoding line: {line}")
                    print(e)

            # return the root folder cid
            return file_hashes[-1] if file_hashes else None  
        
        except requests.exceptions.RequestException as e:
            print(f"Error during file upload: {e}")
            return None
