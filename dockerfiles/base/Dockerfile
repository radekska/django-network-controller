FROM python:slim

WORKDIR /network-controller-app

COPY . ./

RUN apt-get update && apt-get install -y \
        tzdata \
        python3-setuptools \
        python3-pip \
        python3-dev \
        libsnmp-dev \
        && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install -r requirements.txt