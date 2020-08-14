FROM whysw/selenium-headless-chrome:1.0

LABEL Name="PLT - PLUS Laboratory for Training"
LABEL Version="0.1"
LABEL Maintainer="mzg00@postech.ac.kr"

ENV PYTHONUNBUFFERED 1
RUN mkdir /app
WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
COPY app/ /app/
RUN python manage.py collectstatic --noinput

ENTRYPOINT ["python", "manage.py", "runserver", "0.0.0.0:8000"]
