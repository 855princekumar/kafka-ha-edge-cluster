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
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# 🔑 Use Apache ARCHIVE + safe tar flags (Pi overlayfs compatible)
RUN curl -fL https://archive.apache.org/dist/kafka/${KAFKA_VERSION}/kafka_${SCALA_VERSION}-${KAFKA_VERSION}.tgz \
    | tar -xz \
        --no-same-owner \
        --no-same-permissions && \
    mv kafka_${SCALA_VERSION}-${KAFKA_VERSION} kafka

COPY start-zookeeper.sh /start-zookeeper.sh
RUN chmod +x /start-zookeeper.sh

VOLUME ["/var/lib/zookeeper"]

EXPOSE 2181 2888 3888

CMD ["sh", "/start-zookeeper.sh"]

