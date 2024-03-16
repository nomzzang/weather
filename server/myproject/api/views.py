from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import ApiResponse
from .models import SidoRealTimeAirQuality
from .models import SunriseSunset1
from .models import MidTermLandForecast
from .models import MidTermTemperature
from .models import WeatherShtTermLandForecast, WeatherShtTermOceanForecast, WeatherShtTermCode, WeatherMidTermLandTempForecast, WeatherMidTermLandStatusForecast, WeatherAlertForecast
from .models import AirQualityForecast, AirQualityGrade, WeeklyAirQualityForecast, FineDustGrade, WeatherAws1Mobservation, WeatherAwsStnInfo
from rest_framework import viewsets
from .models import SunriseSunset1
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import SidoRealTimeAirQuality, MidTermTemperature, MidTermLandForecast, AirQualityForecast, AirQualityGrade
from .serializers import SunriseSunset1Serializer, AirQualitySerializer, WeatherForecastSerializer, WeatherForecastDataSerializer, AirQualityInfoSerializer, AirQualityGradeSerializer
from django.utils.dateparse import parse_datetime
from django.views.generic import ListView
import json
from datetime import datetime


class SunriseSunset1ViewSet(viewsets.ModelViewSet):  # 이 클래스 이름이 정확해야 합니다.
    queryset = SunriseSunset1.objects.all()
    serializer_class = SunriseSunset1Serializer

