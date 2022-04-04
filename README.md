```
docker run -d \
  --name docker-influxdb-grafana \
  -p 3003:3003 \
  -p 3004:8083 \
  -p 8086:8086 \
  -v influxdb:/var/lib/influxdb \
  -v grafana:/var/lib/grafana \
  philhawthorne/docker-influxdb-grafana:latest
```

SELECT mean("x") FROM "m1" WHERE $timeFilter GROUP BY time($\_\_interval) fill(null)

[{'period_name': 'ThisAfternoon', 'w_summary': 'Partly Sunny', 'w_wind_s': 'WSW 10', 'w_swell_s': '3ft', 'w_wind_kt': 10, 'w_swell_ft': 3},

{'period_name': 'Tonight', 'w_summary': 'Patchy Fog', 'w_wind_s': 'WSW 10', 'w_swell_s': '3-4ft', 'w_wind_kt': 10, 'w_swell_ft': 3}, {'period_name': 'Monday', 'w_summary': 'Patchy Fog', 'w_wind_s': 'WSW 10', 'w_swell_s': '4-5ft', 'w_wind_kt': 10, 'w_swell_ft': 4}, {'period_name': 'MondayNight', 'w_summary': 'Mostly Clear', 'w_wind_s': 'W 10', 'w_swell_s': '3-4ft', 'w_wind_kt': 10, 'w_swell_ft': 3}, {'period_name': 'Tuesday', 'w_summary': 'Sunny', 'w_wind_s': 'WSW 10', 'w_swell_s': '4-5ft', 'w_wind_kt': 10, 'w_swell_ft': 4}, {'period_name': 'TuesdayNight', 'w_summary': 'Mostly Clear', 'w_wind_s': 'WSW 10', 'w_swell_s': '3ft', 'w_wind_kt': 10, 'w_swell_ft': 3}, {'period_name': 'Wednesday', 'w_summary': 'Sunny', 'w_wind_s': 'W 10', 'w_swell_s': '3ft', 'w_wind_kt': 10, 'w_swell_ft': 3}, {'period_name': 'WednesdayNight', 'w_summary': 'Mostly Clear', 'w_wind_s': 'W 10', 'w_swell_s': '2-3ft', 'w_wind_kt': 10, 'w_swell_ft': 2}, {'period_name': 'Thursday', 'w_summary': 'Sunny', 'w_wind_s': 'NW 10', 'w_swell_s': '2-3ft', 'w_wind_kt': 10, 'w_swell_ft': 2}]

['dive,location=Cabrillo,period_name=Tonight w_summary=Patchy Fog,w_wind_s=WSW 10,w_swell_s=3-4ft,w_wind_kt=10i,w_swell_ft=3i 1649030693629',

'dive,location=Cabrillo,period_name=Monday w_summary=Patchy Fog,w_wind_s=WSW 10,w_swell_s=4-5ft,w_wind_kt=10i,w_swell_ft=4i 1649030693629',

name: dive
time location period_name w_summary w_swell_ft w_swell_s w_wind_kt w_wind_s

---

1649045268924000000 Cabrillo Monday Patchy_Fog 4 4-5ft 10 WSW_10
1649045268924000000 Cabrillo MondayNight Mostly_Clear 3 3-4ft 10 W_10
1649045268924000000 Cabrillo Thursday Sunny 2 2-3ft 10 NW_10

select w_summary from dive where period_name =~/$period_name$/ and $timeFilter
