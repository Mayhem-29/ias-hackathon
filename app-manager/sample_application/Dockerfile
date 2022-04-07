FROM python:3

WORKDIR /app

COPY . /app

RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 2001

CMD ["python" ,"run.py", "2001"]
