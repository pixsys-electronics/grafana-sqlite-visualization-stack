Setup a Grafana-SQLite visualization stack using Podman
===============
<p align="left">
    <img src="assets/grafana-logo.png" width="10%">
    <img src="assets/sqlite-logo.png" width="10%">
    <img src="assets/podman-logo.png" width="10%">
</p>

## Objective 🔍
The objective of this tutorial is to show how to setup a Grafana dashboard that plots time-series data retrieved from an SQLite database, using podman containers.

## Description 📖
If you have a WebPanel with [codesys](https://www.codesys.com/), or some other software that stores time-series data gathered from different input devices inside an SQLite database, and you need to visualize it, this tutorial will guide you throughout every step. As a bonus, this tutorial comes with a custom Python podman image used to create and periodically write an SQLite database with random data.

## Prerequisites 🛠️
- A [WebPanel (WP)](https://www.pixsys.net/en/hmi-panel-pc/web-panel) or [TouchController (TC)](https://www.pixsys.net/en/programmable-devices/hmi-codesys) device
- Basic knowledge of [Grafana](https://grafana.com/)
- Basic knowledge of [SQLite](https://sqlite.org/)
- Basic knowledge of [podman](https://podman.io/) and containers
- Basic knowledge of Linux

## **Steps** 👣
1. Connect to the device via SSH using the **`user`** account:
   
   ```bash
   ssh user@<DEVICE_IP>
   ```
2. Navigate to the persistent folder `/data/user`:
   
   ```bash
   cd /data/user
   ```

3. Create a dedicated folder for the tutorial:
    ```bash
    mkdir grafana-sqlite-visualization-stack
    cd grafana-sqlite-visualization-stack
    ```

4. Create a dedicated folder to have persisent storage for Grafana, and a podman `folder` to keep your configuration files:
    ```bash
    mkdir grafana-data
    mkdir podman
    ```
5. Run the container:

    - If you only need the Grafana container and you already have a working SQLite database, just run:
    
        ```bash
        podman run --userns=keep-id -u $(id -u):$(id -g) -v $(pwd)/grafana-data:/var/lib/grafana -v <SQLITE_FILE_FOLDER>:/db -p 3000:3000 -e GF_PLUGINS_PREINSTALL="frser-sqlite-datasource" grafana/grafana-enterprise:12.0.1
        ```

        **Note: use `--userns=keep-id` to make sure that `user` (your current user) is correctly mapped as container user so that there aren't any RXW permissions. Then, use -u `$(id -u):$(id -g)` to actually use your mapped user as container user**

    - If you need both Grafana and an SQLite database, along with the Python container for simulating data, you will use `podman-compose`. First, you need to create an additional folder to store the SQLite database:
        ```bash
        mkdir sqlite-data
        ```
        At this point, you can run:
        ```bash
        MY_UID=$(id -u) MY_GID=$(id -g) ROOT_DIR=$(pwd) podman-compose -f docker/grafana-sqlite-stack.yml up --build
        ```

        **Note: in this case, the --userns and the user mapping are performed internally in the podman-compose.yml, and you just need to pass your UID and the GID**

        **Note 2: make sure your container has access to internet so that grafana can download its plugins. This is not trivial since some firewall rules for Docker/Podman must be set. For the sake of ease and for development usage, add --network=host to the command above**

6. Access the Grafana dashboard navigating to `localhost:3000` if you are physically interacting with your target device, or navigate to `<DEVICE_IP>:3000` if you have remote access to your target device. You should see the default login page of Grafana.

7. Access using:
    - user: admin
    - password: admin

    then you can optionally modify the default password (suggested).
    ![Login](assets/login.png)

8. In order to plot data from the SQLite database, you first need to configure the [data-source for SQLite](https://grafana.com/docs/grafana/latest/datasources/). Go to Home->Connections->Data sources->Add data source, look for SQLite (the plugin installed using *GF_PLUGINS_PREINSTALL*), select it and use */db/sample.db* as path for the database file. You can leave the rest of the configuration as it is, then press "Save and test".
    ![Add data source](assets/add_data_source.png)

9. Go to Home->Dashboards and create a new dashboard. Select the previous configured data-source as data source of the dashboard and create the dashboard
 ![Add dashboard](assets/add_dashboard.png)

    Then, scroll down to the query input file and write:
    ```mysql
    SELECT timestamp as ts, value
    FROM table_sample
    ```
    save the query (or click outside the input text of the query) and you should see a plot of the default panel. 
    ![Plot data](assets/dashboard_panel.png)

<img src="assets/pixsys-logo.png" alt="PixsysLogo" width="50%">