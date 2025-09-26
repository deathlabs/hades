FROM alpine:3.22 AS stage_1
LABEL image.authors="Vic Fernandez III <@cyberphor>"
WORKDIR /home/hades/
COPY hades/ hades/
COPY requirements.txt requirements.txt
RUN apk add --no-cache --update python3 py3-pip &&\
    pip install --break-system-packages -r requirements.txt &&\
    adduser -D hades -h /home/hades &&\
    chown -R hades:hades /home/hades
USER hades
CMD [ "python", "-m", "hades.main", "server" ]
