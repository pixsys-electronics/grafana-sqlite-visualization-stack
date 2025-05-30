# Use Node-RED as base
FROM nodered/node-red:latest

# Maintainer information
LABEL maintainer="YourName <youremail@example.com>"

# Install additional modules: Dashboard and Modbus
RUN npm install node-red-node-serialport node-red-dashboard node-red-contrib-modbus node-red-contrib-modbus-flex-server --unsafe-perm && \
    npm cache clean --force

# Expose port 1880 for Node-RED access
EXPOSE 1880

WORKDIR /data

# Default command to start Node-RED
CMD ["npm", "start", "--", "--userDir", "/data"]