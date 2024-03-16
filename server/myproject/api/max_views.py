from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.dateparse import parse_datetime
from django.views.generic import ListView
import json
from datetime import datetime
from django.db import connection
from django.http import JsonResponse
from datetime import datetime
from datetime import timedelta
import pandas as pd
import os
from .get_weather_alert import alert


network_path = r'\\192.168.1.202\d'

def query_store_fine_Sky(ne_am,ne_pm,tmFc_am,tmFc_pm,gubun):
    print(ne_am,ne_pm,tmFc_am,tmFc_pm)
  
    sql_query = """
        SELECT 
            api_fct_dl3.regId,
            (SELECT regName FROM api_weathershttermcode WHERE regId = api_fct_dl3.regId) AS regName,
            '0' AS lat,
            '0' AS lon,
            (SELECT sky FROM api_weathershttermlandforecast a2 WHERE a2.regId = api_fct_dl3.regId AND a2.ne = %s AND tmFc = %s) AS sky_am,
            (SELECT sky FROM api_weathershttermlandforecast a1 WHERE a1.regId = api_fct_dl3.regId AND a1.ne = %s AND tmFc = %s) AS sky_pm
        FROM api_weathershttermlandforecast api_fct_dl3 
        GROUP BY api_fct_dl3.regId
    """
    # 쿼리 실행
    with connection.cursor() as cursor:
        cursor.execute(sql_query, [ne_am, tmFc_am, ne_pm, tmFc_pm])
        rows = cursor.fetchall()
    # 데이터 포맷 변환 및 JsonResponse 반환
    data = []
    for row in rows:
        data.append({
            'regId': row[0],
            'regName': row[1],
            'lat': row[2],  # 실제 위도 데이터가 있다면 '0' 대신 사용
            'lon': row[3],  # 실제 경도 데이터가 있다면 '0' 대신 사용
            'sky_am': row[4],
            'sky_pm': row[5]
        })
    df = pd.DataFrame(data)
    #print(df)
    if gubun == "tod":
        today_path = os.path.join(network_path,'WSI','DigitalMedia','Custom','NavImportedData','FCT_DL3_SKY')
        df.to_csv(os.path.join(today_path,"today_path.csv"), index=False)
    else :
        tom_path = os.path.join(network_path,'WSI','DigitalMedia','Custom','NavImportedData','FCT_DL3_TOM_SKY')
        df.to_csv(os.path.join(tom_path,"tom_path.csv"), index=False)
        
    return JsonResponse({'status': 'success', 'data': data, 'message': 'Weather data retrieved successfully.'})
def query_store_fine_Temp(ne_am,ne_pm,tmFc_am,tmFc_pm,gubun):
    print(ne_am,ne_pm,tmFc_am,tmFc_pm)
    sql_query = """
        SELECT 
            api_fct_dl3.regId,
            (SELECT regName FROM api_weathershttermcode WHERE regId = api_fct_dl3.regId) AS regName,
            '0' AS lat,
            '0' AS lon,
            (SELECT ta FROM api_weathershttermlandforecast a2 WHERE a2.regId = api_fct_dl3.regId AND a2.ne = %s AND tmFc = %s) AS tMin,
            (SELECT ta FROM api_weathershttermlandforecast a1 WHERE a1.regId = api_fct_dl3.regId AND a1.ne = %s AND tmFc = %s) AS tMax
        FROM api_weathershttermlandforecast api_fct_dl3 
        GROUP BY api_fct_dl3.regId
    """
    # 쿼리 실행
    with connection.cursor() as cursor:
        cursor.execute(sql_query, [ne_am, tmFc_am, ne_pm, tmFc_pm])
        rows = cursor.fetchall()
    # 데이터 포맷 변환 및 JsonResponse 반환
    data = []
    for row in rows:
        data.append({
            'regId': row[0],
            'regName': row[1],
            'lat': row[2],  # 실제 위도 데이터가 있다면 '0' 대신 사용
            'lon': row[3],  # 실제 경도 데이터가 있다면 '0' 대신 사용
            'tMin': row[4],
            'tMax': row[5]
        })
    df = pd.DataFrame(data)
    #print(df)
    if gubun == "tod":
        today_path = os.path.join(network_path,'WSI','DigitalMedia','Custom','NavImportedData','FCT_DL3_TMIN_TMAX_TOD')
        if not os.path.exists(today_path): os.makedirs(today_path,exist_ok=False)
        df.to_csv(os.path.join(today_path,"today_path.csv"), index=False)
    else :
        tom_path = os.path.join(network_path,'WSI','DigitalMedia','Custom','NavImportedData','FCT_DL3_TMIN_TMAX_TOM')
        if not os.path.exists(tom_path): os.makedirs(tom_path,exist_ok=False)
        df.to_csv(os.path.join(tom_path,"tom_path.csv"), index=False)
        
    return JsonResponse({'status': 'success', 'data': data, 'message': 'Weather data retrieved successfully.'})
