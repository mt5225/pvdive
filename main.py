import requests
from bs4 import BeautifulSoup
import re
from influxdb import InfluxDBClient
import time
import logging

logging.basicConfig(filename='dive.log',
                    format="%(asctime)s %(levelname)s %(threadName)s %(name)s %(message)s", level=logging.DEBUG)
INFLUX_HOST = 'localhost'
INFLUX_PORT = 8086


def fetch_data(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    week = soup.find(id='seven-day-forecast-body')
    # logging.info(week)
    # get summary
    items = week.find_all("li", class_="forecast-tombstone")
    period_name = [item.find(class_="txt-ctr-caps").get_text()
                   for item in items]
    w_summary = [item.find(class_="forecast-icon").get('title')
                 for item in items]
    w_detail = [item.get_text() for item in items]

    items = soup.find_all("li", class_="forecast-tombstone")

    # get the details
    detail_week = soup.find(id='detailed-forecast-body')
    detail_items = detail_week.find_all('div', class_='forecast-text')
    forecase_details = [item.get_text().replace(
        ' ', '\ ').replace(',', '.\ ') for item in detail_items]
    # logging.info(forecase_details)

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
                  "w_swell_ft": swell_ft(t[1]),
                  "detail_s": forecase_details[idx],
                  }
        out_arr.append(dict(record))
    # logging.info(out_arr)
    return out_arr


def swell_ft(ftstr):
    if '<' in ftstr:
        return 0
    else:
        return int(ftstr.replace("ft", "").split("-")[0])


def write_influx(out_arr, location):
    client = InfluxDBClient(host=INFLUX_HOST, port=INFLUX_PORT)
    client.create_database('dive')
    measurement_name = 'dive'

    data = []
    idx = 0
    for record in out_arr:
        data.append("{measurement},location={location},period_name={period_name},w_summary={w_summary},w_wind_s={w_wind_s},w_swell_s={w_swell_s},detail_s={detail_s} w_wind_kt={w_wind_kt}i,w_swell_ft={w_swell_ft}i {timestamp}".
                    format(measurement=measurement_name,
                           location=location,
                           period_name="{idx}_{period_name}".format(
                               idx=idx, period_name=record["period_name"]),
                           w_summary=record[
                               "w_summary"].replace(' ', '_'),
                           w_wind_s=record[
                               "w_wind_s"].replace(' ', '_'),
                           w_swell_s=record[
                               "w_swell_s"].replace(' ', ''),
                           w_wind_kt=record[
                               "w_wind_kt"],
                           w_swell_ft=record[
                               "w_swell_ft"],
                           detail_s=record["detail_s"],
                           timestamp=int(time.time() * 1000)))
        idx = idx + 1

    logging.debug(data)

    client_write_start_time = time.perf_counter()
    client.write_points(data, database='dive',
                        time_precision='ms', batch_size=10, protocol='line')

    client_write_end_time = time.perf_counter()

    logging.info("Client Library Write: {time}s".format(
        time=client_write_end_time - client_write_start_time))


if __name__ == "__main__":
    sites = [
        {
            "location": "Cabrillo",
            "url": "https://marine.weather.gov/MapClick.php?lon=-118.28481&lat=33.70772#.YknqXpPYqBQ",
        },
        {
            "location": "Malaga",
            "url": "https://marine.weather.gov/MapClick.php?lon=-118.39739&lat=33.80322#.YkuD7ZPYqBQ",
        },
        {
            "location": "Redondo",
            "url": "https://marine.weather.gov/MapClick.php?lon=-118.39165&lat=33.83646#.Yku_TpPMKBQ",
        },
    ]
    for site in sites:
        data = fetch_data(site['url'])
        time.sleep(5)
        logging.info("sleep for 5 seconds")
        write_influx(data, site['location'])
