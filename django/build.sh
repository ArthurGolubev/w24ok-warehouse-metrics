#!/bin/bash
docker buildx build --push \
--platform linux/amd64 \
--tag arthurgo/w24ok-web:1.0 .
