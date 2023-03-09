FROM python:3.10

WORKDIR /django

COPY ./requirements.txt /django/

RUN pip install --no-cache-dir --upgrade -r /django/requirements.txt

COPY . /django/

# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1

# DEV
# ENTRYPOINT [ "python3", "/django/manage.py", "runserver", "0.0.0.0:8010" ]
# PROD
# CMD ["gunicorn", "--bind", "0.0.0.0:8010", "--workers", "3", "w24ok2.wsgi:application"]
# CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "2", "w24ok2.wsgi:application"]
CMD ["uvicorn", "w24ok2.asgi:application", "--host", "0.0.0.0", "--port", "8000" ]

# Test
# CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]