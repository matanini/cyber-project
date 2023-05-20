FROM python:3.10

WORKDIR /usr/src/backend

COPY ./requirements.txt ./requirements.txt

RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app","--reload", "--host", "0.0.0.0", "--port", "8001"]