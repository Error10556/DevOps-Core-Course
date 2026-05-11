FROM python:3.13-alpine
RUN addgroup -S infoservice
RUN adduser -S infoservice
RUN mkdir /app /venv
RUN chown infoservice:infoservice /venv /app
WORKDIR /app
USER infoservice
RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"
ENV VIRTUAL_ENV="/venv"

COPY --chown=infoservice:infoservice requirements.txt .
RUN pip install -r requirements.txt

COPY --chown=infoservice:infoservice app.py .
EXPOSE 5000
ENTRYPOINT ["gunicorn"]
CMD ["-b", "0.0.0.0:5000", "-e", "DEBUG=true", "app:app"]
