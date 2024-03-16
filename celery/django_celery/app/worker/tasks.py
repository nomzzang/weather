from celery import shared_task
from .max_api import MaxAPI



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
#     AirAPI.dust_info_forecast_name('대기질예보통보조회')
#     return print("Read_csv")

@shared_task()
def fct_land_forecast():
    #단기 육상 예보조회 5, 11, 17
    MaxAPI.fct_land_forecast()
    return print("test단기 육상 예보조회test")

@shared_task()
def fct_ocean_forecast():
    #단기 해상 예보 조회 5, 11, 17   
    MaxAPI.fct_ocean_forecast()
    return print("test단기 해상 예보 조회test")

@shared_task()
def fct_mid_land_temp_forecast():
    #중기 기온 예보 조회 6, 18
    MaxAPI.fct_mid_land_temp_forecast()
    return print("test중기 기온 예보 조회test")

@shared_task()
def fct_mid_land_status_forecast():
    #중기 날씨 예보 조회 6, 18
    MaxAPI.fct_mid_land_status_forecast()
    return print("test중기 날씨 예보 조회test")

