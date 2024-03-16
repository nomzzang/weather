from ctypes.wintypes import HENHMETAFILE
from lxml import etree
from pykml import parser
import requests
import csv
import json
from datetime import datetime
from datetime import timedelta
import pandas as pd
import logging
import os

def color_gubun(a):
    color=""
    a = int(a)
    if a == 100:
        color = "fffc0de6" #태풍 경보
    elif a == 200:
        color = "ffdb28b9" #해일 경보
    elif a == 300:
        color = "ffc728ff" #적설 경보
    elif a == 400:        
        color = "ffde1f3b" 
    elif a == 500:        
        color = "ffd6036e" #Heat 경보
    elif a == 600:
        color = "ff0063ff" #dry 경보
    elif a == 700:        
        color = "ff00baff" #dust 경보
    elif a == 800: 
        color = "ffffa800" 
    elif a == 900:    
        color = "ffff6000" #seaWave 경보
    elif a == 1000:
        color = "ff3ca900" #gale 경보
    elif a == 1100:
        color = "ff7c74e8" #태풍 경보
    elif a == 1200:
        color = "fff18ddd" #해일 주의보
    elif a == 1300:
        color = "ffdf84ff" #적설 주의보
    elif a == 1400:
        color = "ffd78f8e" 
    elif a == 1500:
        color = "fff087bc" #Heat 주의보
    elif a == 1600:
        color = "ff6fa2f6" #dry 주의보
    elif a == 1700:
        color = "fface9ff" #dust 주의보
    elif a == 1800:
        color = "ffffd88c" 
    elif a == 1900:
        color = "ffffa275" #seaWave 주의보
    elif a == 2000:
        color = "ff92ec8e" #gale 주의보
    return color

def eachalert(df,id, currentHour, currentMin):
    #print(df)
    path_dir = os.path.join("\\\\192.168.1.202\\d\\WSI\\DigitalMedia\\Custom\\KML",id)
    if not os.path.exists(path_dir): os.makedirs(path_dir)

    kml_file_path = os.path.join("C:\\git_platform\\platform\\server\\myproject\\api\\KML" ,f'MAX_ALERT_{id}.kml')
   
    with open(kml_file_path,'rt', encoding='UTF8') as f:
        tree = parser.parse(f)
    folder = tree.getroot().Document.Folder
    str_list=[]
    
    for i in range(len(df)):
        areaCode = str(df.iloc[i][3])
        warnVar = str(df.iloc[i][4])
        str_list.append(areaCode+"_"+warnVar+"_")
        
    code = "".join(str_list)
    print(len(code.split("nan")))
    if len(code.split("nan")) > 0:
        print(id)
        for pm in folder.Placemark:
            pm_code = pm.ExtendedData.SchemaData.SimpleData
            if code.find(str(pm_code)) != -1:
                if int(code.split(str(pm_code))[1].split("_")[1]) < 1000 :
                    pm.styleUrl = "#"+id+"_Warning"
                else :
                    pm.styleUrl = "#"+id+"_Watch" 
            else :
                if id == "base":
                    pm.styleUrl = '#None_Base'
                else :
                    pm.styleUrl = '#None'
                
    
            
    with open(path_dir+"\\MAX_ALERT_"+id+".kml", 'w') as output:
        output.write(etree.tostring(tree, pretty_print=True).decode("utf-8"))

    with open(path_dir+"\\MAX_ALERT_"+id+"_"+currentHour+".kml", 'w') as output:
        output.write(etree.tostring(tree, pretty_print=True).decode("utf-8"))
        
    with open(path_dir+"\\MAX_ALERT_"+id+"_"+currentMin+".kml", 'w') as output:
        output.write(etree.tostring(tree, pretty_print=True).decode("utf-8"))
    
        
        
    #with open("MAX_ALERT_"+id+".kml", 'w') as output:
    #    output.write(etree.tostring(tree, pretty_print=True).decode("utf-8"))


