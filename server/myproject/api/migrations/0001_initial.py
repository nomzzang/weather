# Generated by Django 4.2.5 on 2024-03-11 17:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AirQualityForecast',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inform_code', models.CharField(max_length=50)),
                ('inform_cause', models.TextField()),
                ('inform_overall', models.TextField()),
                ('inform_data', models.CharField(max_length=20)),
                ('data_time', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='ApiResponse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resultCode', models.CharField(max_length=20)),
                ('resultMsg', models.CharField(max_length=255)),
                ('dataType', models.CharField(max_length=20)),
                ('pageNo', models.IntegerField()),
                ('numOfRows', models.IntegerField()),
                ('totalCount', models.IntegerField()),
                ('filetype', models.CharField(blank=True, max_length=20, null=True)),
                ('version', models.CharField(blank=True, max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='MidTermLandForecast',
            fields=[
                ('regId', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('rnSt3Am', models.IntegerField()),
                ('rnSt3Pm', models.IntegerField()),
                ('rnSt4Am', models.IntegerField()),
                ('rnSt4Pm', models.IntegerField()),
                ('rnSt5Am', models.IntegerField()),
                ('rnSt5Pm', models.IntegerField()),
                ('rnSt6Am', models.IntegerField()),
                ('rnSt6Pm', models.IntegerField()),
                ('rnSt7Am', models.IntegerField()),
                ('rnSt7Pm', models.IntegerField()),
                ('rnSt8', models.IntegerField(blank=True, null=True)),
                ('rnSt9', models.IntegerField(blank=True, null=True)),
                ('rnSt10', models.IntegerField(blank=True, null=True)),
                ('wf3Am', models.CharField(max_length=50)),
                ('wf3Pm', models.CharField(max_length=50)),
                ('wf4Am', models.CharField(max_length=50)),
                ('wf4Pm', models.CharField(max_length=50)),
                ('wf5Am', models.CharField(max_length=50)),
                ('wf5Pm', models.CharField(max_length=50)),
                ('wf6Am', models.CharField(max_length=50)),
                ('wf6Pm', models.CharField(max_length=50)),
                ('wf7Am', models.CharField(max_length=50)),
                ('wf7Pm', models.CharField(max_length=50)),
                ('wf8', models.CharField(max_length=50)),
                ('wf9', models.CharField(max_length=50)),
                ('wf10', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='MidTermTemperature',
            fields=[
                ('regId', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('taMin3', models.IntegerField()),
                ('taMax3', models.IntegerField()),
                ('taMin4', models.IntegerField()),
                ('taMax4', models.IntegerField()),
                ('taMin5', models.IntegerField()),
                ('taMax5', models.IntegerField()),
                ('taMin6', models.IntegerField()),
                ('taMax6', models.IntegerField()),
                ('taMin7', models.IntegerField()),
                ('taMax7', models.IntegerField()),
                ('taMin8', models.IntegerField()),
                ('taMax8', models.IntegerField()),
                ('taMin9', models.IntegerField()),
                ('taMax9', models.IntegerField()),
                ('taMin10', models.IntegerField()),
                ('taMax10', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='SidoRealTimeAirQuality',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pm25Grade1h', models.CharField(blank=True, max_length=10, null=True)),
                ('pm10Value24', models.CharField(blank=True, max_length=10, null=True)),
                ('so2Value', models.CharField(blank=True, max_length=10, null=True)),
                ('pm10Grade1h', models.CharField(blank=True, max_length=10, null=True)),
                ('pm10Value', models.CharField(blank=True, max_length=10, null=True)),
                ('o3Grade', models.CharField(blank=True, max_length=10, null=True)),
                ('pm25Flag', models.CharField(blank=True, max_length=10, null=True)),
                ('khaiGrade', models.CharField(blank=True, max_length=10, null=True)),
                ('pm25Value', models.CharField(blank=True, max_length=10, null=True)),
                ('no2Flag', models.CharField(blank=True, max_length=10, null=True)),
                ('mangName', models.CharField(max_length=50)),
                ('stationName', models.CharField(max_length=50)),
                ('no2Value', models.CharField(blank=True, max_length=10, null=True)),
                ('so2Grade', models.CharField(blank=True, max_length=10, null=True)),
                ('stationCode', models.CharField(max_length=50)),
                ('coFlag', models.CharField(blank=True, max_length=10, null=True)),
                ('khaiValue', models.CharField(blank=True, max_length=10, null=True)),
                ('coValue', models.CharField(blank=True, max_length=10, null=True)),
                ('pm10Flag', models.CharField(blank=True, max_length=10, null=True)),
                ('sidoName', models.CharField(max_length=50)),
                ('pm25Value24', models.CharField(blank=True, max_length=10, null=True)),
                ('no2Grade', models.CharField(blank=True, max_length=10, null=True)),
                ('o3Flag', models.CharField(blank=True, max_length=10, null=True)),
                ('pm25Grade', models.CharField(blank=True, max_length=10, null=True)),
                ('so2Flag', models.CharField(blank=True, max_length=10, null=True)),
                ('coGrade', models.CharField(blank=True, max_length=10, null=True)),
                ('dataTime', models.CharField(max_length=255)),
                ('pm10Grade', models.CharField(blank=True, max_length=10, null=True)),
                ('o3Value', models.CharField(blank=True, max_length=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SunriseSunset1',
            fields=[
                ('location', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('latitude', models.CharField(max_length=20)),
                ('latitudeNum', models.CharField(max_length=20)),
                ('locdate', models.CharField(max_length=8)),
                ('longitude', models.CharField(max_length=20)),
                ('longitudeNum', models.CharField(max_length=20)),
                ('sunrise', models.CharField(max_length=10)),
                ('sunset', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='WeatherAlertForecast',
            fields=[
                ('regIdWrn', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('regUp', models.CharField(max_length=30)),
                ('regUpKo', models.CharField(max_length=30)),
                ('regId', models.CharField(max_length=30)),
                ('regKo', models.CharField(max_length=30)),
                ('tmFc', models.CharField(max_length=30)),
                ('tmEf', models.CharField(max_length=30)),
                ('apiTime', models.CharField(max_length=30)),
                ('wrn', models.CharField(max_length=30)),
                ('lvl', models.CharField(max_length=30)),
                ('cmd', models.CharField(max_length=30)),
                ('edTm', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='WeatherMidTermLandStatusForecast',
            fields=[
                ('regIdIndex', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('regId', models.CharField(max_length=50)),
                ('tmFc', models.CharField(max_length=30)),
                ('tmEf', models.CharField(max_length=30)),
                ('mod', models.CharField(max_length=30)),
                ('stn', models.CharField(max_length=30)),
                ('c', models.CharField(max_length=30)),
                ('manId', models.CharField(blank=True, max_length=30, null=True)),
                ('manFc', models.CharField(blank=True, max_length=30, null=True)),
                ('regName', models.CharField(blank=True, max_length=30, null=True)),
                ('sky', models.CharField(max_length=30)),
                ('pre', models.CharField(max_length=30)),
                ('conf', models.CharField(max_length=30)),
                ('wf', models.CharField(max_length=30)),
                ('rnSt', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='WeatherMidTermLandTempForecast',
            fields=[
                ('regIdIndex', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('regId', models.CharField(max_length=50)),
                ('tmFc', models.CharField(max_length=30)),
                ('tmEf', models.CharField(max_length=30)),
                ('mod', models.CharField(max_length=30)),
                ('stn', models.CharField(max_length=30)),
                ('c', models.CharField(max_length=30)),
                ('manId', models.CharField(max_length=30)),
                ('manFc', models.CharField(max_length=30)),
                ('regName', models.CharField(max_length=30)),
                ('min', models.CharField(max_length=30)),
                ('max', models.CharField(max_length=30)),
                ('minL', models.CharField(max_length=30)),
                ('minH', models.CharField(max_length=30)),
                ('maxL', models.CharField(max_length=30)),
                ('maxH', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='WeatherShtTermCode',
            fields=[
                ('regId', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('tmSt', models.CharField(max_length=30)),
                ('tmEd', models.CharField(max_length=30)),
                ('regSp', models.CharField(max_length=30)),
                ('regName', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='WeatherShtTermLandForecast',
            fields=[
                ('regIdIndex', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('regId', models.CharField(max_length=50)),
                ('tmFc', models.CharField(max_length=30)),
                ('tmEf', models.CharField(max_length=30)),
                ('mod', models.CharField(max_length=30)),
                ('ne', models.CharField(max_length=30)),
                ('stn', models.CharField(max_length=30)),
                ('c', models.CharField(max_length=30)),
                ('manId', models.CharField(max_length=30)),
                ('manFc', models.CharField(max_length=30)),
                ('w1', models.CharField(max_length=30)),
                ('t', models.CharField(max_length=30)),
                ('w2', models.CharField(max_length=30)),
                ('ta', models.CharField(max_length=30)),
                ('st', models.CharField(max_length=30)),
                ('sky', models.CharField(max_length=30)),
                ('prep', models.CharField(max_length=30)),
                ('wf', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='WeatherShtTermOceanForecast',
            fields=[
                ('regIdIndex', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('regId', models.CharField(max_length=50)),
                ('tmFc', models.CharField(max_length=30)),
                ('tmEf', models.CharField(max_length=30)),
                ('mod', models.CharField(max_length=30)),
                ('ne', models.CharField(max_length=30)),
                ('stn', models.CharField(max_length=30)),
                ('c', models.CharField(max_length=30)),
                ('manId', models.CharField(max_length=30)),
                ('manFc', models.CharField(max_length=30)),
                ('w1', models.CharField(max_length=30)),
                ('t', models.CharField(max_length=30)),
                ('w2', models.CharField(max_length=30)),
                ('s1', models.CharField(max_length=30)),
                ('s2', models.CharField(max_length=30)),
                ('wh1', models.CharField(max_length=30)),
                ('wh2', models.CharField(max_length=30)),
                ('sky', models.CharField(max_length=30)),
                ('prep', models.CharField(max_length=30)),
                ('wf', models.CharField(max_length=30)),
            ],
        ),
        
        migrations.CreateModel(
            name='WeatherAws1Mobservation',
            fields=[
                ('tmKstStn', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('tmKst', models.CharField(max_length=50)),
                ('stnId', models.CharField(max_length=50)),
                ('ta', models.CharField(max_length=30)),
                ('wd', models.CharField(max_length=30)),
                ('ws', models.CharField(max_length=30)),
                ('rnDay', models.CharField(max_length=30)),
                ('rnHr1', models.CharField(max_length=30)),
                ('Hm', models.CharField(max_length=30)),
                ('PA', models.CharField(max_length=30)),
                ('PS', models.CharField(max_length=30)),
            ],   
        ),
        migrations.CreateModel(
            name='WeatherAwsStnInfo',
            fields=[
                ('stnIdKO', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('stnId', models.CharField(max_length=50)),
                ('lon', models.CharField(max_length=30)),
                ('lat', models.CharField(max_length=30)),
                ('stnSp', models.CharField(max_length=30)),
                ('ht', models.CharField(max_length=30)),
                ('htWd', models.CharField(max_length=30)),
                ('stnKo', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='WeeklyAirQualityForecast',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('presentation_date', models.DateField(unique=True)),
            ],
            options={
                'db_table': 'api_weeklyairqualityforecast',
            },
        ),
        migrations.CreateModel(
            name='FineDustGrade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('forecast_day', models.CharField(max_length=20)),
                ('region', models.TextField()),
                ('grade', models.TextField()),
                ('forecast', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='grades', to='api.weeklyairqualityforecast')),
            ],
        ),
        migrations.CreateModel(
            name='AirQualityGrade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('region', models.CharField(max_length=100)),
                ('grade', models.CharField(max_length=50)),
                ('air_quality_info', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='grades', to='api.airqualityforecast')),
            ],
        ),
    ]