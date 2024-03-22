from django.db import models


# class ApiResponse(models.Model):
#     resultCode = models.CharField(max_length=20)
#     resultMsg = models.CharField(max_length=255)
#     dataType = models.CharField(max_length=20)
#     pageNo = models.IntegerField()
#     numOfRows = models.IntegerField()
#     totalCount = models.IntegerField()
    
#     # Assuming new fields to capture properties of nested 'items'
#     filetype = models.CharField(max_length=20, null=True, blank=True)
#     version = models.CharField(max_length=20, null=True, blank= True)

    
# class SidoRealTimeAirQuality(models.Model):
#     pm25Grade1h = models.CharField(max_length=10, null=True, blank=True)
#     pm10Value24 = models.CharField(max_length=10, null=True, blank=True)
#     so2Value = models.CharField(max_length=10, null=True, blank=True)
#     pm10Grade1h = models.CharField(max_length=10, null=True, blank=True)
#     pm10Value = models.CharField(max_length=10, null=True, blank=True)
#     o3Grade = models.CharField(max_length=10, null=True, blank=True)
#     pm25Flag = models.CharField(max_length=10, null=True, blank=True)
#     khaiGrade = models.CharField(max_length=10, null=True, blank=True)
#     pm25Value = models.CharField(max_length=10, null=True, blank=True)
#     no2Flag = models.CharField(max_length=10, null=True, blank=True)
#     mangName = models.CharField(max_length=50)
#     stationName = models.CharField(max_length=50)
#     no2Value = models.CharField(max_length=10, null=True, blank=True)
#     so2Grade = models.CharField(max_length=10, null=True, blank=True)
#     stationCode = models.CharField(max_length=50)
#     coFlag = models.CharField(max_length=10, null=True, blank=True)
#     khaiValue = models.CharField(max_length=10, null=True, blank=True)
#     coValue = models.CharField(max_length=10, null=True, blank=True)
#     pm10Flag = models.CharField(max_length=10, null=True, blank=True)
#     sidoName = models.CharField(max_length=50)
#     pm25Value24 = models.CharField(max_length=10, null=True, blank=True)
#     no2Grade = models.CharField(max_length=10, null=True, blank=True)
#     o3Flag = models.CharField(max_length=10, null=True, blank=True)
#     pm25Grade = models.CharField(max_length=10, null=True, blank=True)
#     so2Flag = models.CharField(max_length=10, null=True, blank=True)
#     coGrade = models.CharField(max_length=10, null=True, blank=True)
#     dataTime = models.CharField(max_length=255)
#     pm10Grade = models.CharField(max_length=10, null=True, blank=True)
#     o3Value = models.CharField(max_length=10, null=True, blank=True)
    
# class MidTermTemperature(models.Model):
#     regId = models.CharField(max_length=10, primary_key=True)
#     taMin3 = models.IntegerField()
#     taMax3 = models.IntegerField()
#     taMin4 = models.IntegerField()
#     taMax4 = models.IntegerField()
#     taMin5 = models.IntegerField()
#     taMax5 = models.IntegerField()
#     taMin6 = models.IntegerField()
#     taMax6 = models.IntegerField()
#     taMin7 = models.IntegerField()
#     taMax7 = models.IntegerField()
#     taMin8 = models.IntegerField()
#     taMax8 = models.IntegerField()
#     taMin9 = models.IntegerField()
#     taMax9 = models.IntegerField()
#     taMin10 = models.IntegerField()
#     taMax10 = models.IntegerField()

#     def __str__(self):
#         return self.regId
    
# class MidTermLandForecast(models.Model):
#     regId = models.CharField(max_length=10, primary_key=True)
#     rnSt3Am = models.IntegerField()
#     rnSt3Pm = models.IntegerField()
#     rnSt4Am = models.IntegerField()
#     rnSt4Pm = models.IntegerField()
#     rnSt5Am = models.IntegerField()
#     rnSt5Pm = models.IntegerField()
#     rnSt6Am = models.IntegerField()
#     rnSt6Pm = models.IntegerField()
#     rnSt7Am = models.IntegerField()
#     rnSt7Pm = models.IntegerField()
#     rnSt8 = models.IntegerField(null=True, blank=True)
#     rnSt9 = models.IntegerField(null=True, blank=True)
#     rnSt10 = models.IntegerField(null=True, blank=True)
#     wf3Am = models.CharField(max_length=50)
#     wf3Pm = models.CharField(max_length=50)
#     wf4Am = models.CharField(max_length=50)
#     wf4Pm = models.CharField(max_length=50)
#     wf5Am = models.CharField(max_length=50)
#     wf5Pm = models.CharField(max_length=50)
#     wf6Am = models.CharField(max_length=50)
#     wf6Pm = models.CharField(max_length=50)
#     wf7Am = models.CharField(max_length=50)
#     wf7Pm = models.CharField(max_length=50)
#     wf8 = models.CharField(max_length=50)
#     wf9 = models.CharField(max_length=50)
#     wf10 = models.CharField(max_length=50)

