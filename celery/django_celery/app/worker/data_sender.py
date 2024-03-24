import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.app.settings")  # Django 프로젝트 설정 파일 경로 수정 필요
django.setup()

from worker.models import UltraShortTermLiveStatus, ShortTermForecast, UltraShortTermForecast  

def send_data_to_ultra_short_term_forecast(data):
    """
    초단기 예보 데이터를 데이터베이스에 저장합니다.
    data: 예보 데이터가 담긴 딕셔너리 객체
    """
    for item in data['response']['body']['items']['item']:
        UltraShortTermForecast.objects.create(
            base_date=item['baseDate'],
            base_time=item['baseTime'],
            category=item['category'],
            fcst_date=item['fcstDate'],
            fcst_time=item['fcstTime'],
            fcst_value=item['fcstValue'],
            nx=item['nx'],
            ny=item['ny']
        )
    print("Data saved to UltraShortTermForecast model.")

# 예제 데이터
example_data = {
    "response": {
        "body": {
            "items": {
                "item": [
                    {
                        "baseDate": "20240323",
                        "baseTime": "0500",
                        "category": "TMP",
                        "fcstDate": "20240323",
                        "fcstTime": "0600",
                        "fcstValue": "7",
                        "nx": 55,
                        "ny": 127
                    },
                    # 더 많은 데이터 아이템...
                ]
            }
        }
    }
}

def send_data_to_ultra_short_term_live_status(data):
    """
    초단기 실황 데이터를 데이터베이스에 저장합니다.
    """
    for item in data['response']['body']['items']['item']:
        UltraShortTermLiveStatus.objects.create(
            base_date=item['baseDate'],
            base_time=item['baseTime'],
            category=item['category'],
            obsr_value=item['obsrValue'],
            nx=item['nx'],
            ny=item['ny']
        )
    print("Data saved to UltraShortTermLiveStatus model.")

def send_data_to_short_term_forecast(data):
    """
    단기 예보 데이터를 데이터베이스에 저장합니다.
    """
    for item in data['response']['body']['items']['item']:
        ShortTermForecast.objects.create(
            base_date=item['baseDate'],
            base_time=item['baseTime'],
            category=item['category'],
            fcst_date=item['fcstDate'],
            fcst_time=item['fcstTime'],
            fcst_value=item['fcstValue'],
            nx=item['nx'],
            ny=item['ny']
        )
    print("Data saved to ShortTermForecast model.")


# 함수 호출 예시
if __name__ == "__main__":
    send_data_to_ultra_short_term_forecast(example_data)

# def load_endpoint_url(endpoint_name):
#     # Get the directory of the current script
#     current_dir = os.path.dirname(__file__)
#     print(current_dir)
    
#     # Construct the path to the JSON configuration file
#     config_path = os.path.join(current_dir, 'apiconfig', 'open_api_settings.json')
#     print(config_path)
    
#     # Open the configuration file and search for the endpoint URL
#     with open(config_path, 'r', encoding='utf-8') as file:
#         settings = json.load(file)
#         for endpoint in settings['apiEndpoints']:
#             if endpoint['name'] == endpoint_name:
#                 return endpoint['url']
#     return None

# def send_data_to_endpoint(endpoint_name, data):
#     # url = load_endpoint_url(endpoint_name)
#     print("send_data", endpoint_name, data)
    # response = requests.post(url, json=data)
    # response.raise_for_status()  # 오류가 있을 경우 예외 발생
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
        