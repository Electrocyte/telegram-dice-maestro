#!/usr/bin/env bash
# From https://blog.hypriot.com/post/setup-simple-ci-pipeline-for-arm-images/
set -euo pipefail

# $1 Image repo
# $2 Tag

echo "${DOCKER_PASSWORD}" | base64 -d | docker login -u "${DOCKER_USERNAME}" --password-stdin

docker push "${1}:${2}"
