FROM python:3.8-alpine

RUN mkdir /app

COPY . /app

WORKDIR /app

RUN pip install -r    requirements.txt                                                                            

EXPOSE 2000

ENTRYPOINT  ["python3"]

CMD ["run.py", "2000"]
