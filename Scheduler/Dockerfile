FROM python:3
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
EXPOSE 9600
CMD python Scheduler.py