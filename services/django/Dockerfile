FROM python:3.13-slim
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install --upgrade pip && pip3 install -r requirements.txt --no-cache
COPY . .
RUN python manage.py collectstatic --no-input --clear