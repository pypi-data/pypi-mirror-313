import requests
import os
import zipfile
import tempfile
from dexhub import load  # Assuming `dexhub.load` is available for loading `.dex` files

BASE_URL = "https://ssm.dexhub.ai"
API_TOKEN = os.getenv("DEXHUB_API_TOKEN", None)

def get_dataset_uuids() -> list:
    """
    Fetches the list of datasets available in DexHub along with their details.

    This function sends a GET request to the DexHub API to retrieve a list of datasets.
    The response includes details such as the UUID, name, description, and download URL
    for each dataset.

    :return: A list of dictionaries, where each dictionary contains the following keys:
             - "uuid": The unique identifier of the dataset.
             - "name": The name of the dataset (optional, may be empty).
             - "description": A short description of the dataset (optional, may be empty).
             - "download_url": The pre-signed URL for downloading the dataset.
             If no datasets are found or an error occurs, an empty list is returned.
    :rtype: list

    Raises:
        :class:`requests.exceptions.RequestException`: If there is an error during the GET request.

    .. note::
        - If the response structure is unexpected or no datasets are found, the function will log a message
          and return an empty list.
    """
    url = f"{BASE_URL}/data/datasets"
    headers = {
        "API_TOKEN": API_TOKEN,
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "Success" and "items" in data:
                datasets = []
                for item in data["items"]:
                    dataset = {
                        "uuid": item["uuid"],
                        "name": item.get("name", ""),
                        "description": item.get("description", ""),
                        "download_url": item.get("zipKey", ""),
                    }
                    datasets.append(dataset)
                return datasets
            else:
                print("No datasets found or unexpected response structure.")
                return []
        else:
            print(f"Failed to fetch datasets: {response.status_code}")
            print(response.text)
            return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []
    

def find_dataset_uuid(name: str) -> str:
    """
    Finds the UUID of a dataset by its name.

    This function searches through the list of available datasets for one with a name
    matching the input `name`. If a match is found, it returns the UUID of the dataset.
    If no match is found, it returns `None`.

    :param name: The name of the dataset to search for.
    :type name: str
    :return: The UUID of the matching dataset, or `None` if no match is found.
    :rtype: str or None

    Raises:
        :class:`requests.exceptions.RequestException`: If there is an error during the GET request.

    .. note::
        - This function performs a case-sensitive search.
    """
    datasets = get_dataset_uuids()
    for dataset in datasets:
        if dataset["name"] == name:
            return dataset["uuid"]
    return None



def download_dataset(uuid: str) -> list:
    """
    Downloads a dataset from the DexHub server using its UUID, extracts its contents,
    loads individual `.dex` files using `dexhub.load`, and returns a list of loaded
    objects.

    :param uuid: The UUID of the dataset to download.
    :type uuid: str
    :return: A list of objects loaded from `.dex` files in the dataset.
    :rtype: list

    Raises:
        :class:`requests.exceptions.RequestException`: If there is an error during the GET request.
        :class:`OSError`: If there is an issue writing the dataset file to disk or extracting it.
        :class:`FileNotFoundError`: If no `.dex` files are found in the extracted dataset.
    """
    url = f"{BASE_URL}/data/dataset/download/{uuid}"
    headers = {
        "API_TOKEN": API_TOKEN,
    }

    try:
        # Step 1: Download the dataset ZIP file
        response = requests.get(url, headers=headers, stream=True)
        if response.status_code == 200:
            # Save the ZIP file to a temporary location
            temp_dir = tempfile.mkdtemp()
            zip_path = os.path.join(temp_dir, f"dataset_{uuid}.zip")
            with open(zip_path, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
            print(f"Dataset {uuid} downloaded successfully as {zip_path}.")

            # Step 2: Extract the ZIP file
            extracted_dir = os.path.join(temp_dir, f"dataset_{uuid}")
            os.makedirs(extracted_dir, exist_ok=True)
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extracted_dir)
            print(f"Dataset {uuid} extracted to {extracted_dir}.")

            # Step 3: Load `.dex` files using `dexhub.load`
            dex_files = [os.path.join(extracted_dir, f) for f in os.listdir(extracted_dir) if f.endswith('.dex')]
            if not dex_files:
                raise FileNotFoundError("No `.dex` files found in the extracted dataset.")

            dex_objects = []
            for dex_file in dex_files:
                print(f"Loading {dex_file}...")
                dex_objects.append(load(dex_file))

            print(f"Successfully loaded {len(dex_objects)} `.dex` files.")
            return dex_objects

        else:
            print(f"Failed to download dataset: {response.status_code}")
            print(response.text)
            return []
    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the dataset download: {e}")
        raise
    except OSError as e:
        print(f"An error occurred while handling the dataset files: {e}")
        raise
    except FileNotFoundError as e:
        print(f"An error occurred: {e}")
        raise


if __name__ == "__main__":
    datasets = get_dataset_uuids()
    if datasets:
        print("Fetched datasets:")
        for dataset in datasets:
            print(f"UUID: {dataset['uuid']}")
            print(f"Name: {dataset['name']}")
            print(f"Description: {dataset['description']}")
            print(f"Download URL: {dataset['download_url']}\n")

        # Download the first dataset
        dataset = download_dataset(datasets[0]["uuid"])
        print(dataset)
    else:
        print("No datasets available.")