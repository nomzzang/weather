from rest_framework import serializers
from .models import SunriseSunset1, SidoRealTimeAirQuality, MidTermTemperature, MidTermLandForecast, AirQualityForecast, AirQualityGrade

class SunriseSunset1Serializer(serializers.ModelSerializer):  # 이 클래스 이름이 정확해야 합니다.
    class Meta:
        model = SunriseSunset1
        fields = '__all__'  # 모든 필드를 포함하도록 설정합니다.

class AirQualitySerializer(serializers.ModelSerializer):
    class Meta:
        model = SidoRealTimeAirQuality
        fields = '__all__'
        
class WeatherForecastSerializer(serializers.ModelSerializer):
    class Meta:
        model = MidTermTemperature
        fields = '__all__'

class WeatherForecastDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = MidTermLandForecast
        fields = '__all__'

class AirQualityInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirQualityForecast
        fields = '__all__'

class AirQualityGradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirQualityGrade
        fields = '__all__'
        
        
        
        
        
        
        
        
        