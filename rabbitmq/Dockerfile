FROM ubuntu:22.04 
LABEL image.authors="Vic Fernandez III <@cyberphor>"
ENV DEBIAN_FRONTEND=noninteractive
RUN apt update -y &&\
    apt install -y \
    erlang-base \
    erlang-asn1 erlang-crypto erlang-eldap erlang-ftp erlang-inets \
    erlang-mnesia erlang-os-mon erlang-parsetools erlang-public-key \
    erlang-runtime-tools erlang-snmp erlang-ssl \
    erlang-syntax-tools erlang-tftp erlang-tools erlang-xmerl\
    rabbitmq-server &&\
    rabbitmq-plugins enable rabbitmq_management
WORKDIR /home/hades/
COPY rabbitmq.conf /etc/rabbitmq/
USER rabbitmq
EXPOSE 5672 15672
CMD [ "rabbitmq-server" ]
