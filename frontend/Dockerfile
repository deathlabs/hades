FROM alpine:3.22 AS stage_1
ARG NODE_VERSION=v24.8.0
ENV NODE_VERSION=${NODE_VERSION}
SHELL [ "/bin/ash", "-eo", "pipefail", "-c" ]
WORKDIR /home/hades/
COPY hades/ .
RUN apk add --no-cache curl libstdc++ &&\
    curl -fsSLO --compressed "https://unofficial-builds.nodejs.org/download/release/$NODE_VERSION/node-$NODE_VERSION-linux-x64-musl.tar.xz" &&\
    tar -xJf "node-$NODE_VERSION-linux-x64-musl.tar.xz" --strip-components=1 --no-same-owner -C /usr/local &&\
    npm install &&\
    npm run build &&\
    mv "$(find dist/assets/index-*.js | head -n 1)" dist/assets/index.js &&\
    mv "$(find dist/assets/logo-*.png | head -n 1)" dist/assets/logo.png

FROM alpine:3.22 AS stage_2
ARG GO_VERSION=1.25.1
ENV GO_VERSION=${GO_VERSION}
WORKDIR /home/
COPY --from=stage_1 /home/hades/ hades/
COPY go.mod go.mod
COPY main.go main.go
RUN apk add --no-cache curl gcompat &&\
    curl -fsSLO "https://go.dev/dl/go$GO_VERSION.linux-amd64.tar.gz" &&\
    tar -xzf "go$GO_VERSION.linux-amd64.tar.gz" -C /usr/local &&\
    export PATH=$PATH:/usr/local/go/bin &&\
    go build -ldflags="-s -w" -o server

FROM scratch AS stage_3
LABEL image.authors="Vic Fernandez III <@cyberphor>"
COPY --from=stage_2 /home/server server
ENTRYPOINT [ "./server" ]