# 기상 특보 API를 호출해서, 특보 별로 데이터를 분류한 뒤 
# 기존에 생성해 놓은 특보별 KML 파일에 해당하는 특보별 데이터를 집어넣어 파일을 생성한다. 
def alert(alert_df):
    try:
        print("1111111111111111111111111111111111111111111111111111111111111111111111")
        now = datetime.now()
        if len(alert_df)==0:
            print("데이터 없음")
        else:
            current_time = now.strftime("%H")
            current_day = now.strftime("%Y%m%d")
            current_min = now.strftime("%Y%m%d%H%M")
            currentMin = current_min[0:11]+"0"
            currentHour = now.strftime("%H%M")
            currentHour = currentHour[0:3]+"0"
            alert_df.loc[(alert_df['LVL'] == '주의보') & (alert_df['WRN'] == '태풍'), 'warnVar'] = 1100
            alert_df.loc[(alert_df['LVL'] == '경보') & (alert_df['WRN'] == '태풍'), 'warnVar'] = 100
            alert_df.loc[(alert_df['LVL'] == '주의보') & (alert_df['WRN'] == '지진해일'), 'warnVar'] = 1200
            alert_df.loc[(alert_df['LVL'] == '경보') & (alert_df['WRN'] == '지진해일'), 'warnVar'] = 200
            alert_df.loc[(alert_df['LVL'] == '주의보') & (alert_df['WRN'] == '대설'), 'warnVar'] = 1300
            alert_df.loc[(alert_df['LVL'] == '경보') & (alert_df['WRN'] == '대설'), 'warnVar'] = 300
            alert_df.loc[(alert_df['LVL'] == '주의보') & (alert_df['WRN'] == '한파'), 'warnVar'] = 1400
            alert_df.loc[(alert_df['LVL'] == '경보') & (alert_df['WRN'] == '한파'), 'warnVar'] = 400
            alert_df.loc[(alert_df['LVL'] == '주의보') & (alert_df['WRN'] == '폭염'), 'warnVar'] = 1500
            alert_df.loc[(alert_df['LVL'] == '경보') & (alert_df['WRN'] == '폭염'), 'warnVar'] = 500  
            alert_df.loc[(alert_df['LVL'] == '주의보') & (alert_df['WRN'] == '건조'), 'warnVar'] = 1600
            alert_df.loc[(alert_df['LVL'] == '경보') & (alert_df['WRN'] == '건조'), 'warnVar'] = 600
            alert_df.loc[(alert_df['LVL'] == '주의보') & (alert_df['WRN'] == '황사'), 'warnVar'] = 1700
            alert_df.loc[(alert_df['LVL'] == '경보') & (alert_df['WRN'] == '황사'), 'warnVar'] = 700                                                
            alert_df.loc[(alert_df['LVL'] == '주의보') & (alert_df['WRN'] == '호우'), 'warnVar'] = 1800
            alert_df.loc[(alert_df['LVL'] == '경보') & (alert_df['WRN'] == '호우'), 'warnVar'] = 800   
            alert_df.loc[(alert_df['LVL'] == '주의보') & (alert_df['WRN'] == '해일'), 'warnVar'] = 1900
            alert_df.loc[(alert_df['LVL'] == '경보') & (alert_df['WRN'] == '해일'), 'warnVar'] = 900 
            alert_df.loc[(alert_df['LVL'] == '주의보') & (alert_df['WRN'] == '강풍'), 'warnVar'] = 1900
            alert_df.loc[(alert_df['LVL'] == '경보') & (alert_df['WRN'] == '강풍'), 'warnVar'] = 900   
            df = alert_df
            print(df)
            condition1 = (df.endTime == 'nan') & ((df.warnVar == '100')|(df.warnVar == '1100'))
            eachalert(df[condition1],"Typhoon", currentHour, currentMin)
            condition2 = (df.endTime == 'nan') & ((df.warnVar == '200')|(df.warnVar == '1200'))
            eachalert(df[condition2],"Tsunami", currentHour, currentMin)
            condition3 = (df.endTime == 'nan') & ((df.warnVar == '300')|(df.warnVar == '1300'))
            eachalert(df[condition3],"Snow", currentHour, currentMin)
            condition4 = (df.endTime == 'nan') & ((df.warnVar == '400')|(df.warnVar == '1400'))
            eachalert(df[condition4],"Cold", currentHour, currentMin)
            condition5 =(df.endTime == 'nan') & ((df.warnVar == '500')|(df.warnVar == '1500'))
            eachalert(df[condition5],"Heat", currentHour, currentMin)
            condition6 =(df.endTime == 'nan') & ((df.warnVar == '600')|(df.warnVar == '1600'))
            eachalert(df[condition6],"Dry", currentHour, currentMin)
            condition7 = (df.endTime == 'nan') & ((df.warnVar == '700')|(df.warnVar == '1700'))
            eachalert(df[condition7],"Dust", currentHour, currentMin)
            condition8 = (df.endTime == 'nan') & ((df.warnVar == '800')|(df.warnVar == '1800'))
            eachalert(df[condition8],"DownPour", currentHour, currentMin)
            condition9 = (df.endTime == 'nan') & ((df.warnVar == '900')|(df.warnVar == '1900'))
            eachalert(df[condition9],"SeaWave", currentHour, currentMin)
            condition10 = (df.endTime == 'nan') & ((df.warnVar == '1000')|(df.warnVar == '2000'))
            eachalert(df[condition10],"Gale", currentHour, currentMin)
            condition10 = (df.endTime == 'nan') & ((df.warnVar == '3000'))
            eachalert(df[condition10],"base", currentHour, currentMin)
                    
            logging.info("Done!!")
    except:
        logging.error("error")
    else:
        logging.info("Done")
#alert()