#!/bin/bash

docker run -ti --rm -v ${PWD}/src:/usr/src/app \
       -e "DOCKER_HOST=$(ip -4 addr show docker0 | grep -Po 'inet \K[\d.]+')" \
       espython /bin/bash
