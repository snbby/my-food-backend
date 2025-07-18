FROM python:3.13-slim
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install --upgrade pip && pip3 install -r requirements.txt --no-cache
COPY app.py app.py
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8001"]