#지역별 일출 일몰    
@csrf_exempt
def store_sunrise_sunset(request):
    print("store_sunrise_sunset")
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            sunrise_sunset_instance = SunriseSunset1(
                latitude=data['latitude'],
                latitudeNum=data['latitudeNum'],
                location=data['location'],
                locdate=data['locdate'],
                longitude=data['longitude'],
                longitudeNum=data['longitudeNum'],
                sunrise=data['sunrise'],
                sunset=data['sunset']
            )
            sunrise_sunset_instance.save()  

            return JsonResponse({'status': 'success', 'message': 'Weather data saved successfully.'})
        except KeyError as e:
            return JsonResponse({'status': 'error', 'message': f'Missing key: {str(e)}'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    else:
        return JsonResponse({'status': 'error', 'message': 'Only POST method is allowed.'}, status=405)
    
#시도별 실시간 측정정보 조회
@csrf_exempt
def store_sido_realtime_airquality(request):
    print("store_sido_realtime_airquality")
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Method not allowed.'}, status=405)

    try:
        data = json.loads(request.body)
        items = data['response']['body']['items']
        for item in items:
            SidoRealTimeAirQuality.objects.create(**item)
            
        return JsonResponse({'status': 'success', 'message': f'{len(items)} air quality records saved successfully.'})
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON format.'}, status=400)
    except KeyError as e:
        return JsonResponse({'status': 'error', 'message': f'Missing key: {e}'}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
#중기기온전망
@csrf_exempt
def store_mid_term_temperature_view(request):
    print("store_mid_term_temperature_view")
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            forecast = MidTermTemperature(
                regId=data['regId'],
                taMin3=data['taMin3'],
                taMax3=data['taMax3'],
                taMin4=data['taMin4'],
                taMax4=data['taMax4'],
                taMin5=data['taMin5'],
                taMax5=data['taMax5'],
                taMin6=data['taMin6'],
                taMax6=data['taMax6'],
                taMin7=data['taMin7'],
                taMax7=data['taMax7'],
                taMin8=data['taMin8'],
                taMax8=data['taMax8'],
                taMin9=data['taMin9'],
                taMax9=data['taMax9'],
                taMin10=data['taMin10'],
                taMax10=data['taMax10']      
            )
            forecast.save() 
            
            return JsonResponse({'status': 'success', 'message': 'Weather data saved successfully.'})
        except KeyError as e:
            return JsonResponse({'status': 'error', 'message': f'Missing key: {str(e)}'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    else:
        return JsonResponse({'status': 'error', 'message': 'Only POST method is allowed.'}, status=405)
    
#중기육상예보조회
@csrf_exempt
def store_mid_term_land_forecast_view(request):
    print("store_mid_term_land_forecast_view")
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # JSON 데이터 파싱
            # 모델 인스턴스 생성
            term_forecast = MidTermLandForecast(
                regId=data.get('regId', ''),
                rnSt3Am=data.get('rnSt3Am', None),  # 기본값으로 None 사용
                rnSt3Pm=data.get('rnSt3Pm', None),
                rnSt4Am=data.get('rnSt4Am', None),
                rnSt4Pm=data.get('rnSt4Pm', None),
                rnSt5Am=data.get('rnSt5Am', None),
                rnSt5Pm=data.get('rnSt5Pm', None),
                rnSt6Am=data.get('rnSt6Am', None),
                rnSt6Pm=data.get('rnSt6Pm', None),
                rnSt7Am=data.get('rnSt7Am', None),
                rnSt7Pm=data.get('rnSt7Pm', None),
                rnSt8=data.get('rnSt8', None),
                rnSt9=data.get('rnSt9', None),
                rnSt10=data.get('rnSt10', None),
                wf3Am=data.get('wf3Am', ''),
                wf3Pm=data.get('wf3Pm', ''),
                wf4Am=data.get('wf4Am', ''),
                wf4Pm=data.get('wf4Pm', ''),
                wf5Am=data.get('wf5Am', ''),
                wf5Pm=data.get('wf5Pm', ''),
                wf6Am=data.get('wf6Am', ''),
                wf6Pm=data.get('wf6Pm', ''),
                wf7Am=data.get('wf7Am', ''),
                wf7Pm=data.get('wf7Pm', ''),
                wf8=data.get('wf8', ''),
                wf9=data.get('wf9', ''),
                wf10=data.get('wf10', '')
            )
            term_forecast.save()  

            return JsonResponse({'status': 'success', 'message': 'Weather data saved successfully.'})
        except KeyError as e:
            return JsonResponse({'status': 'error', 'message': f'Missing key: {str(e)}'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    else:
        return JsonResponse({'status': 'error', 'message': 'Only POST method is allowed.'}, status=405)
    
#대기질 예보통보 조회
@csrf_exempt
def store_air_quality_forecast_view(request):
    print("store_air_quality_forecast_view")
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            print("Received data:", data)

            for date, codes_info in data.items():
                for inform_code, info in codes_info.items():
                    air_quality_info, created = AirQualityForecast.objects.update_or_create(
                        inform_data=date,
                        inform_code=inform_code,
                        defaults={
                            'inform_cause': info['informCause'],
                            'inform_overall': info['informOverall'],
                            'data_time': info['dataTime'],
                        }
                    )
                    
                    AirQualityGrade.objects.filter(air_quality_info=air_quality_info).delete()
                    for region, grade in info['informGrade'].items():
                        AirQualityGrade.objects.create(
                            air_quality_info=air_quality_info,
                            region=region,
                            grade=grade
                        )

            return JsonResponse({'status': 'success', 'message': 'Data saved successfully.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    else:
        return JsonResponse({'status': 'error', 'message': 'Only POST method is allowed.'}, status=405)
    
#초미세먼지 주간예보 조회
@csrf_exempt
def store_fine_dust_weekly_forecast_view(request):
    print("store_fine_dust_weekly_forecast_view")
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            print(data)

            # 데이터 처리 시작
            for date_str, forecasts in data.items():
                # 날짜 문자열을 datetime 객체로 변환
                presentation_date = datetime.strptime(date_str, "%Y-%m-%d").date()

                # FineDustWeeklyForecast 인스턴스 생성 또는 업데이트
                forecast_instance, _ = WeeklyAirQualityForecast.objects.update_or_create(
                    presentation_date=presentation_date,
                )

                # 기존에 연결된 FineDustGrade 인스턴스들을 삭제
                forecast_instance.grades.all().delete()

                # 새로운 FineDustGrade 인스턴스들을 생성
                for forecast_day, regions in forecasts.items():
                    for region, grade in regions.items():
                        FineDustGrade.objects.create(
                            forecast=forecast_instance,
                            forecast_day=forecast_day,
                            region=region,
                            grade=grade,
                        )
            
            return JsonResponse({'status': 'success', 'message': 'Forecast data saved successfully.'})
        
        except Exception as e:
            print(f"An error occurred: {e}")
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    else:
        return JsonResponse({'status': 'error', 'message': 'Only POST method is allowed.'}, status=405)
    
#단기육상예보조회
@csrf_exempt
def store_fine_fct_land_forecast_view(request):
    print("store_fine_fct_land_forecast_view")
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # JSON 데이터 파싱
            # 모델 인스턴스 생성
            print(data.get('regIdIndex', ''))
            print(data)
            term_forecast = WeatherShtTermLandForecast(
                regIdIndex = data.get('regIdIndex', ''),
                regId = data.get('regId', None),  # 기본 키로 설정
                tmFc = data.get('tmFc', None),
                tmEf = data.get('tmEf', None),
                mod = data.get('mod', None),
                ne = data.get('ne', None),
                stn = data.get('stn', None),
                c = data.get('c', None),
                manId = data.get('manId', None),
                manFc = data.get('manFc', None),
                w1 = data.get('w1', None),
                t = data.get('t', None),
                w2 = data.get('w2', None),
                ta = data.get('ta', None),
                st = data.get('st', None),
                sky = data.get('sky', None),
                prep = data.get('prep', None),
                wf = data.get('wf', None),
            )
            term_forecast.save()  

            return JsonResponse({'status': 'success', 'message': 'Weather data saved successfully.'})
        except KeyError as e:
            return JsonResponse({'status': 'error', 'message': f'Missing key: {str(e)}'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    else:
        return JsonResponse({'status': 'error', 'message': 'Only POST method is allowed.'}, status=405)   
    
#단기해상예보조회
@csrf_exempt
def store_fine_fct_ocean_forecast_view(request):
    print("store_fine_fct_ocean_forecast_view")
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # JSON 데이터 파싱
            # 모델 인스턴스 생성
            print(data.get('regIdIndex', ''))
            print(data)
            term_forecast = WeatherShtTermOceanForecast(
                regIdIndex = data.get('regIdIndex', ''),
                regId = data.get('regId', None),  # 기본 키로 설정
                tmFc = data.get('tmFc', None),
                tmEf = data.get('tmEf', None),
                mod = data.get('mod', None),
                ne = data.get('ne', None),
                stn = data.get('stn', None),
                c = data.get('c', None),
                manId = data.get('manId', None),
                manFc = data.get('manFc', None),
                w1 = data.get('w1', None),
                t = data.get('t', None),
                w2 = data.get('w2', None),
                s1 = data.get('s1', None),
                s2 = data.get('s2', None),
                wh1 = data.get('wh1', None),
                wh2 = data.get('wh2', None),                
                sky = data.get('sky', None),
                prep = data.get('prep', None),
                wf = data.get('wf', None),
            )
            term_forecast.save()  

            return JsonResponse({'status': 'success', 'message': 'Weather data saved successfully.'})
        except KeyError as e:
            return JsonResponse({'status': 'error', 'message': f'Missing key: {str(e)}'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    else:
        return JsonResponse({'status': 'error', 'message': 'Only POST method is allowed.'}, status=405)   
    
#단기예보 코드조회
@csrf_exempt
def store_fine_fct_station_code_view(request):
    print("store_fine_fct_station_code_view")
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # JSON 데이터 파싱
            print(data)
            # 모델 인스턴스 생성
            term_forecast = WeatherShtTermCode(
                regId = data.get('regId', None),  # 기본 키로 설정
                tmSt = data.get('tmSt', None),
                tmEd = data.get('tmEd', None),
                regSp = data.get('regSp', None),
                regName = data.get('regName', None),
            )
            
            print(request)

            term_forecast.save()  
            return JsonResponse({'status': 'success', 'message': 'Weather data saved successfully.'})
        except KeyError as e:
            return JsonResponse({'status': 'error', 'message': f'Missing key: {str(e)}'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    else:
        return JsonResponse({'status': 'error', 'message': 'Only POST method is allowed.'}, status=405)   
    
#중기 기온 예보 코드조회
@csrf_exempt
def store_fine_fct_mid_land_Temp_forecast_view(request):
    print("store_fine_mid_land_Temp_forecast")
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # JSON 데이터 파싱
            print(data)
            term_forecast = WeatherMidTermLandTempForecast(
                regIdIndex = data.get('regIdIndex', None), # 기본 키로 설정
                regId = data.get('regId', None),   
                tmFc = data.get('tmFc', None), 
                tmEf = data.get('tmEf', None), 
                mod = data.get('mod', None), 
                stn = data.get('stn', None), 
                c = data.get('c', None), 
                manId = data.get('manId', None), 
                manFc = data.get('manFc', None), 
                regName = data.get('regName', None), 
                min = data.get('min', None), 
                max = data.get('max', None), 
                minL = data.get('minL', None), 
                minH = data.get('minH', None), 
                maxL = data.get('maxL', None), 
                maxH = data.get('maxH', None), 
            )
            term_forecast.save()  

            return JsonResponse({'status': 'success', 'message': 'Weather data saved successfully.'})
        except KeyError as e:
            return JsonResponse({'status': 'error', 'message': f'Missing key: {str(e)}'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    else:
        return JsonResponse({'status': 'error', 'message': 'Only POST method is allowed.'}, status=405)   

#중기 날씨 예보 코드조회
@csrf_exempt
def store_fine_fct_mid_land_Status_forecast_view(request):
    print("store_fine_fct_mid_land_Status_forecast")
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # JSON 데이터 파싱
            
            term_forecast = WeatherMidTermLandStatusForecast(
                regIdIndex = data.get('regIdIndex', None), # 기본 키로 설정
                regId = data.get('regId', None),   
                tmFc = data.get('tmFc', None), 
                tmEf = data.get('tmEf', None), 
                mod = data.get('mod', None), 
                stn = data.get('stn', None), 
                c = data.get('c', None), 
                manId = data.get('manId', None), 
                manFc = data.get('manFc', None), 
                regName = data.get('regName', None), 
                sky = data.get('sky', None),
                pre = data.get('pre', None),
                conf = data.get('conf', None),
                wf = data.get('wf', None),
                rnSt = data.get('rnSt', None),
            )
            term_forecast.save()  

            return JsonResponse({'status': 'success', 'message': 'Weather data saved successfully.'})
        except KeyError as e:
            return JsonResponse({'status': 'error', 'message': f'Missing key: {str(e)}'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    else:
        return JsonResponse({'status': 'error', 'message': 'Only POST method is allowed.'}, status=405)   
    
#특보 조회
@csrf_exempt
def store_fine_fct_alert_view(request):
    print("store_fine_fct_alert_view")
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # JSON 데이터 파싱
            
            term_forecast = WeatherAlertForecast(
                
                regIdWrn = data.get('regIdWrn', None), 
                regUp = data.get('regUp', None),                 
                regUpKo = data.get('regUpKo', None), 
                regId = data.get('regId', None), 
                regKo = data.get('regKo', None), 
                tmFc = data.get('tmFc', None), 
                tmEf = data.get('tmEf', None), 
                apiTime = data.get('apiTime', None), 
                wrn = data.get('wrn', None),
                lvl = data.get('lvl', None),
                cmd = data.get('cmd', None),
                edTm = data.get('edTm', None),
            )
            term_forecast.save()  

            return JsonResponse({'status': 'success', 'message': 'Weather data saved successfully.'})
        except KeyError as e:
            return JsonResponse({'status': 'error', 'message': f'Missing key: {str(e)}'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    else:
        return JsonResponse({'status': 'error', 'message': 'Only POST method is allowed.'}, status=405)   
    

#AWS 1시간 기온
@csrf_exempt
def store_obs_aws_1hr(request):
    print("store_obs_aws_1hr_View")
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # JSON 데이터 파싱
            # 모델 인스턴스 생성
            term_forecast = WeatherAws1Mobservation(
                tmKstStn = data.get('tmKstStn', ''),
                tmKst = data.get('tmKst', None),  # 기본 키로 설정
                stnId = data.get('stnId', None),
                ta = data.get('ta', None),
                wd = data.get('wd', None),
                ws = data.get('ws', None),
                rnDay = data.get('rnDay', None),
                rnHr1 = data.get('rnHr1', None),
                Hm = data.get('Hm', None),
                PA = data.get('PA', None),
                PS = data.get('PS', None),
            )
            term_forecast.save()  

            return JsonResponse({'status': 'success', 'message': 'Weather data saved successfully.'})
        except KeyError as e:
            return JsonResponse({'status': 'error', 'message': f'Missing key: {str(e)}'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    else:
        return JsonResponse({'status': 'error', 'message': 'Only POST method is allowed.'}, status=405)   

#AWS 지점 정보
@csrf_exempt
def store_stn_aws(request):
    print("store_stn_aws")

    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # JSON 데이터 파싱
            # 모델 인스턴스 생성
            term_forecast = WeatherAwsStnInfo(
                stnIdKO = data.get('stnIdKO', ''),
                stnId = data.get('stnId', None),
                lon = data.get('lon', None),
                lat = data.get('lat', None),
                stnSp = data.get('stnSp', None),
                ht = data.get('ht', None),
                htWd = data.get('htWd', None),
                stnKo = data.get('stnKo', None),
            )
            term_forecast.save()  

            return JsonResponse({'status': 'success', 'message': 'Weather data saved successfully.'})
        except KeyError as e:
            return JsonResponse({'status': 'error', 'message': f'Missing key: {str(e)}'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    else:
        return JsonResponse({'status': 'error', 'message': 'Only POST method is allowed.'}, status=405)   