# class SunriseSunset1(models.Model):
#     location = models.CharField(max_length=100, primary_key=True)  # 기본 키로 설정
#     latitude = models.CharField(max_length=20)
#     latitudeNum = models.CharField(max_length=20)
#     locdate = models.CharField(max_length=8)
#     longitude = models.CharField(max_length=20)
#     longitudeNum = models.CharField(max_length=20)
#     sunrise = models.CharField(max_length=10)
#     sunset = models.CharField(max_length=10)
    
#     def __str__(self):
#         return self.location
    
# class AirQualityForecast(models.Model):
#     inform_code = models.CharField(max_length=50)
#     inform_cause = models.TextField()
#     inform_overall = models.TextField()
#     inform_data = models.CharField(max_length=20)  
#     data_time = models.CharField(max_length=20)  

#     def __str__(self):
#         return f"{self.inform_code} - {self.inform_data}"

# class AirQualityGrade(models.Model):
#     air_quality_info = models.ForeignKey(AirQualityForecast, related_name='grades', on_delete=models.CASCADE)
#     region = models.CharField(max_length=100)
#     grade = models.CharField(max_length=50)

#     def __str__(self):
#         return f"{self.region}: {self.grade}"
    

# class WeeklyAirQualityForecast(models.Model):
#     presentation_date = models.DateField(unique=True)

#     class Meta:
#         db_table = 'api_weeklyairqualityforecast'

#     def __str__(self):
#         return f"{self.presentation_date} Air Quality Forecast"

# class FineDustGrade(models.Model):
#     forecast = models.ForeignKey(WeeklyAirQualityForecast, on_delete=models.CASCADE, related_name='grades')
#     forecast_day = models.CharField(max_length=20)  # 예: 'frcstOneCn', 'frcstTwoCn' 등
#     region = models.TextField()  # 지역 정보
#     grade = models.TextField()  # 등급 정보

#     def __str__(self):
#         return f"{self.forecast_day} - {self.region}: {self.grade}"
      
# class WeatherShtTermLandForecast(models.Model):
#     regIdIndex = models.CharField(max_length=100, primary_key=True,serialize=False)
#     regId = models.CharField(max_length=50)  # 기본 키로 설정
#     tmFc = models.CharField(max_length=30)
#     tmEf = models.CharField(max_length=30)
#     mod = models.CharField(max_length=30)
#     ne = models.CharField(max_length=30)
#     stn = models.CharField(max_length=30)
#     c = models.CharField(max_length=30)
#     manId = models.CharField(max_length=30)
#     manFc = models.CharField(max_length=30)
#     w1 = models.CharField(max_length=30)
#     t = models.CharField(max_length=30)
#     w2 = models.CharField(max_length=30)
#     ta = models.CharField(max_length=30)
#     st = models.CharField(max_length=30)
#     sky = models.CharField(max_length=30)
#     prep = models.CharField(max_length=30)
#     wf = models.CharField(max_length=30)
    
    
# class WeatherShtTermOceanForecast(models.Model):
#     regIdIndex = models.CharField(max_length=100, primary_key=True,serialize=False)
#     regId = models.CharField(max_length=50)  # 기본 키로 설정
#     tmFc = models.CharField(max_length=30)
#     tmEf = models.CharField(max_length=30)
#     mod = models.CharField(max_length=30)
#     ne = models.CharField(max_length=30)
#     stn = models.CharField(max_length=30)
#     c = models.CharField(max_length=30)
#     manId = models.CharField(max_length=30)
#     manFc = models.CharField(max_length=30)
#     w1 = models.CharField(max_length=30)
#     t = models.CharField(max_length=30)
#     w2 = models.CharField(max_length=30)
#     s1 = models.CharField(max_length=30)
#     s2 = models.CharField(max_length=30)
#     wh1 = models.CharField(max_length=30)
#     wh2 = models.CharField(max_length=30)
#     sky = models.CharField(max_length=30)
#     prep = models.CharField(max_length=30)
#     wf = models.CharField(max_length=30)
    
