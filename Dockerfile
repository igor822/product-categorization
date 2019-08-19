FROM felixleung/auto-sklearn

COPY . /app
WORKDIR /app

RUN pip install --upgrade pip
RUN make requirements

CMD ["make", "serve"]
