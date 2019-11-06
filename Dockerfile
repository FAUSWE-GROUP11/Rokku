FROM ubuntu:xenial

ENV LANG C.UTF-8

RUN apt-get update && apt-get install --no-install-recommends -y \
    software-properties-common \
    python-software-properties \
    && add-apt-repository ppa:jonathonf/python-3.6

RUN apt-get update && apt-get install --no-install-recommends -y \
    gir1.2-gtk-3.0 \
    python3.6 \
    python3-gi \
    python3-gi-cairo \
    python3-pytest \
    xauth \
    xvfb

