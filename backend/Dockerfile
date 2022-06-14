FROM python:3.9 as build-stage
RUN apt-get update

WORKDIR /app
COPY ./ .

RUN python3 -m pip install -r requirements.txt

ENTRYPOINT [ "python3" ]
CMD ["app.py" ]