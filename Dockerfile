FROM ubuntu:latest

RUN apt-get update \
 && apt-get install -y \
        python3-pip \
 && apt-get -y clean \
 && rm -rf /var/lib/apt

# Provide default data file
COPY data/ /tmp/skyfield-data/
COPY almanac /tmp/almanac/almanac
COPY setup.py /tmp/almanac/

RUN cd /tmp/almanac \
 && pip3 install flask skyfield \
 && pip3 install . \
 && cd / \
 && rm -rf /tmp/almanac \
 && mkdir -p /tmp/skyfield-data \
 && useradd -m almanac \
 && chown -R almanac /tmp/skyfield-data

USER almanac

CMD almanac-server -H 0.0.0.0
