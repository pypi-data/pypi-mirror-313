import os
import layernext
from dotenv import load_dotenv

from layernext.datalake.constants import MediaType

load_dotenv()  # take environment variables from .env.

api_key = os.environ.get('API_KEY')
secret = os.environ.get('SECRET')
serverUrl = os.environ.get('LAYERX_URL')

client = layernext.LayerNextClient(api_key, secret, serverUrl)

# file_path = os.environ.get('FILE_TO_UPLOAD')
# client.upload_modelrun_from_json('val2017_image', 'Test 1.0.1', file_path, 'rectangle')
# client.upload_modelrun_from_json('val2017_image', 'Test 1.0.1', file_path, 'polygon')
# client.upload_modelrun_from_json('val2017_image', 'Test 1.0.1', file_path, 'line')

path = "C:/Users/chama/Downloads/testUpload"
# path = "C:/Users/chama/Downloads/training_set/test"
collection_type = MediaType.IMAGE.value
collection_name = ""
meta_data_object = {
    "Captured Location": "test_location",
    "Camera Id": "aaa",
    "Tags": [
        "#retail"
    ],
    "bird": "flying"
}

# client.file_upload(path, collection_type, collection_name, meta_data_object)
