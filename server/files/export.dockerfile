FROM python:3.12-alpine

COPY export_server.py /app/export_server.py

EXPOSE 5000

CMD ["python", "/app/export_server.py"]