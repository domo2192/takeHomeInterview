FROM python:3.11-alpine

RUN apk add --no-cache openssh-client

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

COPY ssh_keys/ ./ssh_keys/

RUN chmod 600 ./ssh_keys/id_rsa
RUN chmod 644 ./ssh_keys/id_rsa.pub

RUN mkdir -p /app/logs

EXPOSE 5000

CMD ["python", "app.py"]