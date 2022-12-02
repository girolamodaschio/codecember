FROM python:3.10.4-slim-buster

RUN pip install --upgrade pip

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY main.py main.py
EXPOSE 9090

ENTRYPOINT ["python"]
CMD ["main.py"]