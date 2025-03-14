FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install -r  \
    requirements.txt \
    --no-cache

COPY . .


CMD ["python", "manage.py", "server_health"]