FROM python:3
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
EXPOSE 9100
CMD python sensor_manager.py