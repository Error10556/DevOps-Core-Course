FROM python:3.13-alpine
RUN adduser -D -H -h /app -u 2000 infoservice infoservice
RUN mkdir /app /venv /data
RUN chown infoservice:infoservice /venv /app /data
WORKDIR /app
COPY docker-entrypoint.sh /
RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"
ENV VIRTUAL_ENV="/venv"

COPY --chown=infoservice:infoservice requirements.txt .
RUN pip install -r requirements.txt

COPY --chown=infoservice:infoservice app.py .
EXPOSE 5000
ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["-b", "0.0.0.0:5000", "-e", "DEBUG=true", "app:app"]
