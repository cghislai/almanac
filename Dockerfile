FROM ubuntu:latest

RUN apt-get update \
 && apt-get install -y \
        python3-pip \
        git \
 && apt-get -y clean \
 && rm -rf /var/lib/apt \
 && cd /tmp \
 && git clone https://github.com/cghislai/almanac.git \
 && cd almanac \
 && pip3 install flask skyfield \
 && pip3 install . \
 && cd / \
 && rm -rf /tmp/almanac


CMD almanac-server -H 0.0.0.0
