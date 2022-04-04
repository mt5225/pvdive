#!/usr/bin/env python3

from influxdb import InfluxDBClient
import uuid
import random
import time

client = InfluxDBClient(host='localhost', port=8086)
client.create_database('writetest')

measurement_name = 'm1'
number_of_points = 250000
data_end_time = int(time.time() * 1000)  # milliseconds

location_tags = ["reservoir",
                 "orchard",
                 "vineyard",
                 "quarry",
                 "hospital",
                 "bakery",
                 "warehouse",
                 "outhouse",
                 "restaurant",
                 "cafeteria",
                 "delicatessen",
                 "office"]

fruit_tags = ["apple",
              "banana",
              "cantaloupe",
              "cherry",
              "coconut",
              "durian",
              "fig",
              "gooseberry",
              "grape",
              "grapefruit",
              "guava",
              "lemon",
              "lime",
              "lychee",
              "mango",
              "papaya",
              "passionfruit",
              "peach",
              "pineapple",
              "plum",
              "strawberry",
              "tangerine",
              "tomato",
              "watermelon"]

id_tags = []
for i in range(100):
    id_tags.append(str(uuid.uuid4()))

data = []
data.append("{measurement},location={location},fruit={fruit},id={id} x={x},y={y},z={z}i {timestamp}"
            .format(measurement=measurement_name,
                    location=random.choice(location_tags),
                    fruit=random.choice(fruit_tags),
                    id=random.choice(id_tags),
                    x=round(random.random(), 4),
                    y=round(random.random(), 4),
                    z=random.randint(0, 50),
                    timestamp=data_end_time))
current_point_time = data_end_time
for i in range(number_of_points-1):
    current_point_time = current_point_time - random.randint(1, 100)
    data.append("{measurement},location={location},fruit={fruit},id={id} x={x},y={y},z={z}i {timestamp}"
                .format(measurement=measurement_name,
                        location=random.choice(location_tags),
                        fruit=random.choice(fruit_tags),
                        id=random.choice(id_tags),
                        x=round(random.random(), 4),
                        y=round(random.random(), 4),
                        z=random.randint(0, 50),
                        timestamp=current_point_time))

client_write_start_time = time.perf_counter()

client.write_points(data, database='writetest',
                    time_precision='ms', batch_size=10000, protocol='line')

client_write_end_time = time.perf_counter()

print("Client Library Write: {time}s".format(
    time=client_write_end_time - client_write_start_time))