def query_store_fine_Ocean(ne_am,ne_pm,tmFc,gubun):
    sql_query = """
        select 
        "서해" as 'id', "서해" as 'regIdName',
        "35.79" as 'lat', "123.79" as 'lon', "" as 'wd2', 
        max(fdo3_1.w1) as 'ws1', max(fdo3_1.w2) as 'ws2',max(fdo3_1.wh1) as 'wh1',max(fdo3_1.wh2) as 'wh2', max(fdo3_1.wf) as 'wfCd'
        from api_weathershttermoceanforecast fdo3_1 where fdo3_1.tmFc = %s and ((fdo3_1.ne= %s) or (fdo3_1.ne= %s)) 
        and ((fdo3_1.regId='12A20100') or (fdo3_1.regId='12A20210')or (fdo3_1.regId='12A20220') or (fdo3_1.regId='12A30100') or 
        (fdo3_1.regId ='12A30211') or (fdo3_1.regId ='12A30222') or (fdo3_1.regId ='12A30221') or (fdo3_1.regId ='12A30212'))
        union
        select 
        "남해" as 'id', "남해" as 'regIdName',
        "34.10" as 'lat', "127.89" as 'lon', "" as 'wd2', 
        max(fdo3_1.w1) as 'ws1', max(fdo3_1.w2) as 'ws2',max(fdo3_1.wh1) as 'wh1',max(fdo3_1.wh2) as 'wh2', max(fdo3_1.wf) as 'wfCd'
        from api_weathershttermoceanforecast fdo3_1 where fdo3_1.tmFc = %s and ((fdo3_1.ne= %s) or (fdo3_1.ne= %s))
        and ((fdo3_1.regId='12B10100') or (fdo3_1.regId='12B10201') or (fdo3_1.regId='12B10202') 
                                    or (fdo3_1.regId='12B20100') or (fdo3_1.regId='12B20210') or (fdo3_1.regId='12B20220'))
        union
        select 
        "제주도" as 'id', "제주도" as 'regIdName',
        "33.48" as 'lat', "126.49" as 'lon', "" as 'wd2', 
        max(fdo3_1.w1) as 'ws1', max(fdo3_1.w2) as 'ws2',max(fdo3_1.wh1) as 'wh1',max(fdo3_1.wh2) as 'wh2', max(fdo3_1.wf) as 'wfCd'
        from api_weathershttermoceanforecast fdo3_1 where fdo3_1.tmFc = %s and ((fdo3_1.ne= %s) or (fdo3_1.ne= %s))
        and ((fdo3_1.regId='12B10300') or (fdo3_1.regId='12B10411') or (fdo3_1.regId='12B10412') or (fdo3_1.regId='12B10420'))
        union
        select 
        "동해" as 'id', "동해" as 'regIdName',
        "37.50" as 'lat', "130.85" as 'lon', "" as 'wd2', 
        max(fdo3_1.w1) as 'ws1', max(fdo3_1.w2) as 'ws2',max(fdo3_1.wh1) as 'wh1',max(fdo3_1.wh2) as 'wh2', max(fdo3_1.wf) as 'wfCd'
        from api_weathershttermoceanforecast fdo3_1 where fdo3_1.tmFc = %s and ((fdo3_1.ne= %s) or (fdo3_1.ne= %s))
        and ((fdo3_1.regId='12C10100') or (fdo3_1.regId='12C10211') or (fdo3_1.regId='12C10221') or (fdo3_1.regId='12C10212') or 
            (fdo3_1.regId='12C10222') or (fdo3_1.regId='12C20100') or (fdo3_1.regId='12C20210') or (fdo3_1.regId='12C20220'))
    """
    # 쿼리 실행
    with connection.cursor() as cursor:
        cursor.execute(sql_query, [tmFc, ne_am, ne_pm,tmFc, ne_am, ne_pm,tmFc, ne_am, ne_pm,tmFc, ne_am, ne_pm, ])
        rows = cursor.fetchall()
    # 데이터 포맷 변환 및 JsonResponse 반환
    data = []
    for row in rows:
        data.append({
            'regId': row[0],
            'regName': row[1],
            'lat': row[2],  # 실제 위도 데이터가 있다면 '0' 대신 사용
            'lon': row[3],  # 실제 경도 데이터가 있다면 '0' 대신 사용
            'wd2': row[4],
            'ws1': row[5],
            'ws2': row[6],
            'wh1': row[7],
            'wh2': row[8],
            'wfCd': row[9]
        })
    df = pd.DataFrame(data)
    #print(df)
    if gubun == "tod":
        today_path = os.path.join(network_path,'WSI','DigitalMedia','Custom','NavImportedData','FCT_DO3_OCEAN_TOD')
        if not os.path.exists(today_path): os.makedirs(today_path,exist_ok=False)
        df.to_csv(os.path.join(today_path,"today_ocean.csv"), index=False)
    else :
        tom_path = os.path.join(network_path,'WSI','DigitalMedia','Custom','NavImportedData','FCT_DO3_OCEAN_TOM')
        if not os.path.exists(tom_path): os.makedirs(tom_path,exist_ok=False)
        df.to_csv(os.path.join(tom_path,"tom_ocean.csv"), index=False)
        
    return JsonResponse({'status': 'success', 'data': data, 'message': 'Weather data retrieved successfully.'})
