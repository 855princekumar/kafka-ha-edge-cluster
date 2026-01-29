#!/bin/sh
set -e

# Required / sensible defaults
KAFKA_BROKER_ID=${KAFKA_BROKER_ID:-1}
KAFKA_ZOOKEEPER_CONNECT=${KAFKA_ZOOKEEPER_CONNECT:-zookeeper:2181}
KAFKA_LISTENERS=${KAFKA_LISTENERS:-PLAINTEXT://0.0.0.0:9092}
KAFKA_ADVERTISED_LISTENERS=${KAFKA_ADVERTISED_LISTENERS:-PLAINTEXT://localhost:9092}
KAFKA_LOG_DIRS=${KAFKA_LOG_DIRS:-/var/lib/kafka}

# HA-related defaults (safe for single-node too)
KAFKA_NUM_PARTITIONS=${KAFKA_NUM_PARTITIONS:-1}
KAFKA_DEFAULT_REPLICATION_FACTOR=${KAFKA_DEFAULT_REPLICATION_FACTOR:-1}
KAFKA_MIN_INSYNC_REPLICAS=${KAFKA_MIN_INSYNC_REPLICAS:-1}

# JVM tuning for Pi
KAFKA_HEAP_OPTS=${KAFKA_HEAP_OPTS:--Xms256m -Xmx512m}

export KAFKA_HEAP_OPTS

mkdir -p "$KAFKA_LOG_DIRS"

cat > $KAFKA_HOME/config/server.properties <<EOF
broker.id=$KAFKA_BROKER_ID
listeners=$KAFKA_LISTENERS
advertised.listeners=$KAFKA_ADVERTISED_LISTENERS

zookeeper.connect=$KAFKA_ZOOKEEPER_CONNECT

log.dirs=$KAFKA_LOG_DIRS

num.partitions=$KAFKA_NUM_PARTITIONS
default.replication.factor=$KAFKA_DEFAULT_REPLICATION_FACTOR
min.insync.replicas=$KAFKA_MIN_INSYNC_REPLICAS

offsets.topic.replication.factor=$KAFKA_DEFAULT_REPLICATION_FACTOR
transaction.state.log.replication.factor=$KAFKA_DEFAULT_REPLICATION_FACTOR
transaction.state.log.min.isr=$KAFKA_MIN_INSYNC_REPLICAS

auto.create.topics.enable=true
EOF

exec $KAFKA_HOME/bin/kafka-server-start.sh \
     $KAFKA_HOME/config/server.properties

