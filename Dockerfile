FROM python:3.9

WORKDIR /usr/src/app

RUN pip install django djangorestframework

COPY . .

EXPOSE 8002

CMD ["python", "manage.py", "runserver", "0.0.0.0:8002"]