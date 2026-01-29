FROM eclipse-temurin:17-jre

ARG KAFKA_VERSION=3.7.0
ARG SCALA_VERSION=2.13

ENV KAFKA_HOME=/opt/kafka
ENV PATH=$PATH:$KAFKA_HOME/bin

WORKDIR /opt

# Minimal tools (Pi-friendly)
RUN apt-get update --allow-releaseinfo-change && \
    apt-get install -y --no-install-recommends \
        curl \
        bash \
        ca-certificates \
        netcat-openbsd && \
    rm -rf /var/lib/apt/lists/*

# 🔑 Apache ARCHIVE + overlayfs-safe extraction
RUN curl -fL https://archive.apache.org/dist/kafka/${KAFKA_VERSION}/kafka_${SCALA_VERSION}-${KAFKA_VERSION}.tgz \
    | tar -xz \
        --no-same-owner \
        --no-same-permissions && \
    mv kafka_${SCALA_VERSION}-${KAFKA_VERSION} kafka

COPY start-kafka.sh /start-kafka.sh
RUN chmod +x /start-kafka.sh

VOLUME ["/var/lib/kafka"]

EXPOSE 9092

CMD ["sh", "/start-kafka.sh"]

