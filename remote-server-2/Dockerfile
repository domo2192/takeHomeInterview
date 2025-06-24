FROM python:3.11-alpine

WORKDIR /app

# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

COPY file_server.py .

RUN mkdir -p /app/files /app/logs

COPY sample_files/ /app/files/

EXPOSE 8080

CMD ["python", "file_server.py"]