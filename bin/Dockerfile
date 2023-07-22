FROM python:3.9-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn
COPY . /app/
EXPOSE 5000
CMD ["gunicorn", "-b", "0.0.0.0:5000", "run:app"]