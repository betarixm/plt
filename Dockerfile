FROM python:3.7

LABEL Name="PLT - PLUS Laboratory for Training"
LABEL Version="0.1"
LABEL Maintainer="mzg00@postech.ac.kr"

ENV PYTHONUNBUFFERED 1
RUN mkdir /app
WORKDIR /app
ADD requirements.txt /app/
RUN pip install -r requirements.txt
ADD app/ /app/
RUN python manage.py collectstatic
ENTRYPOINT ["python", "manage.py", "runserver", "0.0.0.0:8000"]