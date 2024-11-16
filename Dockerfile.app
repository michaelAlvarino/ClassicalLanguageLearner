FROM python:3


WORKDIR /code


COPY ./requirements.txt /code/requirements.txt


RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt


COPY ./ClassicalLanguageLearner /code/ClassicalLanguageLearner

COPY logging.conf /code/logging.conf


CMD ["fastapi", "run", "ClassicalLanguageLearner/main.py", "--port", "80"]