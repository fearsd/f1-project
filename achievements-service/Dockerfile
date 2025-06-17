FROM python:3.13-alpine

WORKDIR /code

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY app/ app/
# COPY main.py .

CMD ["python", "app/main.py"]