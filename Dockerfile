# syntax=docker/dockerfile:1
FROM python:3.10-alpine
WORKDIR /app
COPY . /app
ENV FLASK_APP run.py
ENV FLASK_RUN_HOST=0.0.0.0
RUN apk add --no-cache gcc musl-dev linux-headers
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 5000
COPY . .
CMD ["flask", "run", "--debug"]