# Notes
- [Getting started with OPC-UA](https://medium.com/@muhammadfaiznoh/getting-started-with-opc-ua-in-docker-c68a883d5c65)

## Grafana

```bash
docker build -f docker/grafana.Dockerfile -t grafana .
mkdir grafana-data
docker run -it -v grafana-data:/var/lib/grafana -p 3000:3000 grafana:latest
```

## OPC-UA server
```bash
docker build -f docker/opcua-server.Dockerfile -t opcua-server .
docker run -it -p 4840:4840 opcua-server:latest
```

## NodeRED
```bash
docker build -f docker/node-red.Dockerfile -t node-red .
mkdir node-red-data
docker run -it -p 4840:4840 opcua-server:latest
```