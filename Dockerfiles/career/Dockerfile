FROM python:3.6.6-stretch
ENV PYTHONUNBUFFERED=1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
#RUN apt-get update -y && \
#    apt-get install -y openssl
RUN pip install --upgrade pip && pip install --trusted-host pypi.org --trusted-host files.pythonhosted.orG -r requirements.txt
