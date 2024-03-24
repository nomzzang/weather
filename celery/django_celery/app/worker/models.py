from django.db import models

class UltraShortTermLiveStatus(models.Model):
    
    base_date = models.CharField(max_length=8)  # YYYYMMDD
    base_time = models.CharField(max_length=4)  # HHMM
    nx = models.IntegerField()
    ny = models.IntegerField()
    
    # 실황 값
    pty = models.CharField(max_length=10, blank=True, null=True)  # 강수형태
    reh = models.IntegerField(blank=True, null=True)  # 습도
    rn1 = models.FloatField(blank=True, null=True)  # 1시간 강수량
    t1h = models.FloatField(blank=True, null=True)  # 기온
    uuu = models.FloatField(blank=True, null=True)  # 동서바람성분
    vvv = models.FloatField(blank=True, null=True)  # 남북바람성분
    vec = models.FloatField(blank=True, null=True)  # 풍향
    wsd = models.FloatField(blank=True, null=True)  # 풍속
    
    class Meta:
        unique_together = (('nx', 'ny', 'base_date', 'base_time'),)
        indexes = [
            models.Index(fields=['nx', 'ny', 'base_date', 'base_time']),
        ]

    def __str__(self):
        return f"{self.base_date} {self.base_time} - NX: {self.nx}, NY: {self.ny}"
    
class UltraShortTermForecast(models.Model):
    base_date = models.CharField(max_length=8)  # YYYYMMDD
    base_time = models.CharField(max_length=4)  # HHMM
    category = models.CharField(max_length=10)  # 예보 카테고리
    fcst_date = models.CharField(max_length=8)  # 예보 날짜 YYYYMMDD
    fcst_time = models.CharField(max_length=4)  # 예보 시간 HHMM
    fcst_value = models.CharField(max_length=255)  # 예보 값
    nx = models.IntegerField()  # 격자 x 좌표
    ny = models.IntegerField()  # 격자 y 좌표
    
    class Meta:
        unique_together = (('nx', 'ny', 'base_date', 'base_time', 'category', 'fcst_date', 'fcst_time'),)
        indexes = [
            models.Index(fields=['nx', 'ny', 'base_date', 'base_time', 'category', 'fcst_date', 'fcst_time']),
        ]

    def __str__(self):
        return f"{self.category} forecast for NX:{self.nx}, NY:{self.ny} on {self.fcst_date} {self.fcst_time}"
    
class ShortTermForecast(models.Model):
    base_date = models.CharField(max_length=8)  # YYYYMMDD
    base_time = models.CharField(max_length=4)  # HHMM
    category = models.CharField(max_length=10)  # 예보 카테고리
    fcst_date = models.CharField(max_length=8)  # 예보 날짜 YYYYMMDD
    fcst_time = models.CharField(max_length=4)  # 예보 시간 HHMM
    fcst_value = models.CharField(max_length=255)  # 예보 값 (문자열로 다양한 형태의 예보값을 허용)
    nx = models.IntegerField()  # 격자 x 좌표
    ny = models.IntegerField()  # 격자 y 좌표
    
    class Meta:
        unique_together = (('nx', 'ny', 'base_date', 'base_time', 'category', 'fcst_date', 'fcst_time'),)
        indexes = [
            models.Index(fields=['nx', 'ny', 'base_date', 'base_time', 'category', 'fcst_date', 'fcst_time']),
        ]

    def __str__(self):
        return f"{self.category} forecast for NX:{self.nx}, NY:{self.ny} on {self.fcst_date} {self.fcst_time}"
    