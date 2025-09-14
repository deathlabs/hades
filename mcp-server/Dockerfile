FROM alpine:3.22 AS stage_1
LABEL image.authors="Vic Fernandez III <@cyberphor>"
WORKDIR /home/hades/
COPY hades/ hades/
COPY entrypoint.sh entrypoint.sh
COPY requirements.txt requirements.txt
RUN apk add --no-cache --update python3 py3-pip &&\
    pip install --break-system-packages -r requirements.txt &&\
    adduser -D hades -h /home/hades &&\
    chown -R hades:hades /home/hades &&\
    chmod +x entrypoint.sh
USER hades
CMD [ "./entrypoint.sh" ]
