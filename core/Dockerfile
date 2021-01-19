FROM whysw/selenium-headless-chrome:1.0

LABEL Name="PLT - PLUS Laboratory for Training"
LABEL Version="0.1"
LABEL Maintainer="ysw1109@postech.ac.kr"

ENV PYTHONUNBUFFERED 1
RUN mkdir /app
WORKDIR /app
RUN mkdir static
COPY ./requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
COPY ./ /app/
RUN python manage.py collectstatic --noinput

ENTRYPOINT ["gunicorn", "plt.wsgi", "--worker-class gevent", "--workers=8", "--threads=2", "-b", "0.0.0.0:8000"]
