FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY ./requirements.txt .

# install nltk
RUN pip3 install -U nltk numpy
RUN pip3 install rake-nltk

RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["gunicorn","-k","uvicorn.workers.UvicornWorker", "src.app.main:app", "-b", "0.0.0.0:8000" ]