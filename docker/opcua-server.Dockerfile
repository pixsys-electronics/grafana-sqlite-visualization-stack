FROM python:3.7-slim

WORKDIR /opt/opc_mockup/datagenerator

COPY opcua-server.py requirements.txt /opt/opc_mockup/datagenerator/

RUN pip install -r requirements.txt

CMD [ "python" ,"./opcua-server.py"]