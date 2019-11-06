FROM debian:stretch

ENV LANG C.UTF-8

RUN apt-get update && apt-get install --no-install-recommends -y \
    gir1.2-gtk-3.0 \
    libcairo2-dev \
    libgirepository1.0-dev \
    xauth \
    xvfb