FROM debian:stretch

ENV LANG C.UTF-8

RUN apt-get update && apt-get install --no-install-recommends -y \
    gir1.2-gtk-3.0 \
    libcairo2-dev \
    libgirepository1.0-dev \
    xauth \
    xvfb \
    python3 \
    python3-dev \
    python3-pip

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

RUN python3 -m pip install --upgrade pip setuptools \
    && python3 -m pip install -r requirements.txt    

