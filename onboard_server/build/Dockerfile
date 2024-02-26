FROM ubuntu:20.04

# install utilities & ansible
RUN apt-get update -y \
    && apt-get install -y \
    vim \
    ssh \
    curl \
    wget \
    unzip

ENV PYTHONUNBUFFERED=1
RUN apt-get update 					\
    && apt-get install -y software-properties-common 	\
    && add-apt-repository -y ppa:deadsnakes/ppa 	\
    && apt-get update  					\
    && apt install -y python3.11			\
    && rm /usr/bin/python3				\
    && ln -s /usr/bin/python3.11 /usr/bin/python3

RUN apt-get update 								\
    && apt-get install -y python3-dev python3-setuptools python3.11-distutils	\
    && python3 -m easy_install install pip

RUN curl -LO https://github.com/stedolan/jq/releases/download/jq-1.7.1/jq-linux64 \
  && chmod a+x jq-linux64 \
  && mv jq-linux64 /usr/local/bin/jq

RUN pip3 install fastapi uvicorn[standard]

# Cleanup
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

WORKDIR /home/demo
