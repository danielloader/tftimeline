FROM python:3.8-slim
COPY requirements.txt /requirements.txt
RUN pip install -U pip
RUN pip install -r /requirements.txt 
COPY tftimeline /app/tftimeline
WORKDIR /app

ENTRYPOINT ["python", "-m", "tftimeline"]