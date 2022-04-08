FROM python:3
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
RUN pip install docker
EXPOSE 9900
CMD python deployer.py