# class WeatherShtTermCode(models.Model):
#     regId = models.CharField(max_length=30, primary_key=True, serialize=False)  # 기본 키로 설정
#     tmSt = models.CharField(max_length=30)
#     tmEd = models.CharField(max_length=30)
#     regSp = models.CharField(max_length=30)
#     regName = models.CharField(max_length=30)
    
# class WeatherMidTermLandTempForecast(models.Model):
#     regIdIndex = models.CharField(max_length=100, primary_key=True,serialize=False)
#     regId = models.CharField(max_length=50)  # 기본 키로 설정
#     tmFc = models.CharField(max_length=30)
#     tmEf = models.CharField(max_length=30)
#     mod = models.CharField(max_length=30)
#     stn = models.CharField(max_length=30)
#     c = models.CharField(max_length=30)
#     manId = models.CharField(max_length=30)
#     manFc = models.CharField(max_length=30)
#     regName = models.CharField(max_length=30)
#     min = models.CharField(max_length=30)
#     max = models.CharField(max_length=30)
#     minL = models.CharField(max_length=30)
#     minH = models.CharField(max_length=30)
#     maxL = models.CharField(max_length=30)
#     maxH = models.CharField(max_length=30)
    
# class WeatherMidTermLandStatusForecast(models.Model):
#     regIdIndex = models.CharField(max_length=100, primary_key=True,serialize=False) # 기본 키로 설정
#     regId = models.CharField(max_length=50)  
#     tmFc = models.CharField(max_length=30)
#     tmEf = models.CharField(max_length=30)
#     mod = models.CharField(max_length=30)
#     stn = models.CharField(max_length=30)
#     c = models.CharField(max_length=30)
#     manId = models.CharField(max_length=30, null=True, blank=True)
#     manFc = models.CharField(max_length=30, null=True, blank=True)
#     regName = models.CharField(max_length=30, null=True, blank=True)
#     sky = models.CharField(max_length=30)
#     pre = models.CharField(max_length=30)
#     conf = models.CharField(max_length=30)
#     wf = models.CharField(max_length=30)
#     rnSt = models.CharField(max_length=30)    
    
# class WeatherAlertForecast(models.Model):
#     regIdWrn = models.CharField(max_length=30, primary_key=True, serialize=False)
#     regUp = models.CharField(max_length=30)
#     regUpKo = models.CharField(max_length=30)
#     regId = models.CharField(max_length=30)
#     regKo = models.CharField(max_length=30)
#     tmFc = models.CharField(max_length=30)
#     tmEf = models.CharField(max_length=30)
#     apiTime = models.CharField(max_length=30)
#     wrn = models.CharField(max_length=30)
#     lvl = models.CharField(max_length=30)
#     cmd = models.CharField(max_length=30)
#     edTm = models.CharField(max_length=30)
    
# class WeatherAws1Mobservation(models.Model):
#     tmKstStn = models.CharField(max_length=70, primary_key=True, serialize=False)
#     tmKst = models.CharField(max_length=30)
#     stnId = models.CharField(max_length=30)
#     ta = models.CharField(max_length=30)
#     wd = models.CharField(max_length=30)
#     ws = models.CharField(max_length=30)
#     rnDay = models.CharField(max_length=30)
#     rnHr1 = models.CharField(max_length=30)
#     Hm = models.CharField(max_length=30)
#     PA = models.CharField(max_length=30)
#     PS = models.CharField(max_length=30)

# class WeatherAwsStnInfo(models.Model):
#     stnIdKO = models.CharField(max_length=70, primary_key=True, serialize=False)
#     stnId = models.CharField(max_length=30)
#     lon = models.CharField(max_length=30)
#     lat = models.CharField(max_length=30)
#     stnSp = models.CharField(max_length=30)
#     ht = models.CharField(max_length=30)
#     htWd = models.CharField(max_length=30)
#     stnKo = models.CharField(max_length=30)    
