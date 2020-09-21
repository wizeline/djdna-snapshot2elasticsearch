# pull official base image
FROM python:3.6

# set work directory
WORKDIR /usr/src/app

# install system dependencies
RUN apt-get update && apt-get install -y netcat

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

# copy project
COPY . /usr/src/app/
RUN git clone https://github.com/dowjones/factiva_common.git
RUN git clone https://github.com/miballe/djdna_common

EXPOSE 8050

CMD ["python3", "main.py"]
