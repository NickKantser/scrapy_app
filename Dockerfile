FROM python:3.10

WORKDIR /sreality

COPY . .

RUN pip install -r requirements.txt

CMD ["python", "./sreality_flats/flats.py"]
