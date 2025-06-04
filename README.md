# Grafana-SQLite visualization stack
## Description
This repository shows how setup a simple stack where [Grafana](https://grafana.com/) plots some time-series data
retrieved from a SQLite database using [Docker](https://www.docker.com/). The following procedure can be applied to a WebPanel that runs [codesys](https://www.codesys.com/), which can save data gathered from different input devices into a SQLite database. In this example, a python script is used to create a SQLite database and continuosly add an entry into an example table, while Grafana shows the values of that table.

## Setup
You will need:
- a Linux distro
- [podman](https://podman.io/)(v1.0.6) or [docker](https://www.docker.com/)(v28.1.1)

**Note: some podman-compose options may change between versions. If the following code snippets does not work for you because you have a different podman version, check [the official repo for podman-compose](https://github.com/containers/podman-compose), checkout to the correct branch and look for some options changes**

To have persisent storage for both grafana and SQLite, create 2 directories:
```bash
mkdir grafana-data
mkdir sqlite-data
```

## Run with podman run
### Grafana
If you want to run a grafana container separately and test bind-mounts permissions, run:
```bash
# use *--userns=keep-id* to make sure that the host user that has created the folders for bind-mount is correctly mapped to the container
# so that the permissions match
# then, use *-u $(id -u):$(id -g)* to actually use your mapped user as container user
podman run --userns=keep-id -u $(id -u):$(id -g) -v $(pwd)/grafana-data:/var/lib/grafana -p 3000:3000 -e GF_PLUGINS_PREINSTALL="frser-sqlite-datasource" grafana/grafana-enterprise:12.0.1
```
**Note: make sure your container has access to internet so that grafana can download its plugins. This is not trivial since some firewall rules for Docker/Podman must be set. For the sake of ease and for development usage, add --network=host to the command above**

For further informations about grafana on docker, visit [this page](https://grafana.com/docs/grafana/latest/setup-grafana/installation/docker/).

## Run with podman-compose

**Note: the preferred way to configure the container user is to make sure it matches the host user that has created the directories to mount, so that there are no permissions issues.**

Set *ROOT_DIR* to the root directory where *grafana-data* and *sqlite-data* have been created, then set *MY_UID* and *MY_GID* so that they match the user that has created the directories to mount (grafana-data and sqlite-data).

Finally, run the compose:
```bash
MY_UID=$(id -u) MY_GID=$(id -g) ROOT_DIR=$(pwd) podman-compose -f docker/grafana-sqlite-stack.yml up --build
```

## NodeRED
```bash
docker build -f docker/node-red.Dockerfile -t node-red-example .
mkdir node-red-data
docker run -it -p 1880:1880 -v $(pwd)/node-red-data:/data node-red-example:latest
```
