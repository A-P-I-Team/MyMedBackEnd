FROM python:3.9-alpine

ENV  PYTHONDONTWRITEBYTECODE 1
ENV  PYTHONUNBUFFERED 1 
ENV  DJANGO_SUPERUSER_PASSWORD Ab654321

RUN mkdir /app
WORKDIR /app






RUN apk update
RUN apk add jpeg-dev zlib-dev libjpeg 
RUN apk add --no-cache --virtual .build-deps build-base linux-headers python3-tkinter
RUN apk add --no-cache gcc python3-dev musl-dev mariadb-dev
RUN pip install --upgrade pip


#ADDED
RUN pip install -U setuptools


RUN pip install gunicorn mysqlclient


#ADDED 
RUN pip install -U pip setuptools wheel ruamel.yaml.clib==0.2.6


RUN apk del gcc python3-dev musl-dev

# while ! python3 manage.py sqlflush > /dev/null 2>&1 ; do sleep 1 ; done

CMD pip install -r requirements.txt && \
    sleep 60 && \
    python3 manage.py makemigrations --noinput && \
    python3 manage.py migrate --noinput && \
    python3 manage.py collectstatic --noinput && \
    if echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser(username='admin@admin.com', password = 'Ab654321')" | python manage.py shell >/dev/null 2>&1 ; then echo "superuser created"; else echo "super user existed" ; fi && \
    celery -A MyMed worker --loglevel=INFO --detach && \
    sleep 2 && \
    gunicorn -b 0.0.0.0:8000 MyMed.wsgi --daemon && \
    sleep 2 && \
    celery -A MyMed flower --loglevel=INFO --detach
    

