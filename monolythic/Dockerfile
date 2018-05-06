FROM python:3.6-alpine3.7

LABEL name=ms version=dev

WORKDIR /app

COPY *requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app
RUN pip install -e .

CMD ["gunicorn", "-b", ":80", "--workers=1", "app:app"]

EXPOSE 80
LABEL name=ms version=dev
