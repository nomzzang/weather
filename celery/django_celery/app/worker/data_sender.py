import requests
import json
import os

def load_endpoint_url(endpoint_name):
    # Get the directory of the current script
    current_dir = os.path.dirname(__file__)
    print(current_dir)
    
    # Construct the path to the JSON configuration file
    config_path = os.path.join(current_dir, 'apiconfig', 'open_api_settings.json')
    print(config_path)
    
    # Open the configuration file and search for the endpoint URL
    with open(config_path, 'r', encoding='utf-8') as file:
        settings = json.load(file)
        for endpoint in settings['apiEndpoints']:
            if endpoint['name'] == endpoint_name:
                return endpoint['url']
    return None

def send_data_to_endpoint(endpoint_name, data):
    url = load_endpoint_url(endpoint_name)
    print(endpoint_name)
    print("----------")
    print(url)
    response = requests.post(url, json=data)
    response.raise_for_status()  # 오류가 있을 경우 예외 발생
    print(f"Data successfully sent to {url}")
    # if url is not None:
    #     try:
    #         return response.json()
    #     except requests.exceptions.HTTPError as err:
    #         print(f"HTTP error occurred: {err}")
    #     except Exception as err:
    #         print(f"An error occurred: {err}")
    # else:
    #     print(f"Endpoint {endpoint_name} not found.")

# 예시 사용
# data = {'example_key': 'example_value'}
# send_data_to_endpoint('store_sunrise_sunset', data)
        