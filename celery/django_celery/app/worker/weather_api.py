from xml.dom.minidom import parseString
import xml.etree.ElementTree as ET
import requests
import json
import time
import csv
import xmltodict
from datetime import datetime, timedelta
import pandas as pd
import os
import logging
from celery.exceptions import Ignore


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        

class WeatherAPI:
    def __init__(self, api_endpoints, service_key):
        self.api_endpoints = api_endpoints
        self.service_key = service_key
        
    @staticmethod
    def load_api_config(file_path):
        """Loads API configuration from a JSON file."""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        full_path = os.path.join(current_dir, file_path)
        with open(full_path, 'r') as file:
            return json.load(file)["apiEndpoints"]
        
    @staticmethod
    def load_service_key(file_path):
        """Loads service keys from a JSON file."""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        full_path = os.path.join(current_dir, file_path)
        with open(full_path, 'r') as file:
            
            return json.load(file)

    def data_by_shot_forecast(self, endpoint_name, nx, ny):
        now = datetime.now()
        base_date = now.strftime('%Y%m%d')
        base_time = now.strftime('%H%M')
        adjusted_time = now - timedelta(minutes=30)
        minute = adjusted_time.minute - (adjusted_time.minute % 30)
        rounded_time = adjusted_time.replace(minute=minute, second=0, microsecond=0).strftime('%H%M')
        
        if endpoint_name == '초단기실황조회':
            print("초단기실황조회")
            for endpoint in self.api_endpoints:
                if endpoint['name'] == endpoint_name:
                    url = endpoint['url']
                    params = endpoint['params'].copy()
                    params['serviceKey'] = self.service_key  # Make sure this is the correct key
                    params['base_date'] = base_date
                    params['base_time'] = rounded_time
                    params['nx'] = nx
                    params['ny'] = ny                    
                    time.sleep(1)
                    print(rounded_time)
                    
                    response = requests.get(url, params=params)
                    response.raise_for_status()  # Raises an HTTPError for bad responses
                    # Successful response handling
                    # formatted_response = json.dumps(response.json(), indent=4, ensure_ascii=False)
                    # print(formatted_response)
                    return response.json()
                        
        # 실행시 20분 소요 매시간 30분 기준으로 데이터를 받을수있다. 
        # 현재시간 기준으로 
        # 에러 2개 발생 슬립 0.2
        elif endpoint_name == '초단기예보조회':
            print("초단기예보조회")
            for endpoint in self.api_endpoints:
                if endpoint['name'] == endpoint_name:
                    url = endpoint['url']
                    params = endpoint['params'].copy()
                    params['serviceKey'] = self.service_key  # Make sure this is the correct key
                    params['base_date'] = base_date
                    params['base_time'] = rounded_time
                    params['nx'] = nx
                    params['ny'] = ny
                    time.sleep(1)
                    print(rounded_time)
                          
                    # print(base_date, thirty_minutes_earlier, nx, ny)
                    # print(base_date, thirty_minutes_earlier, nx, ny)
                    # print(base_date, thirty_minutes_earlier, nx, ny)
                    
                    response = requests.get(url, params=params)
                    response.raise_for_status()  # Raises an HTTPError for bad responses
                    # Successful response handling
                    # formatted_response = json.dumps(response.json(), indent=4, ensure_ascii=False)
                    # print(formatted_response)
                    return response.json()
                        
        #base_time 0500 고정
        #슬립 0.2에 여섯개 에러 발생
        elif endpoint_name == '단기예보조회':
            print("단기예보조회")
            for endpoint in self.api_endpoints:
                if endpoint['name'] == endpoint_name:
                    url = endpoint['url']
                    params = endpoint['params'].copy()
                    params['serviceKey'] = self.service_key  # Make sure this is the correct key
                    params['base_date'] = base_date
                    params['base_time'] = '0500'
                    params['nx'] = nx
                    params['ny'] = ny
                    # print(base_date, base_time, nx, ny)
                    time.sleep(1)
                    
                    response = requests.get(url, params=params)
                    response.raise_for_status()  # Raises an HTTPError for bad responses
                    # Successful response handling
                    # formatted_response = json.dumps(response.json(), indent=4, ensure_ascii=False)
                    # print(formatted_response)
                    return response.json()
                        
    def fetch_forecast_data_version(self, forecast_type, base_date, base_time):

        endpoint_name = '예보버전조회'  # Adjusted to match the provided example
        for endpoint in self.api_endpoints:
            if endpoint['name'] == endpoint_name:
                url = endpoint['url']
                params = endpoint['params'].copy()
                params['serviceKey'] = self.service_key
                params['basedatetime'] = base_date + base_time
                
                # Setting ftype based on forecast_type parameter
                if forecast_type == 'ODAM':  # 동네예보실황
                    params['ftype'] = 'ODAM'  
                    print("ODAM")
                elif forecast_type == 'VSRT':  # 동네예보초단기
                    params['ftype'] = 'VSRT'  
                    print("VSRT")
                elif forecast_type == 'SHRT':  #동네예보단기
                    params['ftype'] = 'SHRT'  
                    params['basedatetime'] =  base_date + '0500'
                    print("SHRT")
                else:
                    print(f"Invalid forecast type: {forecast_type}")
                    return

                try:
                    response = requests.get(url, params=params)
                    response.raise_for_status()  # Raises an HTTPError for bad responses
                    # Successful response handling
                    formatted_response = json.dumps(response.json(), indent=4, ensure_ascii=False)
                    # print(formatted_response)

                    return response.json()

                except requests.HTTPError as http_err:
                    print(f"HTTP error occurred: {http_err}")
                except Exception as err:
                    print(f"An error occurred: {err}")
                break  # Exit the loop after finding and processing the matching endpoint

        else:
            # This else block executes if no break occurs, meaning no matching endpoint was found
            print(f"No endpoint found with the name: {endpoint_name}")


    # 일 0600, 1800 두번 호출 할수있다. 
    def fetch_data_by_mid(self, endpoint_name, base_date, base_time, local, code):

            if base_time == '0700':
                base_time = '0600'                
            elif base_time == '1900':
                base_time = '1800'

            if endpoint_name == '중기기온조회':
                print("중기기온조회")
                for endpoint in self.api_endpoints:
                    if endpoint['name'] == endpoint_name:
                        url = endpoint['url']
                        params = endpoint['params'].copy()
                        params['serviceKey'] = self.service_key  # Make sure this is the correct key
                        params['regId'] = code
                        params['tmFc'] =  '202402280600'
                        # params['tmFc'] =  base_date+base_time

                        time.sleep(1)
                        # print(base_date, base_time, code)
                        
                        try:
                            response = requests.get(url, params=params)
                            response.raise_for_status()  # Raises an HTTPError for bad responses
                            # Successful response handling
                            data = response.json()
                            items = data['response']['body']['items']['item']
                            filtered_data_dict = {}

                            for item in items:
                                filtered_data_dict = {
                                    "regId": item['regId'],
                                    "taMin3": item['taMin3'],
                                    "taMax3": item['taMax3'],
                                    "taMin4": item['taMin4'],
                                    "taMax4": item['taMax4'],
                                    "taMin5": item['taMin5'],
                                    "taMax5": item['taMax5'],
                                    "taMin6": item['taMin6'],
                                    "taMax6": item['taMax6'],
                                    "taMin7": item['taMin7'],
                                    "taMax7": item['taMax7'],
                                    "taMin8": item['taMin8'],
                                    "taMax8": item['taMax8'],
                                    "taMin9": item['taMin9'],
                                    "taMax9": item['taMax9'],
                                    "taMin10": item['taMin10'],
                                    "taMax10": item['taMax10']
                                }

                            formatted_response = json.dumps(filtered_data_dict, indent=4, ensure_ascii=False)
                            print(formatted_response)
                            return filtered_data_dict
                            # return response.json()
                        
                        except requests.HTTPError as http_err:
                            print(f"HTTP error occurred: {http_err}")
                            filename = f"{local},{code}_error.csv"
                            with open(filename, mode='w', newline='', encoding='utf-8') as file:
                                writer = csv.writer(file)
                                # Write the headers and the error message
                                writer.writerow(['Error'])
                                writer.writerow([str(err)])
                            print(f"An error occurred and has been written to {filename}")
                        except Exception as err:
                            print(f"An error occurred: {err}")
                            print(f"An error occurred and has been written to {filename}")
                            
                        break  # Exit the loop after finding and processing the matching endpoint
            
            elif endpoint_name == '중기육상예보조회':
                print("중기육상예보조회")
                for endpoint in self.api_endpoints:
                    if endpoint['name'] == endpoint_name:
                        url = endpoint['url']
                        params = endpoint['params'].copy()
                        params['serviceKey'] = self.service_key  # Make sure this is the correct key
                        params['regId'] = code
                        params['tmFc'] =  '202402280600'

                        time.sleep(0.5)
                        print(base_date, code)
                        
                        try:
                            response = requests.get(url, params=params)
                            response.raise_for_status()  # Raises an HTTPError for bad responses
                            # Successful response handling
                            data = response.json()
                            items = data['response']['body']['items']['item']
                            filtered_data_dict = {}

                            for item in items:
                                filtered_data_dict = {
                                    "regId": item['regId'],
                                    "rnSt3Am": item['rnSt3Am'],
                                    "rnSt3Pm": item['rnSt3Pm'],
                                    "rnSt4Am": item['rnSt4Am'],
                                    "rnSt4Pm": item['rnSt4Pm'],
                                    "rnSt5Am": item['rnSt5Am'],
                                    "rnSt5Pm": item['rnSt5Pm'],
                                    "rnSt6Am": item['rnSt6Am'],
                                    "rnSt6Pm": item['rnSt6Pm'],
                                    "rnSt7Am": item['rnSt7Am'],
                                    "rnSt7Pm": item['rnSt7Pm'],
                                    "rnSt8": item.get('rnSt8', 0),
                                    "rnSt9": item.get('rnSt9', 0),
                                    "rnSt10": item.get('rnSt10', 0),
                                    "wf3Am": item['wf3Am'],
                                    "wf3Pm": item['wf3Pm'],
                                    "wf4Am": item['wf4Am'],
                                    "wf4Pm": item['wf4Pm'],
                                    "wf5Am": item['wf5Am'],
                                    "wf5Pm": item['wf5Pm'],
                                    "wf6Am": item['wf6Am'],
                                    "wf6Pm": item['wf6Pm'],
                                    "wf7Am": item['wf7Am'],
                                    "wf7Pm": item['wf7Pm'],
                                    "wf8": item['wf8'],
                                    "wf9": item['wf9'],
                                    "wf10": item['wf10']
                                }

                            formatted_response = json.dumps(filtered_data_dict, indent=4, ensure_ascii=False)
                            print(formatted_response)
                            return filtered_data_dict
                        
                        except requests.HTTPError as http_err:
                            print(f"HTTP error occurred: {http_err}")
                            filename = f"{local},{code}_error.csv"
                            with open(filename, mode='w', newline='', encoding='utf-8') as file:
                                writer = csv.writer(file)
                                # Write the headers and the error message
                                writer.writerow(['Error'])
                                writer.writerow([str(err)])
                            print(f"An error occurred and has been written to {filename}")
                        except Exception as err:
                            print(f"An error occurred: {err}")
                            filename = f"{local},{code}_error.csv"
                            with open(filename, mode='w', newline='', encoding='utf-8') as file:
                                writer = csv.writer(file)
                                # Write the headers and the error message
                                writer.writerow(['Error'])
                                writer.writerow([str(err)])
                            print(f"An error occurred and has been written to {filename}")
                            
                        break  # Exit the loop after finding and processing the matching endpoint
            
            elif endpoint_name == '중기전망조회':
                print("중기전망조회")
                for endpoint in self.api_endpoints:
                    if endpoint['name'] == endpoint_name:
                        url = endpoint['url']
                        params = endpoint['params'].copy()
                        params['serviceKey'] = self.service_key  # Make sure this is the correct key
                        params['regId'] = code
                        params['tmFc'] =  '202402121800'

                        time.sleep(0.2)
                        print(base_date, local, code)
                        
                        try:
                            response = requests.get(url, params=params)
                            response.raise_for_status()  # Raises an HTTPError for bad responses
                            # Successful response handling
                            formatted_response = json.dumps(response.json(), indent=4, ensure_ascii=False)
                            print(formatted_response)
                            return response.json()
                        
                        except requests.HTTPError as http_err:
                            print(f"HTTP error occurred: {http_err}")
                            filename = f"{local},{code}_error.csv"
                            with open(filename, mode='w', newline='', encoding='utf-8') as file:
                                writer = csv.writer(file)
                                # Write the headers and the error message
                                writer.writerow(['Error'])
                                writer.writerow([str(err)])
                            print(f"An error occurred and has been written to {filename}")
                        except Exception as err:
                            print(f"An error occurred: {err}")
                            filename = f"{local},{code}_error.csv"
                            with open(filename, mode='w', newline='', encoding='utf-8') as file:
                                writer = csv.writer(file)
                                # Write the headers and the error message
                                writer.writerow(['Error'])
                                writer.writerow([str(err)])
                            print(f"An error occurred and has been written to {filename}")
                            
                        break  # Exit the loop after finding and processing the matching endpoint
            
            elif endpoint_name == '중기해상예보조회':
                print("중기해상예보조회")
                for endpoint in self.api_endpoints:
                    if endpoint['name'] == endpoint_name:
                        url = endpoint['url']
                        params = endpoint['params'].copy()
                        params['serviceKey'] = self.service_key  # Make sure this is the correct key
                        params['regId'] = code
                        params['tmFc'] =  '202402121800'

                        time.sleep(0.2)
                        print(base_date, local, code)
                        
                        try:
                            response = requests.get(url, params=params)
                            response.raise_for_status()  # Raises an HTTPError for bad responses
                            # Successful response handling
                            formatted_response = json.dumps(response.json(), indent=4, ensure_ascii=False)
                            print(formatted_response)
                            return response.json()
                        
                        except requests.HTTPError as http_err:
                            print(f"HTTP error occurred: {http_err}")
                            filename = f"{local},{code}_error.csv"
                            with open(filename, mode='w', newline='', encoding='utf-8') as file:
                                writer = csv.writer(file)
                                # Write the headers and the error message
                                writer.writerow(['Error'])
                                writer.writerow([str(err)])
                            print(f"An error occurred and has been written to {filename}")
                        except Exception as err:
                            print(f"An error occurred: {err}")
                            filename = f"{local},{code}_error.csv"
                            with open(filename, mode='w', newline='', encoding='utf-8') as file:
                                writer = csv.writer(file)
                                # Write the headers and the error message
                                writer.writerow(['Error'])
                                writer.writerow([str(err)])
                            print(f"An error occurred and has been written to {filename}")
                            
                        break  # Exit the loop after finding and processing the matching endpoint
            
    def sunrise_sunset_data(self, endpoint_name, location):
        endpoint_name = '지역별해달출몰시각정보조회'  
        current_data = datetime.now().date()
        formatted_date = current_data.strftime('%Y%m%d')
        print(endpoint_name, location, formatted_date)
        for endpoint in self.api_endpoints:
            if endpoint['name'] == endpoint_name:
                url = endpoint['url']
                params = endpoint['params'].copy()
                params['serviceKey'] = self.service_key
                params['locdate'] = formatted_date
                params['location'] = location
                time.sleep(1)
                
                try:
                    response = requests.get(url, params=params)
                    response.raise_for_status()  # Raises an HTTPError for bad responses
                    # Successful response handling
                    xml_dict = xmltodict.parse(response.content)
                    item = xml_dict['response']['body']['items']['item']
                    filtered_data = {
                        "latitude": item.get('latitude'),
                        "latitudeNum": item.get('latitudeNum'),
                        "location": item.get('location'),
                        "locdate": item.get('locdate'),
                        "longitude": item.get('longitude'),
                        "longitudeNum": item.get('longitudeNum'),
                        "sunrise": item.get('sunrise'),
                        "sunset": item.get('sunset')
                    }
                    
                    json_str = json.dumps(filtered_data, ensure_ascii=False, indent=4)
                    print(json_str)
                    return filtered_data

                except requests.HTTPError as http_err:
                    # Create a DataFrame with error details
                    df = pd.DataFrame({'Error Type': ['HTTPError'], 'Error Message': [str(http_err)]})
                    # Create CSV file named after the location with the error details
                    csv_file_name = f"{location}_error.csv"
                    df.to_csv(csv_file_name, index=False, encoding='utf-8-sig')
                    print(f'HTTP error occurred: {http_err}. Details saved to {csv_file_name}')

                except Exception as err:
                    # Create a DataFrame with error details
                    df = pd.DataFrame({'Error Type': ['Exception'], 'Error Message': [str(err)]})
                    # Create CSV file named after the location with the error details
                    csv_file_name = f"{location}_error.csv"
                    df.to_csv(csv_file_name, index=False, encoding='utf-8-sig')
                    print(f'Other error occurred: {err}. Details saved to {csv_file_name}')
                break  # Exit the loop after finding and processing the matching endpoint

        else:
            # This else block executes if no break occurs, meaning no matching endpoint was found
            print(f"No endpoint found with the name: {endpoint_name}")