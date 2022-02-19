FROM python:3.9

RUN apt-get update -y
RUN apt-get upgrade -y

WORKDIR /app

COPY ./requirements.txt ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY ./Lunchtime ./Lunchtime
ENV TZ Europe/Helsinki

EXPOSE 8000

CMD [ "python3", "./Lunchtime/manage.py", "runserver", "0.0.0.0:8000"]