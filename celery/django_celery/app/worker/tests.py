from django.test import TestCase
from .models import UltraShortTermForecast, UltraShortTermLiveStatus, ShortTermForecast

class WeatherDataModelTests(TestCase):
    def test_ultra_short_term_forecast_creation(self):
        """초단기 예보 모델 인스턴스 생성 및 필드 값 검증 테스트"""
        forecast = UltraShortTermForecast.objects.create(
            base_date="20240323",
            base_time="0500",
            category="TMP",
            fcst_date="20240323",
            fcst_time="0600",
            fcst_value="7",
            nx=55,
            ny=127
        )
        self.assertEqual(forecast.base_date, "20240323")
        self.assertEqual(forecast.fcst_value, "7")

    def test_ultra_short_term_live_status_creation(self):
        """초단기 실황 모델 인스턴스 생성 및 필드 값 검증 테스트"""
        live_status = UltraShortTermLiveStatus.objects.create(
            base_date="20240323",
            base_time="0200",
            category="T1H",
            obsr_value="9",
            nx=55,
            ny=127
        )
        self.assertEqual(live_status.obsr_value, "9")

    def test_short_term_forecast_creation(self):
        """단기 예보 모델 인스턴스 생성 및 필드 값 검증 테스트"""
        forecast = ShortTermForecast.objects.create(
            base_date="20240323",
            base_time="0500",
            category="TMP",
            fcst_date="20240326",
            fcst_time="0000",
            fcst_value="9",
            nx=55,
            ny=127
        )
        self.assertEqual(forecast.fcst_value, "9")