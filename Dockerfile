FROM python:3.9.5

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

RUN pip uninstall decouple -y

COPY ./app /code/app

COPY ./.env /code/ 

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]