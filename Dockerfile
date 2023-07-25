FROM python:3.8.5
LABEL Name=mgahawa Version=1.0
FROM python:3

RUN mkdir /mgahawa
WORKDIR /mgahawa
ADD requirements.txt /mgahawa/
RUN pip install -r requirements.txt
EXPOSE 8003

