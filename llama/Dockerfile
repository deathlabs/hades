FROM debian:13.1 AS stage_1
LABEL maintainer="Vic Fernandez III <@cyberphor>"
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1
RUN apt update -y && \
    apt install -y python3 python3-pip git wget &&\
    pip install --upgrade pip && \
    pip install -r requirements.txt &&\
    wget https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF/resolve/main/mistral-7b-instruct-v0.2.Q6_K.gguf
WORKDIR /home/hades/
COPY main.py main.py
EXPOSE 9999
CMD [ "uvicorn", "main:api", "--host", "0.0.0.0", "--port", "9999" ]
