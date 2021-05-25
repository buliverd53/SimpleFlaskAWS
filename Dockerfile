FROM python:3.7

WORKDIR /opt/

ADD ./app /opt/

RUN pip install -r requirements.txt

CMD ["gunicorn", "-b", "0.0.0.0:8000", "--log-level", "debug", "api:app"]