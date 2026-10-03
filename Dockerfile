FROM python:3.12-slim
WORKDIR /app
COPY relay.py .
ENV PYTHONUNBUFFERED=1 RELAY_PORT=9000
EXPOSE 9000
CMD ["python", "relay.py"]
