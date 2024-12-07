import json
import requests
from awe.util.logging import logger

def post_request(server_address, endpoint, data=None):
    url = f"http://{server_address}{endpoint}"
    headers = {"Content-Type": "application/json"} if data else {}
    json_data = json.dumps(data).encode("utf-8") if data else None
    response = requests.post(url, headers=headers, data=json_data)
    if response.status_code != 200:
        logger.info(f"Failed: {endpoint}, status code: {response.status_code}")
    return response