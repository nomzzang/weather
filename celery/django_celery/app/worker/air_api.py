import requests
import json
import time
import csv
import pandas as pd
from datetime import datetime
from data_sender import send_data_to_endpoint




class AirAPI:
    def __init__(self, api_endpoints, service_key):
        self.api_endpoints = api_endpoints
        self.service_key = service_key

    def dust_station_list(self, endpoint_name):
        if endpoint_name == '측정소목록조회':
            print("측정소목록조회")
            for endpoint in self.api_endpoints:
                if endpoint['name'] == endpoint_name:
                    url = endpoint['url']
                    params = endpoint['params'].copy()
                    params['serviceKey'] = self.service_key  # Make sure this is the correct key
                    time.sleep(0.2)

                    response = requests.get(url, params=params)
                    data = response.json()
                    df = pd.json_normalize(data['response']['body']['items'])
                    df.to_csv("dust_station_list.csv", index=False, encoding='utf-8=sig')
        
        elif endpoint_name == '근접측정소목록조회':
            print("근접측정소목록조회")
            for endpoint in self.api_endpoints:
                if endpoint['name'] == endpoint_name:
                    url = endpoint['url']
                    params = endpoint['params'].copy()
                    params['serviceKey'] = self.service_key  # Make sure this is the correct key
                    time.sleep(0.2)

                    response = requests.get(url, params=params)
                    data = response.json()
                    df = pd.json_normalize(data['response']['body']['items'])
                    df.to_csv("dust_near_station_list.csv", index=False, encoding='utf-8=sig')

        elif endpoint_name == 'TM기준좌표조회':
            print("TM기준좌표조회")
            for endpoint in self.api_endpoints:
                if endpoint['name'] == endpoint_name:
                    url = endpoint['url']
                    params = endpoint['params'].copy()
                    params['serviceKey'] = self.service_key  # Make sure this is the correct key
                    time.sleep(0.2)

                    response = requests.get(url, params=params)
                    data = response.json()
                    df = pd.json_normalize(data['response']['body']['items'])
                    df.to_csv("dust_umd_station_list.csv", index=False, encoding='utf-8=sig')

    def dust_info_forecast_name(self, endpoint_name):
        if endpoint_name == '대기질예보통보조회':
            print("대기질예보통보조회")
            for endpoint in self.api_endpoints:
                if endpoint['name'] == endpoint_name:
                    url = endpoint['url']
                    params = endpoint['params'].copy()
                    params['serviceKey'] = self.service_key  
                    today = datetime.now().strftime('%Y-%m-%d')
                    params['searchDate'] = today
                    params['InformCode'] = ''
                    time.sleep(0.5)
                    inform_codes = ['PM10', 'PM25']
                    # responses = {}
                    # for code in inform_codes:
                    #     params['InformCode'] = code
                    #     print(code)
                    
                    try:
                        response = requests.get(url, params=params)
                        response.raise_for_status()  # 오류가 있을 경우 예외 발생
                        
                        # print(json.dumps(response.json(), indent=4, ensure_ascii=False))
                        # 성공적인 응답 처리
                        data = response.json()  # JSON 데이터 로드
                        # print(json.dumps(data, indent=4, ensure_ascii=False))
                        items = data['response']['body']['items']  # 'items' 리스트에 접근
                        # 필요한 정보만 추출하여 딕셔너리에 저장
                        filtered_responses = {}
                        for item in items:
                            inform_data = item['informData']
                            inform_code = item['informCode']

                            # informData 별로 informCode를 키로 갖는 딕셔너리를 생성
                            if inform_data not in filtered_responses:
                                filtered_responses[inform_data] = {}

                            # informCode 별로 데이터 저장
                            filtered_responses[inform_data][inform_code] = {
                                'informCause': item['informCause'],
                                'informOverall': item['informOverall'],
                                'informData': item['informData'],
                                'informGrade': {region.strip(): grade.strip() for region, grade in (grade_pair.split(':') for grade_pair in item['informGrade'].split(','))},
                                'dataTime': item['dataTime'],
                            }

                        # 필터링된 응답 출력
                        print(json.dumps(filtered_responses, indent=4, ensure_ascii=False))
                        send_data_to_endpoint('store_air_quality_forecast', filtered_responses)  # 수정된 부분
                    
                        
                    except requests.HTTPError as http_err:
                        print(f"HTTP error occurred: {http_err}")
                        # filename = f"{code}_error.csv"
                        with open(filename, mode='w', newline='', encoding='utf-8=sig') as file:
                            writer = csv.writer(file)
                            # Write the headers and the error message
                            writer.writerow(['Error'])
                            writer.writerow([str(err)])
                        print(f"An error occurred and has been written to {filename}")

                    except Exception as err:
                        print(f"An error occurred: {err}")
                        # filename = f"{code}_error.csv"
                        with open(filename, mode='w', newline='', encoding='utf-8=sig') as file:
                            writer = csv.writer(file)
                            # Write the headers and the error message
                            writer.writerow(['Error'])
                            writer.writerow([str(err)])
                        print(f"An error occurred and has been written to {filename}")
                                
                # return filtered_responses

        elif endpoint_name == '초미세먼지주간예보조회':
            print("초미세먼지주간예보조회")
            for endpoint in self.api_endpoints:
                if endpoint['name'] == endpoint_name:
                    url = endpoint['url']
                    params = endpoint['params'].copy()
                    today = datetime.now().strftime('%Y-%m-%d')
                    params['searchDate'] = today
                    params['serviceKey'] = self.service_key

                    try:
                        response = requests.get(url, params=params)
                        response.raise_for_status()
                        data = response.json()
                        items = data['response']['body']['items']
                        
                        filtered_responses = {}
                        for item in items:
                            presnatnDt = item['presnatnDt']
                            # 각 날짜별 예보 정보를 딕셔너리에 저장
                            filtered_responses[presnatnDt] = {
                                'frcstOneCn': {region.strip(): grade.strip() for region, grade in (grade_pair.split(':') for grade_pair in item['frcstOneCn'].split(','))},
                                'frcstTwoCn': {region.strip(): grade.strip() for region, grade in (grade_pair.split(':') for grade_pair in item['frcstTwoCn'].split(','))},
                                'frcstThreeCn': {region.strip(): grade.strip() for region, grade in (grade_pair.split(':') for grade_pair in item['frcstThreeCn'].split(','))},
                                'frcstFourCn': {region.strip(): grade.strip() for region, grade in (grade_pair.split(':') for grade_pair in item['frcstFourCn'].split(','))},
                            }
                        
                        print(json.dumps(filtered_responses, indent=4, ensure_ascii=False))
                        send_data_to_endpoint('store_fine_dust_weekly_forecast', filtered_responses)
                    
                    except requests.HTTPError as http_err:
                        print(f"HTTP error occurred: {http_err}")
                        filename = "초미세먼지주간예보_error.csv"
                        with open(filename, mode='w', newline='', encoding='utf-8') as file:
                            writer = csv.writer(file)
                            # Write the headers and the error message
                            writer.writerow(['Error'])
                            writer.writerow([str(err)])
                        print(f"An error occurred and has been written to {filename}")
                    except Exception as err:
                        print(f"An error occurred: {err}")
                        filename = "초미세먼지주간예보_error.csv"
                        with open(filename, mode='w', newline='', encoding='utf-8') as file:
                            writer = csv.writer(file)
                            # Write the headers and the error message
                            writer.writerow(['Error'])
                            writer.writerow([str(err)])
                        print(f"An error occurred and has been written to {filename}")
                        
                    break  # Exit the loop after finding and processing the matching endpoint

        elif endpoint_name == '통합대기환경지수나쁨이상측정소목록조회':
            print("통합대기환경지수나쁨이상측정소목록조회")
            for endpoint in self.api_endpoints:
                if endpoint['name'] == endpoint_name:
                    url = endpoint['url']
                    params = endpoint['params'].copy()
                    params['serviceKey'] = self.service_key  # Make sure this is the correct key
                    time.sleep(0.2)

                    try:
                        response = requests.get(url, params=params)
                        response.raise_for_status()  # Raises an HTTPError for bad responses
                        # Successful response handling
                        formatted_response = json.dumps(response.json(), indent=4, ensure_ascii=False)
                        print(formatted_response)
                        return response.json()
                    
                    except requests.HTTPError as http_err:
                        print(f"HTTP error occurred: {http_err}")
                        filename = "통합대기환경지수나쁨이상측정소목록조회_err.csv"
                        with open(filename, mode='w', newline='', encoding='utf-8') as file:
                            writer = csv.writer(file)
                            # Write the headers and the error message
                            writer.writerow(['Error'])
                            writer.writerow([str(err)])
                        print(f"An error occurred and has been written to {filename}")
                    except Exception as err:
                        print(f"An error occurred: {err}")
                        filename = "통합대기환경지수나쁨이상측정소목록조회_err.csv"
                        with open(filename, mode='w', newline='', encoding='utf-8') as file:
                            writer = csv.writer(file)
                            # Write the headers and the error message
                            writer.writerow(['Error'])
                            writer.writerow([str(err)])
                        print(f"An error occurred and has been written to {filename}")
                        
                    break  # Exit the loop after finding and processing the matching endpoint
        
        elif endpoint_name == '미세먼지경보현황정보조회':
            print("미세먼지경보현황정보조회")
            for endpoint in self.api_endpoints:
                if endpoint['name'] == endpoint_name:
                    url = endpoint['url']
                    params = endpoint['params'].copy()
                    params['serviceKey'] = self.service_key  # Make sure this is the correct key
                    time.sleep(0.2)

                    try:
                        response = requests.get(url, params=params)
                        response.raise_for_status()  # Raises an HTTPError for bad responses
                        # Successful response handling
                        formatted_response = json.dumps(response.json(), indent=4, ensure_ascii=False)
                        print(formatted_response)
                        return response.json()
                    
                    except requests.HTTPError as http_err:
                        print(f"HTTP error occurred: {http_err}")
                        filename = "미세먼지경보현황정보조회.csv"
                        with open(filename, mode='w', newline='', encoding='utf-8') as file:
                            writer = csv.writer(file)
                            # Write the headers and the error message
                            writer.writerow(['Error'])
                            writer.writerow([str(err)])
                        print(f"An error occurred and has been written to {filename}")
                    except Exception as err:
                        print(f"An error occurred: {err}")
                        filename = "미세먼지경보현황정보조회.csv"
                        with open(filename, mode='w', newline='', encoding='utf-8') as file:
                            writer = csv.writer(file)
                            # Write the headers and the error message
                            writer.writerow(['Error'])
                            writer.writerow([str(err)])
                        print(f"An error occurred and has been written to {filename}")
                        
                    break  # Exit the loop after finding and processing the matching endpoint
        
        
        
        #655 개소 데이터 
    def dust_real_forecast_name(self, endpoint_name, list):
        print("측정소별실시간측정정보조회")
        for endpoint in self.api_endpoints:
            if endpoint['name'] == endpoint_name:
                url = endpoint['url']
                params = endpoint['params'].copy()
                params['serviceKey'] = self.service_key  # Make sure this is the correct key
                params['stationName'] = list
                time.sleep(0.3)
                er_list = []
                print(er_list)
                try:
                    response = requests.get(url, params=params)
                    response.raise_for_status()  # Raises an HTTPError for bad responses
                    # Successful response handling
                    formatted_response = json.dumps(response.json(), indent=4, ensure_ascii=False)
                    # print(formatted_response)
                    return response.json()
                
                except requests.HTTPError as http_err:
                    print(f"HTTP error occurred: {http_err}")
                    print(f"An error occurred and has been written to {list}")
                    filename = f"{list}_error.csv"
                    with open(filename, mode='w', newline='', encoding='utf-8') as file:
                        writer = csv.writer(file)
                        # Write the headers and the error message
                        writer.writerow(['Error'])
                        writer.writerow([str(err)])
                except Exception as err:
                    print(f"An error occurred: {err}")
                    print(f"An error occurred and has been written to {list}")
                    filename = f"{list}_error.csv"
                    with open(filename, mode='w', newline='', encoding='utf-8') as file:
                        writer = csv.writer(file)
                        # Write the headers and the error message
                        writer.writerow(['Error'])
                        writer.writerow([str(err)])
                
                break  # Exit the loop after finding and processing the matching endpoint
    
    #시도별 실시간 측정정보조회
    def dust_real_sidoname(self, endpoint_name, sidoname):
        print("시도별실시간측정정보조회")
        print(sidoname)

        for endpoint in self.api_endpoints:
                if endpoint['name'] == endpoint_name:
                    url = endpoint['url']
                    params = endpoint['params'].copy()
                    params['sidoname'] = sidoname
                    params['serviceKey'] = self.service_key  # Make sure this is the correct key
                    time.sleep(0.2)

                    try:
                        response = requests.get(url, params=params)
                        response.raise_for_status()  # Raises an HTTPError for bad responses
                        # Successful response handling
                        formatted_response = json.dumps(response.json(), indent=4, ensure_ascii=False)
                        return response.json()
                    
                    except requests.HTTPError as http_err:
                        print(f"HTTP error occurred: {http_err}")
                        filename = "미세먼지경보현황정보조회.csv"
                        with open(filename, mode='w', newline='', encoding='utf-8') as file:
                            writer = csv.writer(file)
                            # Write the headers and the error message
                            writer.writerow(['Error'])
                            writer.writerow([str(err)])
                        print(f"An error occurred and has been written to {filename}")
                    except Exception as err:
                        print(f"An error occurred: {err}")
                        filename = "미세먼지경보현황정보조회.csv"
                        with open(filename, mode='w', newline='', encoding='utf-8') as file:
                            writer = csv.writer(file)
                            # Write the headers and the error message
                            writer.writerow(['Error'])
                            writer.writerow([str(err)])
                        print(f"An error occurred and has been written to {filename}")
                        
                    break  # Exit the loop after finding and processing the matching endpoint