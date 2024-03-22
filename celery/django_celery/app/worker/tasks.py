from celery import shared_task
from celery.exceptions import MaxRetriesExceededError
from requests.exceptions import RequestException
from .data_sender import send_data_to_endpoint
from .weather_api import WeatherAPI
from celery.utils.log import get_task_logger
import logging
from django.conf import settings
import csv, os
import requests

logger = logging.getLogger(__name__)
api_config_path = 'apiconfig/weather_apiConfig.json'
service_key_path = 'apiconfig/service_key.json'

# Initialize WeatherAPI instance
weather_api = WeatherAPI(WeatherAPI.load_api_config(api_config_path),
                         WeatherAPI.load_service_key(service_key_path)['weather_serviceKey'])



@shared_task(bind=True, max_retries=5, default_retry_delay=150, queue='queue1')
def fetch_data_for_location(self, endpoint_name, nx, ny):
    try:
        # print(f"Starting task for endpoint {endpoint_name} with nx={nx}, ny={ny}")
        result = weather_api.data_by_shot_forecast(endpoint_name, nx, ny)
        if result is None:
            raise ValueError("Received invalid JSON response")
        logger.info(f"Success: Data fetched for {endpoint_name} at nx={nx}, ny={ny}")

        # 데이터 전송 작업을 호출
        send_weather_data_to_server.delay(endpoint_name, result)

        # print(f"Task succeeded for endpoint {endpoint_name} with nx={nx}, ny={ny}")
        return result
    except (requests.exceptions.ConnectionError, requests.HTTPError, ValueError) as e:
        logger.warning(f"Connection or HTTP error on {endpoint_name}: {e}. This is retry number {self.request.retries + 1}. Retrying...")
        self.retry(exc=e)
    except MaxRetriesExceededError as e:
        logger.error(f"Max retries exceeded after {self.request.retries} attempts for task {self.request.id} with endpoint {endpoint_name}, nx={nx}, ny={ny}")
        raise e
    except Exception as e:
        logger.error(f"Error fetching data for {endpoint_name} at nx={nx}, ny={ny}: {e}")
        raise e
    

@shared_task()
def data_by_shot_forecast(endpoint_name):
    # Path to your CSV file
    csv_file_path = os.path.join(settings.BASE_DIR, 'worker', 'local_info', 'local_grid_loc_nx_ny.csv')
    with open(csv_file_path, mode='r', newline='', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            fetch_data_for_location.delay(endpoint_name, row['nx'], row['ny'])


@shared_task()
def fetch_weather_data(endpoint_name, nx, ny):
    data = weather_api.data_by_shot_forecast(endpoint_name, nx, ny)
    # Assuming the next task needs the data and the endpoint URL for the server
    send_weather_data_to_server.delay('http://yourserver.com/data', data)

@shared_task(queue='queue2')
def send_weather_data_to_server(endpoint_name, data):
    response = send_data_to_endpoint(endpoint_name, data)
    return response  # Log or use the response as needed



@shared_task(name='fetch_sunrise_sunset_data')
def sunrise_sunset_data(location='서울'):
    try:
        result = weather_api.sunrise_sunset_data('지역별해달출몰시각정보조회', location)
        logger.info("sunrise_sunset_data: %s", result)
        return "sunrise_sunset_data"
    except Exception as e:
        logger.error("Error fetching sunrise and sunset data: %s", e)
        return None


@shared_task()
def add(x, y):
    return x + y

# # Synchronous Task
# def sync_task():
#     result = sleep_task.apply_async() # type: ignore
#     print("Waiting ...")
#     print(result.get())

# # Asynchronous Task
# def async_task():
#     result = sleep_task.apply_async() # type: ignore
#     print("Not waiting ...")
#     print(result.task_id)

# @shared_task()
# def dust_info_forecast_name():
#     AirAPI.dust_info_forecast_name('대기질예보통보조회')ls
#     return print("Read_csv")

# @shared_task()
# def fct_land_forecast():
#     #단기 육상 예보조회 5, 11, 17
#     MaxAPI.fct_land_forecast()
#     return print("test단기 육상 예보조회test")

# @shared_task()
# def fct_ocean_forecast():
#     #단기 해상 예보 조회 5, 11, 17   
#     MaxAPI.fct_ocean_forecast()
#     return print("test단기 해상 예보 조회test")

# @shared_task()
# def fct_mid_land_temp_forecast():
#     #중기 기온 예보 조회 6, 18
#     MaxAPI.fct_mid_land_temp_forecast()
#     return print("test중기 기온 예보 조회test")

# @shared_task()
# def fct_mid_land_status_forecast():
#     #중기 날씨 예보 조회 6, 18
#     MaxAPI.fct_mid_land_status_forecast()
#     return print("test중기 날씨 예보 조회test")