def query_fine_weekly(ne_first,ne_second,ne_third,ne_fourth,fct_dl_time,fct_wc_time,fct_wc_tmEf1,fct_wc_tmEf2,fct_wc_tmEf3,fct_wc_tmEf4):
    print(ne_first,ne_second,ne_third,ne_fourth,fct_dl_time,fct_wc_time,fct_wc_tmEf1,fct_wc_tmEf2,fct_wc_tmEf3,fct_wc_tmEf4)
    sql_query = """
        select 
        fct_wc6.regId, fct_wc6.regName, "0" as "lat", "0" as "lon",
        (select ta from api_weathershttermlandforecast fct_dl3 where fct_dl3.tmFc = %s and fct_dl3.ne =%s and fct_dl3.regId ='11B10101') as ta2Min,
        (select ta from api_weathershttermlandforecast fct_dl3 where fct_dl3.tmFc = %s and fct_dl3.ne =%s and fct_dl3.regId ='11B10101') as ta2Max,
        (select ta from api_weathershttermlandforecast fct_dl3 where fct_dl3.tmFc = %s and fct_dl3.ne =%s and fct_dl3.regId ='11B10101') as ta3Min,
        (select ta from api_weathershttermlandforecast fct_dl3 where fct_dl3.tmFc = %s and fct_dl3.ne =%s and fct_dl3.regId ='11B10101') as ta3Max,
        (select min from api_weathermidtermlandtempforecast fct_wc6 where fct_wc6.tmFc = %s and fct_wc6.tmEf = %s and fct_wc6.regId ='11B10101') as ta4Min,
        (select max from api_weathermidtermlandtempforecast fct_wc6 where fct_wc6.tmFc = %s and fct_wc6.tmEf = %s and fct_wc6.regId ='11B10101') as ta4Max,
        (select min from api_weathermidtermlandtempforecast fct_wc6 where fct_wc6.tmFc = %s and fct_wc6.tmEf = %s and fct_wc6.regId ='11B10101') as ta5Min,
        (select max from api_weathermidtermlandtempforecast fct_wc6 where fct_wc6.tmFc = %s and fct_wc6.tmEf = %s and fct_wc6.regId ='11B10101') as ta5Max,
        (select min from api_weathermidtermlandtempforecast fct_wc6 where fct_wc6.tmFc = %s and fct_wc6.tmEf = %s and fct_wc6.regId ='11B10101') as ta6Min,
        (select max from api_weathermidtermlandtempforecast fct_wc6 where fct_wc6.tmFc = %s and fct_wc6.tmEf = %s and fct_wc6.regId ='11B10101') as ta6Max,
        (select min from api_weathermidtermlandtempforecast fct_wc6 where fct_wc6.tmFc = %s and fct_wc6.tmEf = %s and fct_wc6.regId ='11B10101') as ta7Min,
        (select max from api_weathermidtermlandtempforecast fct_wc6 where fct_wc6.tmFc = %s and fct_wc6.tmEf = %s and fct_wc6.regId ='11B10101') as ta7Max
        from api_weathermidtermlandtempforecast fct_wc6 where fct_wc6.regId ='11B10101' GROUP by fct_wc6.regId 
    """
    # 쿼리 실행
    with connection.cursor() as cursor:
        cursor.execute(sql_query, [fct_dl_time,ne_first,
                                   fct_dl_time,ne_second,
                                   fct_dl_time,ne_third,
                                   fct_dl_time,ne_fourth,
                                   fct_wc_time,fct_wc_tmEf1,
                                   fct_wc_time,fct_wc_tmEf1,
                                   fct_wc_time,fct_wc_tmEf2,
                                   fct_wc_time,fct_wc_tmEf2,
                                   fct_wc_time,fct_wc_tmEf3,
                                   fct_wc_time,fct_wc_tmEf3,
                                   fct_wc_time,fct_wc_tmEf4,
                                   fct_wc_time,fct_wc_tmEf4
                                   ])
        rows = cursor.fetchall()
    # 데이터 포맷 변환 및 JsonResponse 반환
    data = []
    for row in rows:
        data.append({
            'regId': row[0],
            'regName': row[1],
            'lat': row[2],  # 실제 위도 데이터가 있다면 '0' 대신 사용
            'lon': row[3],  # 실제 경도 데이터가 있다면 '0' 대신 사용
            'ta2Min': row[4],
            'ta2Max': row[5],
            'ta3Min': row[6],
            'ta3Max': row[7],
            'ta4Min': row[8],
            'ta4Max': row[9],
            'ta5Min': row[10],
            'ta5Max': row[11],
            'ta6Min': row[12],
            'ta6Max': row[13],
            'ta7Min': row[14],
            'ta7Max': row[15],
        })
    df = pd.DataFrame(data)
    print(df)
    today_path = os.path.join(network_path,'WSI','DigitalMedia','Custom','ImportedData','FCT_WC6')
    if not os.path.exists(today_path): os.makedirs(today_path,exist_ok=False)
    df.to_csv(os.path.join(today_path,"FCT_WC6.csv"), index=False)
        
    return JsonResponse({'status': 'success', 'data': data, 'message': 'Weather data retrieved successfully.'})
