#!/bin/bash

echo "Initializing environment..."

docker run -ti --rm --entrypoint "/bin/bash" -u root -v "${PWD}:/mnt" \
       grafana/grafana:latest \
       /mnt/initialize_grafana.sh

docker run -ti --rm --entrypoint "/bin/bash" -u root -v "${PWD}:/mnt" \
       docker.elastic.co/elasticsearch/elasticsearch-oss:7.2.0 \
       /mnt/initialize_elasticsearch.sh

echo "Complete"
echo "To launch enter:"
echo "  docker-compose up -d"


