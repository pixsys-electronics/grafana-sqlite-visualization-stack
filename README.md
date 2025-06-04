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

## NodeRED
```bash
docker build -f docker/node-red.Dockerfile -t node-red-example .
mkdir node-red-data
docker run -it -p 1880:1880 -v $(pwd)/node-red-data:/data node-red-example:latest
```

## Grafana-SQLite stack
First, you need an .env file that contains:
- UID of the container user
- GID of the container user
- ROOT_DIR, which is the base path for the persistent folders. Make sure you use the absolute path

**Note: the preferred way to configure the container user is to make sure it matches the host user, so that there are no permissions issues**

```bash
echo UID=$(id -u) >> .env
echo GID=$(id -u) >> .env
```

Then, create the folders to use as persistent volumes:
```bash
# create folders for persistent data
mkdir sqlite-data
mkdir grafana-data
```

And finally run the compose:
```bash
PODMAN_USERNS=keep-id ROOT_DIR=$(pwd) podman-compose -f docker/grafana-sqlite-stack.yml up --build
```