def query_fine_alert(current_time):
    print(current_time)
    sql_query = """
            select * from api_weatheralertforecast aw where aw.apiTime = %s
    """
    # 쿼리 실행
    with connection.cursor() as cursor:
        cursor.execute(sql_query, [current_time])
        rows = cursor.fetchall()
        data = []
    for row in rows:
        data.append({
            'regWrn': row[0],
            'regUp': row[1],
            'regUpKo': row[2],  # 실제 위도 데이터가 있다면 '0' 대신 사용
            'regId': row[3],  # 실제 경도 데이터가 있다면 '0' 대신 사용
            'regKo': row[4],
            'tmFc': row[5],
            'tmEf': row[6],
            'apiTime': row[7],
            'wrn': row[8],
            'lvl': row[9],
            'cmd': row[10],
            'edtm': row[11],
        })    
        df = pd.DataFrame(data) 
        print(df[df['lvl'] != '예비']  )
        alert_df = df[df['lvl'] != '예비']  
    return alert_df     
    print(df)
    
def query_fine_aws(current_time):        
    sql_query = """
            SELECT aws_stn.stnId, aws_stn.stnKo, aws_stn.lat, aws_stn.lon, aw.tmKst, aw.ta, aw.wd, aw.ws, aw.rnDay, aw.rnHr1, aw.Hm  
            FROM api_weatheraws1mobservation aw
            JOIN api_weatherawsstninfo aws_stn ON aws_stn.stnId  = aw.stnId
            WHERE aw.tmKst = %s AND aw.ta > -99;
    """    
    # 쿼리 실행
    with connection.cursor() as cursor:
        cursor.execute(sql_query, [current_time])
        rows = cursor.fetchall()
        data = []
    for row in rows:
        data.append({
            'stnId': row[0],
            'stnKo': row[1],
            'lat': row[2],  # 실제 위도 데이터가 있다면 '0' 대신 사용
            'lon': row[3],  # 실제 경도 데이터가 있다면 '0' 대신 사용
            'tmkst' : row[4],
            'ta': row[5],
            'wd': row[6],
            'ws': row[7],
            'rnDay': row[8],
            'rnHr1': row[9],
            'Hm': row[10],
        })    
    df = pd.DataFrame(data)     
    current_path = os.path.join(network_path,'WSI','DigitalMedia','Custom','NavImportedData','current_AWS')
    if not os.path.exists(current_path): os.makedirs(current_path,exist_ok=False)
    df.to_csv(os.path.join(current_path,"current_AWS.csv"), index=False)
        
        
