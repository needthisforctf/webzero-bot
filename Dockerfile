FROM python:3

RUN apt-get update && apt-get install -y curl
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "./bot.py"]