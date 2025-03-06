FROM dockercodata.pb.gov.br/ci-base-images/python:3.13

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Variáveis de ambiente temporárias para executar o `python manage.py collectstatic`
RUN SECRET_KEY='' \
    DATABASE_HOST='' \
    DATABASE_PORT='' \
    DATABASE_NAME='' \
    DATABASE_USERNAME='' \
    DATABASE_PASSWORD='' \
    SSO_CLIENT_SECRET='' \
    python manage.py collectstatic --noinput

COPY --chmod=755 docker-entrypoint.sh /docker-entrypoint.sh

ENV DJANGO_RUN_MIGRATE=1
CMD ["/docker-entrypoint.sh"]