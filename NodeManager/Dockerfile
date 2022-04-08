FROM python:3
RUN  apt-get update

RUN apt install sshpass

RUN apt install zip

WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
EXPOSE 9500
CMD python NodeManager.py