import requests
import json
import csv
from datetime import datetime, timedelta
from .data_sender import send_data_to_endpoint
import re

class MaxAPI:
    def __init__(self, api_endpoints, service_key):
        self.api_endpoints = api_endpoints
        self.service_key = service_key
    
    #예보 구역 코드 조회(테스트 완료)     
    def store_fct_shrt_station():
        endpoint_name = '예보 구역 코드 조회'  
        #current_data = datetime.now()
        #hour = current_data.strftime('%H')
        
        headers = {  # 헤더 설정
           'Content-Type': 'application/json'  # JSON 형식 설정
        }
        API_KEY = 'rejjPNsPRRyo4zzbD-UcDg'
        
        KMA_URL = 'https://apihub.kma.go.kr/api/typ01/url/fct_shrt_reg.php'
        param = f'tmfc=0&authKey={API_KEY}'
        try:
            url =f'{KMA_URL}?{param}'
            print(url)
            response = requests.get(url,headers=headers)
            response.raise_for_status()
            #print(response.text)
            lines = response.text.strip().split('\n')
            print(lines[10:-1])

            for line in lines[11:-1]:
                result = re.sub(r"\s+", " ", line)
                gubuns = result.split(" ")
                
                filtered_data_dict = {
                        "regId": f"{gubuns[0]}",
                        "tmSt": f"{gubuns[1]}",
                        "tmEd": f"{gubuns[2]}",
                        "regSp": f"{gubuns[3]}",
                        "regName": f"{gubuns[4]}",
                    }
                
                print(filtered_data_dict)
                print(json.dumps(filtered_data_dict, indent=4, ensure_ascii=False))
                send_data_to_endpoint('fct_shrt_station_code', filtered_data_dict)
                
        except requests.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            filename = f"예보 구역 코드_error.csv"
            with open(filename, mode='w', newline='', encoding='utf-8=sig') as file:
                writer = csv.writer(file)
                # Write the headers and the error message
                writer.writerow(['Error'])
                writer.writerow([str(err)])
            print(f"An error occurred and has been written to {filename}")

        except Exception as err:
            print(f"An error occurred: {err}")
            filename = f"예보 구역 코드_error.csv"
            with open(filename, mode='w', newline='', encoding='utf-8=sig') as file:
                writer = csv.writer(file)
                # Write the headers and the error message
                writer.writerow(['Error'])
                writer.writerow([str(err)])
            print(f"An error occurred and has been written to {filename}")    

    #단기 육상 예보 조회(테스트 완료)
    def fct_land_forecast():
        endpoint_name = '단기 육상 예보 조회'  
        #current_data = datetime.now()
        #hour = current_data.strftime('%H')
        
        now = datetime.now()
        hour = now.strftime('%H')
        yes = datetime.now() - timedelta(days=1)
        current_day = now.strftime("%Y%m%d")
        current_min = now.strftime("%Y%m%d%H%M")
        current_min = current_min[0:11]+"0"
        currentHour = now.strftime("%H%M")
        currentHour = currentHour[0:3]+"0"
        yes_day = yes.strftime("%Y%m%d")
        
        if int(hour) < 5:
            current_time = yes_day+"1700"
        elif 5<= int(hour) < 11: 
            current_time = current_day+"0500"
        elif 11<= int(hour) <15:        
            current_time = current_day+"1100"
        elif 15<= int(hour) <17:        
            current_time = current_day+"1100"
        elif 17<= int(hour):  
            current_time =current_day+"1700"
        
        
        headers = {  # 헤더 설정
           'Content-Type': 'application/json'  # JSON 형식 설정
        }
        
        API_KEY = 'rejjPNsPRRyo4zzbD-UcDg'
        KMA_URL = 'https://apihub.kma.go.kr/api/typ01/url/fct_afs_dl.php'
        
        param = f'reg=&tmfc1={current_time}&tmfc2={current_time}&disp=1&help=0&authKey={API_KEY}'
        try:
            url =f'{KMA_URL}?{param}'
            #print(url)
            response = requests.get(url,headers=headers)
            response.raise_for_status()
        
            lines = response.text.strip().split('\n')
            #print(lines[2:-1])

            for line in lines[2:-1]:
                gubuns = line.split(",")
                filtered_data_dict = {
                        "regIdIndex": f"{gubuns[0]}_{gubuns[1]}_{gubuns[4]}",
                        "regId": f"{gubuns[0]}",
                        "tmFc": f"{gubuns[1]}",
                        "tmEf": f"{gubuns[2]}",
                        "mod": f"{gubuns[3]}",
                        "ne": f"{gubuns[4]}",
                        "stn": f"{gubuns[5]}",
                        "c": f"{gubuns[6]}",
                        "manId": f"{gubuns[7]}",
                        "manFc": f"{gubuns[8]}",
                        "w1": f"{gubuns[9]}",
                        "t": f"{gubuns[10]}",
                        "w2": f"{gubuns[11]}",
                        "ta": f"{gubuns[12]}",
                        "st": f"{gubuns[13]}",
                        "sky": f"{gubuns[14]}",
                        "prep": f"{gubuns[15]}",
                        "wf": f"{gubuns[16]}",
                    }
                print(filtered_data_dict)
                print(json.dumps(filtered_data_dict, indent=4, ensure_ascii=False))
                send_data_to_endpoint('store_fct_land_forecast', filtered_data_dict)
                
        except requests.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            filename = f"단기 육상 예보_error.csv"
            with open(filename, mode='w', newline='', encoding='utf-8=sig') as file:
                writer = csv.writer(file)
                # Write the headers and the error message
                writer.writerow(['Error'])
                writer.writerow([str(err)])
            print(f"An error occurred and has been written to {filename}")

        except Exception as err:
            print(f"An error occurred: {err}")
            filename = f"단기 육상 예보_error.csv"
            with open(filename, mode='w', newline='', encoding='utf-8=sig') as file:
                writer = csv.writer(file)
                # Write the headers and the error message
                writer.writerow(['Error'])
                writer.writerow([str(err)])
            print(f"An error occurred and has been written to {filename}")

    #단기 해상 예보 조회(테스트 완료)    
    def fct_ocean_forecast():
        endpoint_name = '단기 해상 예보 조회'  
        #current_data = datetime.now()
        #hour = current_data.strftime('%H')
        
        now = datetime.now()
        hour = now.strftime('%H')
        yes = datetime.now() - timedelta(days=1)
        current_day = now.strftime("%Y%m%d")
        current_min = now.strftime("%Y%m%d%H%M")
        current_min = current_min[0:11]+"0"
        currentHour = now.strftime("%H%M")
        currentHour = currentHour[0:3]+"0"
        yes_day = yes.strftime("%Y%m%d")
        
        if int(hour) < 5:
            current_time = yes_day+"1700"
        elif 5<= int(hour) < 11: 
            current_time = current_day+"0500"
        elif 11<= int(hour) <15:        
            current_time = current_day+"1100"
        elif 15<= int(hour) <17:        
            current_time = current_day+"1100"
        elif 17<= int(hour):  
            current_time =current_day+"1700"
        
        
        headers = {  # 헤더 설정
           'Content-Type': 'application/json'  # JSON 형식 설정
        }
        API_KEY = 'rejjPNsPRRyo4zzbD-UcDg'
        
        KMA_URL = 'https://apihub.kma.go.kr/api/typ01/url/fct_afs_do.php'
        param = f'reg=&tmfc1={current_time}&tmfc2={current_time}&disp=1&help=0&authKey={API_KEY}'
        try:
            url =f'{KMA_URL}?{param}'
            #print(url)
            response = requests.get(url,headers=headers)
            response.raise_for_status()
        
            lines = response.text.strip().split('\n')
            #print(lines[2:-1])

            for line in lines[2:-1]:
                print(url)
                gubuns = line.split(",")
                filtered_data_dict = {
                        "regIdIndex": f"{gubuns[0]}_{gubuns[1]}_{gubuns[4]}",
                        "regId": f"{gubuns[0]}",
                        "tmFc": f"{gubuns[1]}",
                        "tmEf": f"{gubuns[2]}",
                        "mod": f"{gubuns[3]}",
                        "ne": f"{gubuns[4]}",
                        "stn": f"{gubuns[5]}",
                        "c": f"{gubuns[6]}",
                        "manId": f"{gubuns[7]}",
                        "manFc": f"{gubuns[8]}",
                        "w1": f"{gubuns[9]}",
                        "t": f"{gubuns[10]}",
                        "w2": f"{gubuns[11]}",
                        "s1": f"{gubuns[12]}",
                        "s2": f"{gubuns[13]}",
                        "wh1": f"{gubuns[14]}",
                        "wh2": f"{gubuns[15]}",
                        "sky": f"{gubuns[16]}",
                        "prep": f"{gubuns[17]}",
                        "wf": f"{gubuns[18]}",
                    }
                print(filtered_data_dict)
                print(json.dumps(filtered_data_dict, indent=4, ensure_ascii=False))
                send_data_to_endpoint('store_fct_ocean_forecast', filtered_data_dict)
                
        except requests.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            filename = f"단기 해상 예보_error.csv"
            with open(filename, mode='w', newline='', encoding='utf-8=sig') as file:
                writer = csv.writer(file)
                # Write the headers and the error message
                writer.writerow(['Error'])
                writer.writerow([str(err)])
            print(f"An error occurred and has been written to {filename}")

        except Exception as err:
            print(f"An error occurred: {err}")
            filename = f"단기 해상 예보_error.csv"
            with open(filename, mode='w', newline='', encoding='utf-8=sig') as file:
                writer = csv.writer(file)
                # Write the headers and the error message
                writer.writerow(['Error'])
                writer.writerow([str(err)])
            print(f"An error occurred and has been written to {filename}")

    #중기 기온 예보 조회
    def fct_mid_land_temp_forecast():
        endpoint_name = '중기 기온 예보 조회'  
        
        now = datetime.now()
        hour = now.strftime('%H')
        yes = datetime.now() - timedelta(days=1)
        current_day = now.strftime("%Y%m%d")
        current_min = now.strftime("%Y%m%d%H%M")
        current_min = current_min[0:11]+"0"
        currentHour = now.strftime("%H%M")
        currentHour = currentHour[0:3]+"0"
        yes_day = yes.strftime("%Y%m%d")
        
      
        if int(hour) < 6:
            current_time = yes_day+"18"
        elif 6<= int(hour) < 18: 
            current_time = current_day+"06"
        elif 18<= int(hour):        
            current_time = current_day+"18"
            
        headers = {  # 헤더 설정
           'Content-Type': 'application/json'  # JSON 형식 설정
        }
        API_KEY = 'rejjPNsPRRyo4zzbD-UcDg'
        KMA_URL = 'https://apihub.kma.go.kr/api/typ01/url/fct_afs_wc.php'
        param = f'reg=&tmfc1={current_time}&tmfc2={current_time}&mode=1&disp=1&help=0&authKey={API_KEY}'
        try:
            url =f'{KMA_URL}?{param}'
            print(url)
            response = requests.get(url,headers=headers)
            response.raise_for_status()    
            lines = response.text.strip().split('\n')    
            for line in lines[2:-1]:
                gubuns = line.split(",")
                filtered_data_dict = {
                            "regIdIndex": f"{gubuns[0]}_{gubuns[1]}_{gubuns[2]}",
                            "regId": f"{gubuns[0]}",
                            "tmFc": f"{gubuns[1]}",
                            "tmEf": f"{gubuns[2]}",
                            "mod": f"{gubuns[3]}",
                            "stn": f"{gubuns[4]}",
                            "c": f"{gubuns[5]}",
                            "manId": f"{gubuns[6]}",
                            "manFc": f"{gubuns[7]}",
                            "regName": f"{gubuns[8]}",
                            "min": f"{gubuns[9]}",
                            "max": f"{gubuns[10]}",
                            "minL": f"{gubuns[11]}",
                            "minH": f"{gubuns[12]}",
                            "maxL": f"{gubuns[13]}",
                            "maxH": f"{gubuns[14]}",
                }
                print(json.dumps(filtered_data_dict, indent=4, ensure_ascii=False))
                # send_data_to_endpoint('store_mid_land_Temp_forecast', filtered_data_dict)
                try:
                    send_data_to_endpoint('store_mid_land_Temp_forecast', filtered_data_dict)
                except Exception as e:  # 'e'를 사용하여 예외를 잡습니다.
                    # 여기에 오류 로깅이나 다른 예외 처리 로직을 추가할 수 있습니다.
                    print(f"An error occurred: {e}")

                    # 다음과 같이 예외 정보를 CSV 파일에 쓸 수 있습니다.
                    with open('error_log.csv', 'a', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow([str(e)])

                
        except requests.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            filename = f"중기 기온 예보_error.csv"
            with open(filename, mode='w', newline='', encoding='utf-8=sig') as file:
                writer = csv.writer(file)
                # Write the headers and the error message
                writer.writerow(['Error'])
                writer.writerow([str(err)])
            print(f"An error occurred and has been written to {filename}")

        except Exception as err:
            print(f"An error occurred: {err}")
            filename = f"중기 기온 예보_error.csv"
            with open(filename, mode='w', newline='', encoding='utf-8=sig') as file:
                writer = csv.writer(file)
                # Write the headers and the error message
                writer.writerow(['Error'])
                writer.writerow([str(err)])
            print(f"An error occurred and has been written to {filename}")     

    #중기 날씨 예보 조회
    def fct_mid_land_status_forecast(): 
        endpoint_name = '중기 날씨 예보 조회'  
        
        now = datetime.now()
        hour = now.strftime('%H')
        yes = datetime.now() - timedelta(days=1)
        current_day = now.strftime("%Y%m%d")
        current_min = now.strftime("%Y%m%d%H%M")
        current_min = current_min[0:11]+"0"
        currentHour = now.strftime("%H%M")
        currentHour = currentHour[0:3]+"0"
        yes_day = yes.strftime("%Y%m%d")
        
        if int(hour) < 6:
            current_time = yes_day+"1800"
        elif 6<= int(hour) < 18: 
            current_time = current_day+"0600"
        elif 18<= int(hour):        
            current_time = current_day+"1800"
            
        headers = {  # 헤더 설정
           'Content-Type': 'application/json'  # JSON 형식 설정
        }
        API_KEY = 'rejjPNsPRRyo4zzbD-UcDg'
        
        KMA_URL = 'https://apihub.kma.go.kr/api/typ01/url/fct_afs_wl.php'
        param = f'reg=&tmfc={current_time}&mode=0&disp=1&help=0&authKey={API_KEY}'
        try:
            url =f'{KMA_URL}?{param}'
            print(url)
            response = requests.get(url,headers=headers)
            response.raise_for_status()    
            lines = response.text.strip().split('\n')    
            for line in lines[2:-1]:
                gubuns = line.split(",")
                print(url)
                print(len(gubuns),gubuns[10])
                filtered_data_dict = {
                            "regIdIndex": f"{gubuns[0]}_{gubuns[1]}_{gubuns[2]}",
                            "regId": f"{gubuns[0]}",
                            "tmFc": f"{gubuns[1]}",
                            "tmEf": f"{gubuns[2]}",
                            "mod": f"{gubuns[3]}",
                            "stn": f"{gubuns[4]}",
                            "c": f"{gubuns[5]}",
                            "manId": f"",
                            "manFc": f"",
                            "regName": f"",
                            "sky": f"{gubuns[6]}",
                            "pre": f"{gubuns[7]}",
                            "conf": f"{gubuns[8]}",
                            "wf": f"{gubuns[9]}",
                            "rnSt": f"{gubuns[10]}",
                }
                print(json.dumps(filtered_data_dict, indent=4, ensure_ascii=False))
                send_data_to_endpoint('store_mid_land_Status_forecast', filtered_data_dict)
                
        except requests.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            filename = f"중기 날씨 예보_error.csv"
            with open(filename, mode='w', newline='', encoding='utf-8=sig') as file:
                writer = csv.writer(file)
                # Write the headers and the error message
                writer.writerow(['Error'])
                writer.writerow([str(err)])
            print(f"An error occurred and has been written to {filename}")

        except Exception as err:
            print(f"An error occurred: {err}")
            filename = f"중기 날씨 예보_error.csv"
            with open(filename, mode='w', newline='', encoding='utf-8=sig') as file:
                writer = csv.writer(file)
                # Write the headers and the error message
                writer.writerow(['Error'])
                writer.writerow([str(err)])
            print(f"An error occurred and has been written to {filename}")   

    #특보 조회
    def fct_mid_alert_forecast():
        endpoint_name = '특보 조회'  
        
        now = datetime.now()
        hour = now.strftime('%H')
        yes = datetime.now() - timedelta(days=1)
        current_day = now.strftime("%Y%m%d")
        current_min = now.strftime("%Y%m%d%H%M")
        current_min = current_min[0:11]+"0"
        current_hour = now.strftime("%Y%m%d%H")
        currentHour = now.strftime("%H%M")
        currentHour = currentHour[0:3]+"0"

            
        headers = {  # 헤더 설정
           'Content-Type': 'application/json'  # JSON 형식 설정
        }
        API_KEY = 'rejjPNsPRRyo4zzbD-UcDg'
        
        KMA_URL = 'https://apihub.kma.go.kr/api/typ01/url/wrn_now_data.php'
        param = f'fe=f&tm=&disp=0&help=1&authKey={API_KEY}'
        try:
            url =f'{KMA_URL}?{param}'
            response = requests.get(url,headers=headers)
            response.raise_for_status()    
            lines = response.text.strip().split('\n')
            #print(lines[18:])    
            for line in lines[18:]:
                gubuns = line.split(",")
                filtered_data_dict = {
                        "regIdWrn":f"{gubuns[2].strip()}_{gubuns[6].strip()}",
                        "regUp": f"{gubuns[0].strip()}",
                        "regUpKo": f"{gubuns[1].strip()}",
                        "regId": f"{gubuns[2].strip()}",
                        "regKo": f"{gubuns[3].strip()}",
                        "tmFc": f"{gubuns[4].strip()}",
                        "tmEf": f"{gubuns[5].strip()}",
                        "apiTime":f"{current_hour}",
                        "wrn": f"{gubuns[6].strip()}",
                        "lvl": f"{gubuns[7].strip()}",
                        "cmd": f"{gubuns[8].strip()}",
                        "edTm": f"{gubuns[9].strip()}",
                }
                print(json.dumps(filtered_data_dict, indent=4, ensure_ascii=False))
                # send_data_to_endpoint('store_fct_alert_forecast', filtered_data_dict)
                
        except requests.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            filename = f"특보_error.csv"
            with open(filename, mode='w', newline='', encoding='utf-8=sig') as file:
                writer = csv.writer(file)
                # Write the headers and the error message
                writer.writerow(['Error'])
                writer.writerow([str(err)])
            print(f"An error occurred and has been written to {filename}")

        except Exception as err:
            print(f"An error occurred: {err}")
            filename = f"특보_error.csv"
            with open(filename, mode='w', newline='', encoding='utf-8=sig') as file:
                writer = csv.writer(file)
                # Write the headers and the error message
                writer.writerow(['Error'])
                writer.writerow([str(err)])
            print(f"An error occurred and has been written to {filename}")           

# MaxAPI.fct_mid_land_temp_forecast()

     
#MaxAPI.fct_mid_land_forecast()        
        
        # print(endpoint_name, location, formatted_date)
        # for endpoint in self.api_endpoints:
        #     if endpoint['name'] == endpoint_name:
        #         url = endpoint['url']
        #         params = endpoint['params'].copy()
        #         params['serviceKey'] = self.service_key
        #         params['locdate'] = formatted_date
        #         params['location'] = location
        #         time.sleep(1)
                
        #         try:
        #             response = requests.get(url, params=params)
        #             response.raise_for_status()  # Raises an HTTPError for bad responses
        #             # Successful response handling
        #             xml_dict = xmltodict.parse(response.content)
        #             item = xml_dict['response']['body']['items']['item']
        #             filtered_data = {
        #                 "latitude": item.get('latitude'),
        #                 "latitudeNum": item.get('latitudeNum'),
        #                 "location": item.get('location'),
        #                 "locdate": item.get('locdate'),
        #                 "longitude": item.get('longitude'),
        #                 "longitudeNum": item.get('longitudeNum'),
        #                 "sunrise": item.get('sunrise'),
        #                 "sunset": item.get('sunset')
        #             }
                    
        #             json_str = json.dumps(filtered_data, ensure_ascii=False, indent=4)
        #             print(json_str)
        #             return filtered_data

        #         except requests.HTTPError as http_err:
        #             # Create a DataFrame with error details
        #             df = pd.DataFrame({'Error Type': ['HTTPError'], 'Error Message': [str(http_err)]})
        #             # Create CSV file named after the location with the error details
        #             csv_file_name = f"{location}_error.csv"
        #             df.to_csv(csv_file_name, index=False, encoding='utf-8-sig')
        #             print(f'HTTP error occurred: {http_err}. Details saved to {csv_file_name}')

        #         except Exception as err:
        #             # Create a DataFrame with error details
        #             df = pd.DataFrame({'Error Type': ['Exception'], 'Error Message': [str(err)]})
        #             # Create CSV file named after the location with the error details
        #             csv_file_name = f"{location}_error.csv"
        #             df.to_csv(csv_file_name, index=False, encoding='utf-8-sig')
        #             print(f'Other error occurred: {err}. Details saved to {csv_file_name}')
        #         break  # Exit the loop after finding and processing the matching endpoint

        # else:
        #     # This else block executes if no break occurs, meaning no matching endpoint was found
        #     print(f"No endpoint found with the name: {endpoint_name}")
            
