# how to run

### start docker

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

### import dashboard into grafana

### install python dependencies

```
pip3 install -r requirements.txt
```

### fetch data

```
python ./main.py
```
