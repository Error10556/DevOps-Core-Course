FROM python:3.13-alpine
RUN mkdir /app
WORKDIR /app
RUN adduser -S infoservice
USER infoservice

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app.py .
EXPOSE 5000
ENTRYPOINT ["gunicorn"]
CMD ["-b", "0.0.0.0:5000", "-e", "DEBUG=true", "app:app"]
