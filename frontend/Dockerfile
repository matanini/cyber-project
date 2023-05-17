FROM python:latest

WORKDIR /usr/src/frontend

COPY ./requirements.txt ./requirements.txt

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

ENTRYPOINT [ "streamlit", "run", "Homepage.py", "--server.port=8000", "--server.address=0.0.0.0", "--server.sslCertFile=./ssl/cert.pem", "--server.sslKeyFile=./ssl/key.pem"]