from unittest import skip
import requests
from bs4 import BeautifulSoup
import re
from influxdb import InfluxDBClient
import time

# fetch the data
# url = "https://forecast.weather.gov/MapClick.php?lat=41.884250000000065&lon=-87.63244999999995#.XtpdeOfhXIX"

url = "https://marine.weather.gov/MapClick.php?lon=-118.28481&lat=33.70772#.YknqXpPYqBQ"
r = requests.get(url)

soup = BeautifulSoup(r.content, "html.parser")
week = soup.find(id="seven-day-forecast-body")
# print(week)

items = soup.find_all("li", class_="forecast-tombstone")
period_name = [item.find(class_="txt-ctr-caps").get_text() for item in items]
w_summary = [item.find(class_="forecast-icon").get('title') for item in items]
w_detail = [item.get_text() for item in items]


items = soup.find_all("li", class_="forecast-tombstone")

out_arr = []

for idx in range(len(period_name)):
    if w_detail[idx].find('kt') == -1:
        continue
    t = w_detail[idx].replace(period_name[idx], "").split("kt")
    record = {"period_name": period_name[idx],
              "w_summary": w_summary[idx],
              "w_wind_s": t[0],
              "w_swell_s": t[1],
              "w_wind_kt": int(re.findall(r'\d+', t[0])[0]),
              "w_swell_ft": int(t[1].replace("ft", "").split("-")[0]),
              }
    out_arr.append(dict(record))

# print(out_arr)


# write to influxdb
client = InfluxDBClient(host='localhost', port=8086)
client.create_database('dive')
measurement_name = 'dive'

data = []
idx = 0
for record in out_arr:
    data.append("{measurement},location={location},period_name={period_name},w_summary={w_summary},w_wind_s={w_wind_s},w_swell_s={w_swell_s} w_wind_kt={w_wind_kt}i,w_swell_ft={w_swell_ft}i {timestamp}".
                format(measurement=measurement_name,
                       location="Cabrillo",
                       period_name=f"{idx}_{record['period_name']}",
                       w_summary=record[
                           "w_summary"].replace(' ', '_'),
                       w_wind_s=record[
                           "w_wind_s"].replace(' ', '_'),
                       w_swell_s=record[
                           "w_swell_s"],
                       w_wind_kt=record[
                           "w_wind_kt"],
                       w_swell_ft=record[
                           "w_swell_ft"],
                       timestamp=int(time.time() * 1000)))
    idx = idx + 1

print(data)

client_write_start_time = time.perf_counter()
client.write_points(data, database='dive',
                    time_precision='ms', batch_size=len(out_arr), protocol='line')

client_write_end_time = time.perf_counter()

print("Client Library Write: {time}s".format(
    time=client_write_end_time - client_write_start_time))
