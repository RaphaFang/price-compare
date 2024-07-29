FROM python:3.9

WORKDIR /usr/src/app

COPY . .

RUN pip install --no-cache-dir 'requests<2.29.0' 'urllib3<2.0' -r requirements.txt

EXPOSE 8002

CMD ["hypercorn", "project.asgi:app", "--bind", "0.0.0.0:8002"]
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8002"]
# CMD [ "uvicorn", "project.asgi:app", "python", "manage.py", "runserver", "0.0.0.0:8002"]

# ARG DJANGO_SECRET_KEY
# ENV DJANGO_SECRET_KEY=${DJANGO_SECRET_KEY}
# RUN python manage.py collectstatic --noinput