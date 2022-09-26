FROM dockercodata.pb.gov.br/ci-base-images/python:3.10

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN DATABASE_URL=sqlite:///db.sqlite \
    SSO_CLIENT_ID='' \
    SSO_CLIENT_SECRET='' \
    python manage.py collectstatic --noinput

CMD ["gunicorn", "config.wsgi", "--bind=8080"]