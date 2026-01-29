Post compose up:
----------
Validation
----------
  Step-1
----------
docker exec kafka-1 kafka-topics.sh \
  --bootstrap-server 10.1.40.26:9092 \
  --create \
  --topic stable-test \
  --partitions 1 \
  --replication-factor 1


----------
  Step-2
----------
docker exec kafka-1 kafka-topics.sh \
  --bootstrap-server 10.1.40.26:9092 \
  --list

----------
  Step-3
----------
docker compose down
docker compose up -d

----------
  Step-4
----------
docker exec kafka-1 kafka-topics.sh \
  --bootstrap-server 10.1.40.26:9092 \
  --list

