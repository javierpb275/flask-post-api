FROM alpine:3.10

RUN apk add --no-cache python3-dev \
    && pip3 install --upgrade pip

WORKDIR /app 

COPY . /app

RUN \
 apk add --no-cache python3 postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc python3-dev musl-dev postgresql-dev && \
 pip3 --no-cache-dir install -r requirements.txt && \
 apk --purge del .build-deps

CMD [ "python3", "src/app.py" ]