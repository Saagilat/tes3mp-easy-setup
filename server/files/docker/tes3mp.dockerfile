FROM debian:11-slim

RUN apt-get update && apt-get install -y \
    libluajit-5.1-2 \
    libcurl4 \
    libssl1.1 \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

COPY data/ /tes3mp/
WORKDIR /tes3mp
EXPOSE 25565/tcp
EXPOSE 25565/udp
CMD ["./tes3mp-server"]