from celery import shared_task
from .max_api import MaxAPI
from .weather_api import WeatherAPI
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
api_config_path = 'apiconfig/weather_apiConfig.json'
service_key_path = 'apiconfig/service_key.json'

# Initialize WeatherAPI instance
weather_api = WeatherAPI(WeatherAPI.load_api_config(api_config_path),
                         WeatherAPI.load_service_key(service_key_path)['weather_serviceKey'])

@shared_task
def data_by_shot_forecast(endpoint_name):
    print("data_by_shot_forecast 실행")
    print("start: tasks", endpoint_name)
    try:
        result = weather_api.data_by_shot_forecast(endpoint_name)
        logger.info(f"Data fetched successfully for {endpoint_name}.")
        return result
    except Exception as e:
        logger.error(f"Error fetching data for {endpoint_name}: {e}")

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
