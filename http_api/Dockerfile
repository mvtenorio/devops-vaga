FROM python:3.7

WORKDIR /usr/src/app

RUN pip install pipenv

COPY Pipfile .
COPY Pipfile.lock .

RUN pipenv install

CMD ["pipenv", "run", "flask", "run", "--host=0.0.0.0"]
