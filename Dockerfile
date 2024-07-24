FROM python:3.9

WORKDIR /usr/src/app

COPY . .

ARG DJANGO_SECRET_KEY
ENV DJANGO_SECRET_KEY=${DJANGO_SECRET_KEY}

RUN pip install --no-cache-dir 'requests<2.29.0' 'urllib3<2.0' -r requirements.txt

RUN rm -rf /usr/src/app/static/
ARG DJANGO_SECRET_KEY
ENV DJANGO_SECRET_KEY=${DJANGO_SECRET_KEY}
# RUN python manage.py collectstatic --noinput

RUN DJANGO_SECRET_KEY=${DJANGO_SECRET_KEY} python manage.py collectstatic --noinput
# 在想這邊應該可以刪掉原先就的檔案？不然每次斗案都同一個

EXPOSE 8002

# CMD ["python", "manage.py", "runserver", "0.0.0.0:8002"]
# CMD [ "uvicorn", "project.asgi:app", "python", "manage.py", "runserver", "0.0.0.0:8002"]
CMD ["hypercorn", "project.asgi:app", "--bind", "0.0.0.0:8002"]