@csrf_exempt
def fct_search_fine_Temp(request): 
    now = datetime.now()
    current_time = now.strftime("%H")
    current_day = now.strftime("%Y%m%d")
    current_min = now.strftime("%Y%m%d%H%M")
    current_min = current_min[0:11]+"0"
    currentHour = now.strftime("%H%M")
    currentHour = currentHour[0:3]+"0"
    yes = now - timedelta(days=1)
    yes_day = yes.strftime("%Y%m%d")

    if int(current_time) < 5:
    #전날 정보를 호출
        query_store_fine_Temp('1','2',yes_day+"1700",yes_day+"1700","tod")
        query_store_fine_Temp('1','2',yes_day+"1700",yes_day+"1700","tom")
    if 5<= int(current_time) < 11: 
    #5시 데이터 호출
        query_store_fine_Temp('0','1',current_day+"0500",current_day+"0500","tod")
        query_store_fine_Temp('2','3',current_day+"0500",current_day+"0500","tom")
    if 11<= int(current_time) <15:        
    #11시 데이터 호출
        query_store_fine_Temp('0','0',current_day+"1100",current_day+"1100","tod")
        query_store_fine_Temp('1','2',current_day+"1100",current_day+"1100","tom")
    if 15<= int(current_time) <17:        
    #11시 데이터 호출
        query_store_fine_Temp('0','0',current_day+"1100",current_day+"1100","tod")
        query_store_fine_Temp('1','2',current_day+"1100",current_day+"1100","tom")
        
    if 17<= int(current_time):  
        query_store_fine_Temp('0','0',current_day+"1700",current_day+"1700","tod")
        query_store_fine_Temp('1','2',current_day+"1700",current_day+"1700","tom")

    return JsonResponse({'status': 'success', 'message': 'Weather data retrieved successfully.'})

@csrf_exempt    
def fct_search_fine_Sky(request): 
    
    now = datetime.now()
    current_time = now.strftime("%H")
    current_day = now.strftime("%Y%m%d")
    current_min = now.strftime("%Y%m%d%H%M")
    current_min = current_min[0:11]+"0"
    currentHour = now.strftime("%H%M")
    currentHour = currentHour[0:3]+"0"
    yes = now - timedelta(days=1)
    yes_day = yes.strftime("%Y%m%d")

    if int(current_time) < 5:
    #전날 정보를 호출
        query_store_fine_Sky('1','2',yes_day+"1700",yes_day+"1700","tod")
        query_store_fine_Sky('1','2',yes_day+"1700",yes_day+"1700","tom")
    if 5<= int(current_time) < 11: 
    #5시 데이터 호출
        query_store_fine_Sky('0','1',current_day+"0500",current_day+"0500","tod")
        query_store_fine_Sky('2','3',current_day+"0500",current_day+"0500","tom")
    if 11<= int(current_time) <15:        
    #11시 데이터 호출
        query_store_fine_Sky('0','0',current_day+"1100",current_day+"1100","tod")
        query_store_fine_Sky('1','2',current_day+"1100",current_day+"1100","tom")
    if 15<= int(current_time) <17:        
    #11시 데이터 호출
        query_store_fine_Sky('0','0',current_day+"1100",current_day+"1100","tod")
        query_store_fine_Sky('1','2',current_day+"1100",current_day+"1100","tom")
        
    if 17<= int(current_time):  
        query_store_fine_Sky('0','0',current_day+"1700",current_day+"1700","tod")
        query_store_fine_Sky('1','2',current_day+"1700",current_day+"1700","tom")
        
    return JsonResponse({'status': 'success', 'message': 'Weather data retrieved successfully.'})

