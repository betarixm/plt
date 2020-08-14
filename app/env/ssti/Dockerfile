FROM python:3.7

LABEL Name="PLT - PLUS Laboratory for Training - for SSTI"
LABEL Version="0.1"
LABEL Maintainer="ysw1109@postech.ac.kr"

ENV PYTHONUNBUFFERED 1
RUN mkdir /app
WORKDIR /app
RUN pip install --no-cache-dir flask
COPY app.py /app/

ENTRYPOINT ["python", "app.py"]
