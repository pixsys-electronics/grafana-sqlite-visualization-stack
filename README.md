# Notes
- [Getting started with OPC-UA](https://medium.com/@muhammadfaiznoh/getting-started-with-opc-ua-in-docker-c68a883d5c65)

## Grafana

### Run from scratch image
```bash
# use *--userns=keep-id* to make sure that the host user that has created the folders for bind-mount is correctly mapped to the container
# so that the permissions match
# then, use *-u $(id -u):$(id -g)* to actually use your mapped user as container user
podman run --userns=keep-id -u $(id -u):$(id -g) -v $(pwd)/grafana-data:/var/lib/grafana -p 3000:3000 grafana/grafana-enterprise:latest
```

### Run from custom image
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
# create folders for persistent data
mkdir sqlite-data
mkdir grafana-data
# change 
chmod -R 777 grafana-data
chmod -R 777 sqlite-data
podman build -f docker/sqlite-data-generator.Dockerfile -t sqlite-data-generator .
PODMAN_USERNS=keep-id podman compose -f docker/grafana-sqlite-stack.yml up
```