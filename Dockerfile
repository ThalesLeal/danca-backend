FROM dockercodata.pb.gov.br/ci-base-images/python:3.11

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN SECRET_KEY="secret" \
    DATABASE_URL=sqlite:///db.sqlite \
    SSO_CLIENT_ID='' \
    SSO_CLIENT_SECRET='' \
    python manage.py collectstatic --noinput

CMD ["gunicorn", "config.wsgi", "--bind=0.0.0.0:8080"]
