# Python 3.8.0

FROM python:3

# author of file
LABEL maintainer="Zhiyuan (Andrew) Wang <wangzyzju@gmail.com>"

# Packages that we need
WORKDIR /usr/src/app
COPY requirements.txt ./
COPY requirements ./requirements

# instruction to be run during image build
RUN pip install -r requirements.txt

# Copy all the files from current source duirectory(from your system) to
# Docker container in /usr/src/app directory
COPY funwithflags/. ./funwithflags
COPY tests/. ./tests

# Command to startup the container
CMD ["pytest"]
