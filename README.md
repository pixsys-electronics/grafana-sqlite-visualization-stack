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
If you want to run a stand-alone grafana container to make sure it works outside of a compose, run:
```bash
# use *--userns=keep-id* to make sure that the host user that has created the folders for bind-mount is correctly mapped to the container
# so that the permissions match
# then, use *-u $(id -u):$(id -g)* to actually use your mapped user as container user
podman run --userns=keep-id -u $(id -u):$(id -g) -v $(pwd)/grafana-data:/var/lib/grafana -v $(pwd)/sqlite-data:/db -p 3000:3000 -e GF_PLUGINS_PREINSTALL="frser-sqlite-datasource" grafana/grafana-enterprise:12.0.1
```
**Note: make sure your container has access to internet so that grafana can download its plugins. This is not trivial since some firewall rules for Docker/Podman must be set. For the sake of ease and for development usage, add --network=host to the command above**

For further informations about grafana on docker, visit [this page](https://grafana.com/docs/grafana/latest/setup-grafana/installation/docker/).

### SQLite data generator
If you want to run a stand-alone SQLite data generator container, run:
```bash
podman build -t sqlite-data-generator-example -f docker/sqlite-data-generator.Dockerfile .
podman run --userns=keep-id -u $(id -u):$(id -g) -v $(pwd)/sqlite-data:/workspace/sqlite-data sqlite-data-generator-example
```

## Run with podman-compose

**Note: the preferred way to configure the container user is to make sure it matches the host user that has created the directories to mount, so that there are no permissions issues. Note2: both containers of the podman-compose runs with network_mode=host by default**

Set *ROOT_DIR* to the root directory where *grafana-data* and *sqlite-data* have been created, then set *MY_UID* and *MY_GID* so that they match the user that has created the directories to mount (grafana-data and sqlite-data).

Finally, run the compose:
```bash
MY_UID=$(id -u) MY_GID=$(id -g) ROOT_DIR=$(pwd) podman-compose -f docker/grafana-sqlite-stack.yml up --build
```

## Grafana configuration
To access the Grafana dashboard, navigate to the host device URL at port 3000 (the default port for Grafana). If you have access to the URL bar of the browser of your target device, navigate to:
*127.0.0.1:3000*. You should see the default login page of Grafana. Access using:
- user: admin
- password: admin

then you can optionally modify the default password (suggested).
![Login](assets/login.png)

In order to plot data from the SQLite database, you first need to configure the [data-source for SQLite](https://grafana.com/docs/grafana/latest/datasources/). Go to Home->Connections->Data sources->Add data source, look for SQLite (the plugin installed using *GF_PLUGINS_PREINSTALL*), select it and use */db/sample.db* as path for the database file. You can leave the rest of the configuration as it is, then press "Save and test".
![Add data source](assets/add_data_source.png)

Then, go to Home->Dashboards and create a new dashboard. Select the previous configured data-source as data source of the dashboard and create the dashboard.
![Add dashboard](assets/add_dashboard.png)


Then, scroll down to the query input file and write:
```mysql
SELECT timestamp as ts, value
FROM table_sample
```
save the query (or click outside the input text of the query) and you should see a plot of the default panel. 
![Plot data](assets/dashboard_panel.png)
