FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install -r  \
    requirements.txt \
    --no-cache

COPY . .

RUN python manage.py collectstatic --no-input --clear

# The command to run is specified by docker-compose for both the production
# server and the test service. This allows using the same image in different
# contexts.
