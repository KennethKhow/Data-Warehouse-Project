FROM python:3.10.4-slim

COPY install.sh requirements.txt /tmp/

RUN bash /tmp/install.sh && rm /tmp/install.sh

RUN python -m venv /app/venv && \
    /app/venv/bin/pip install --no-cache-dir -r /tmp/requirements.txt

WORKDIR /app/etl

COPY /etl/*.py .

ENV ORCLUID=OT ORCLPWD=1234 MDBUID=root MDBPWD=1234

# Oracle Instant Client connection string: sqlplus kk/kk@\"//192.168.22.143:1521/XE\" 