FROM python:3.11.1

ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/venv_caretaxi

COPY requirements.txt .

RUN pip install -r requirements.txt

RUN pip install --upgrade pip

RUN pip install django-import-export

ADD . /usr/src/venv_caretaxi

CMD ["python", "manage.py", "runserver", "0.0.0.0:7000"]
