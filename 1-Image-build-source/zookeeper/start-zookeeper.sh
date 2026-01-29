#!/bin/sh
set -e

ZOOKEEPER_DATA_DIR=${ZOOKEEPER_DATA_DIR:-/var/lib/zookeeper}
ZOOKEEPER_CLIENT_PORT=${ZOOKEEPER_CLIENT_PORT:-2181}
ZOOKEEPER_TICK_TIME=${ZOOKEEPER_TICK_TIME:-2000}

mkdir -p "$ZOOKEEPER_DATA_DIR"

cat > $KAFKA_HOME/config/zookeeper.properties <<EOF
tickTime=$ZOOKEEPER_TICK_TIME
dataDir=$ZOOKEEPER_DATA_DIR
clientPort=$ZOOKEEPER_CLIENT_PORT
initLimit=5
syncLimit=2
EOF

exec $KAFKA_HOME/bin/zookeeper-server-start.sh \
     $KAFKA_HOME/config/zookeeper.properties

