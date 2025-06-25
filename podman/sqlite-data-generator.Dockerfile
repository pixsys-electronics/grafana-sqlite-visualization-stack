FROM docker.io/python:3.10-slim

WORKDIR /workspace

COPY write_sample.py .

CMD [ "python" ,"./write_sample.py"]