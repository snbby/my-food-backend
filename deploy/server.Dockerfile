FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install -r  \
    requirements.txt \
    --no-cache

COPY . .

RUN python manage.py collectstatic --no-input --clear

CMD [ \
  "gunicorn", "myfood.wsgi:application", \
  "--name", "myfood", \
  "--bind", "0.0.0.0:8000", \
  "--log-level", "info", \
  "--log-file", "-" \
]