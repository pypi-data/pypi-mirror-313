import requests
import os 
from dexhub import * 
import json
import json 
from enum import Enum

base_url = "https://ssm.dexhub.ai"
dexhub_api_token = os.getenv("DEXHUB_API_TOKEN", None)

real_log_endpoint = "/data/upload/contribution"
download_endpoint = "/data/list/contributions"
    


class EnumEncoder(json.JSONEncoder):
    """
    Custom encoder to convert Enum types to their values for JSON serialization.
    """
    def default(self, obj):
        if isinstance(obj, Enum):
            return obj.value
        return json.JSONEncoder.default(self, obj)


def upload_file(file_buffer, filename, meta_data, video_buffer = None ):
    """
    Uploads files to DexHub using an in-memory buffer, along with the metadata.

    :param file_buffer: The file buffer containing the serialized data.
    :param filename: The name of the file to upload.
    :param meta_data: The metadata associated with the upload.
    """

    url = f"{base_url}{real_log_endpoint}"
    headers = {
        "API_TOKEN": dexhub_api_token,
    }

    # Serialize meta_data using the custom EnumEncoder
    meta_data_json = json.dumps(meta_data, cls=EnumEncoder)

    # Prepare the files and form data
    files = {
        'file': (filename, file_buffer, 'application/octet-stream'),
    }

    if video_buffer is not None: 
        files['video'] = (filename[:-4] + ".mp4", video_buffer, 'video/mp4')
        print("video buffer ready to be uploaded")

    # Metadata sent as a separate form field
    form_data = {
        'meta_data': meta_data_json, 
    }

    try:
        # Send a POST request with both file and metadata in multipart/form-data format
        response = requests.post(url, headers=headers, files=files, data=form_data)

        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "Success":
                print("File uploaded successfully.")
                print(f"Details: {data['details']}")
                print(f"Message: {data['message']}")
            else:
                print("Upload failed:", data)
        else:
            print(f"Error: Received status code {response.status_code}")
            print(response.text)

    except Exception as e:
        print(f"An error occurred: {e}")

def get_list(self, min_expiration=100):
    url = f"{self.base_url}{self.download_endpoint}?min={min_expiration}"
    headers = {
        "API_TOKEN": dexhub_api_token,
    }
    
    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "Success":
                print("Files listed successfully:")
                for item in data["data"]:
                    print(f"Name: {item['name']}, URL: {item['url']}, Created At: {item['created_at']}")
                print(f"Message: {data['message']}")
            else:
                print("Failed to list files:", data)
        else:
            print(f"Error: Received status code {response.status_code}")
            print(response.text)
    
    except Exception as e:
        print(f"An error occurred: {e}")


    

