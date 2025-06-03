# Notes
- [Getting started with OPC-UA](https://medium.com/@muhammadfaiznoh/getting-started-with-opc-ua-in-docker-c68a883d5c65)

## Grafana
```bash
docker build -f docker/grafana.Dockerfile -t grafana-example .
mkdir -p grafana-data
docker run -it -u $(id -u):$(id -g) -p 3000:3000 -v $(pwd)/grafana-data:/var/lib/grafana grafana-example:latest
```

## SQLite
```bash
docker build -f docker/sqlite.Dockerfile -t sqlite-example .
mkdir -p sqlite-data
docker run -it -u $(id -u):$(id -g) -v $(pwd)/sqlite-data:/workspace -w /workspace sqlite-example:latest
```

## OPC-UA server
```bash
docker build -f docker/opcua-server.Dockerfile -t opcua-server-example .
docker run -it -p 4840:4840 opcua-server-example:latest
```

## NodeRED
```bash
docker build -f docker/node-red.Dockerfile -t node-red-example .
mkdir node-red-data
docker run -it -p 1880:1880 -v $(pwd)/node-red-data:/data node-red-example:latest
```

## InfluxDB
```bash
docker build -f docker/influxdb.Dockerfile -t influxdb-example .
mkdir influxdb-data
mkdir influxdb-config
docker run -it -p 8086:8086 -v $(pwd)/influxdb-data:/var/lib/influxdb2 -v influxdb-config:/etc/influxdb2 influxdb-example:latest
```

## Grafana-SQLite stack
```bash
mkdir sqlite-data
mkdir grafana-data
docker build -f docker/sqlite-data-generator.Dockerfile -t sqlite-data-generator .
docker compose -f docker/grafana-sqlite-stack.yml up
```