# Dockerfile metadata for first build.
FROM ubuntu:22.04 AS first-build
LABEL image.authors="Victor Fernandez III, @cyberphor"
ENV DEBIAN_FRONTEND=noninteractive

# Install RabbitMQ and its dependencies.
RUN apt update -y &&\
    apt install -y \
    erlang-base \
    erlang-asn1 erlang-crypto erlang-eldap erlang-ftp erlang-inets \
    erlang-mnesia erlang-os-mon erlang-parsetools erlang-public-key \
    erlang-runtime-tools erlang-snmp erlang-ssl \
    erlang-syntax-tools erlang-tftp erlang-tools erlang-xmerl\
    rabbitmq-server

# Delete me.
RUN rabbitmq-plugins enable rabbitmq_management

# Set the working directory.
WORKDIR /
COPY rabbitmq.conf /etc/rabbitmq/

# Start RabbitMQ.
USER rabbitmq
EXPOSE 5672 15672
CMD [ "rabbitmq-server" ]