@csrf_exempt
def fct_search_fine_Ocean(request):
    now = datetime.now()
    current_time = now.strftime("%H")
    current_day = now.strftime("%Y%m%d")
    current_min = now.strftime("%Y%m%d%H%M")
    current_min = current_min[0:11]+"0"
    currentHour = now.strftime("%H%M")
    currentHour = currentHour[0:3]+"0"
    yes = now - timedelta(days=1)
    yes_day = yes.strftime("%Y%m%d")
    
    if(int(current_time) < 5) :
        query_store_fine_Ocean('1','2',yes_day+"1700","tod")
        query_store_fine_Ocean('1','2',yes_day+"1700","tom")
    elif( 5<= int(current_time) <11) :
        query_store_fine_Ocean('0','1',current_day+"0500","tod")
        query_store_fine_Ocean('2','3',current_day+"0500","tom")
    elif(11<= int(current_time) < 15) :
        query_store_fine_Ocean('0','0',current_day+"1100","tod")
        query_store_fine_Ocean('1','2',current_day+"1100","tom")
    elif(15<= int(current_time) < 17) :
        query_store_fine_Ocean('1','2',current_day+"1100","tod")
        query_store_fine_Ocean('1','2',current_day+"1100","tom")
    elif(17<= int(current_time) < 24) :
        query_store_fine_Ocean('1','2',current_day+"1700","tod")
        query_store_fine_Ocean('1','2',current_day+"1700","tom")
        
    return JsonResponse({'status': 'success', 'message': 'Weather data retrieved successfully.'})

@csrf_exempt
def fct_search_weekly_Data(request):
    now = datetime.now()
    current_time = now.strftime("%H")
    current_day = now.strftime("%Y%m%d")
    current_min = now.strftime("%Y%m%d%H%M")
    current_min = current_min[0:11]+"0"
    currentHour = now.strftime("%H%M")
    currentHour = currentHour[0:3]+"0"
    yes = now - timedelta(days=1)
    yes_day = yes.strftime("%Y%m%d")
    
    #발효 시간
    fct_wc_tmEf1 = (now + timedelta(days=3)).strftime("%Y%m%d")+"0000"
    fct_wc_tmEf2 = (now + timedelta(days=4)).strftime("%Y%m%d")+"0000"
    fct_wc_tmEf3 = (now + timedelta(days=5)).strftime("%Y%m%d")+"0000"
    fct_wc_tmEf4 = (now + timedelta(days=6)).strftime("%Y%m%d")+"0000"
    
    #어제 기준 발효시간
    yes_fct_wc_tmEf1 = (now + timedelta(days=2)).strftime("%Y%m%d")+"0000"
    yes_fct_wc_tmEf2 = (now + timedelta(days=3)).strftime("%Y%m%d")+"0000"
    yes_fct_wc_tmEf3 = (now + timedelta(days=4)).strftime("%Y%m%d")+"0000"
    yes_fct_wc_tmEf4 = (now + timedelta(days=5)).strftime("%Y%m%d")+"0000"
    
    
    if(int(current_time) < 5) :
        query_fine_weekly('3','4','5','6',yes_day+"1700",yes_day+"1800",
                          yes_fct_wc_tmEf1,yes_fct_wc_tmEf2,yes_fct_wc_tmEf3,yes_fct_wc_tmEf4)
    elif( 5<= int(current_time) <6) :
        query_fine_weekly('2','3','4','5',current_day+"0500",yes_day+"1800",
                          fct_wc_tmEf1,fct_wc_tmEf2,fct_wc_tmEf3,fct_wc_tmEf4)
    elif( 6<= int(current_time) <11) :
        query_fine_weekly('2','3','4','5',current_day+"0500",current_day+"0600",
                          fct_wc_tmEf1,fct_wc_tmEf2,fct_wc_tmEf3,fct_wc_tmEf4)
    elif(11<= int(current_time) < 17) :
        query_fine_weekly('1','2','3','4',current_day+"1100",current_day+"0600",
                          fct_wc_tmEf1,fct_wc_tmEf2,fct_wc_tmEf3,fct_wc_tmEf4)
    elif(17<= int(current_time) < 18) :
        query_fine_weekly('3','4','5','6',current_day+"1700",current_day+"0600",
                          fct_wc_tmEf1,fct_wc_tmEf2,fct_wc_tmEf3,fct_wc_tmEf4)
    elif(18<= int(current_time)) :    
        query_fine_weekly('3','4','5','6',current_day+"1700",current_day+"1800",
                          fct_wc_tmEf1,fct_wc_tmEf2,fct_wc_tmEf3,fct_wc_tmEf4)
    

@csrf_exempt
def fct_search_alert_Data(request):
    now = datetime.now()
    current_time = now.strftime("%H")
    current_time = now.strftime("%Y%m%d%H")
    alert_df = query_fine_alert(current_time)
    alert(alert_df)
    

@csrf_exempt
def obs_aws_1hr_fine_Data(request):   
    now = datetime.now()
    current_time = now.strftime("%H")
    current_time = now.strftime("%Y%m%d%H")
    query_fine_aws(current_time+"00")
    
    
    