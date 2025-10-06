FROM debian:13.1 AS stage_1
LABEL maintainer="Vic Fernandez III <@cyberphor>"
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1
WORKDIR /home/
COPY requirements.txt requirements.txt
COPY mistral-7b-instruct-v0.2.Q6_K.gguf mistral-7b-instruct-v0.2.Q6_K.gguf
RUN apt update -y && \
    apt install -y python3 python3-pip git wget &&\
    pip install -r requirements.txt --break-system-packages
COPY hades hades
EXPOSE 9999
CMD [ "uvicorn", "hades.main:api", "--host", "0.0.0.0", "--port", "9999" ]
