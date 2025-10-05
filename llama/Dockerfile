FROM debian:13.1 AS stage_1
LABEL maintainer="Vic Fernandez III <@cyberphor>"
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1
WORKDIR /home/
COPY requirements.txt requirements.txt
RUN apt update -y && \
    apt install -y python3 python3-pip git wget &&\
    pip install -r requirements.txt --break-system-packages &&\
    wget https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF/resolve/main/mistral-7b-instruct-v0.2.Q6_K.gguf
COPY hades hades
EXPOSE 9999
CMD [ "uvicorn", "hades.main:api", "--host", "0.0.0.0", "--port", "9999" ]
