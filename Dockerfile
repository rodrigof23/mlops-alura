FROM python:3.7-slim

ARG BASIC_AUTH_USERNAME_ARG
ARG BASIC_AUTH_PASSWROD_ARG

ENV BASIC_AUTH_USERNAME=$BASIC_AUTH_USERNAME_ARG
ENV BASIC_AUTH_PASSWROD=$BASIC_AUTH_PASSWROD_ARG

WORKDIR /usr

COPY ./requirements.txt /usr/requirements.txt
RUN pip3 install -r requirements.txt

COPY ./src /usr/src
COPY ./models /usr/models

ENTRYPOINT ["python3"]

CMD ["src/app/main.py"]
