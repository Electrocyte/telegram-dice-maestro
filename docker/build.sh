#!/usr/bin/env bash
# From https://blog.hypriot.com/post/setup-simple-ci-pipeline-for-arm-images/
set -euo pipefail

# $1 Image repo
# $2 Tag
# $3 Dockerfile

docker run --rm --privileged multiarch/qemu-user-static:register --reset

docker build -t "${1}:${2}" -f "${3:-Dockerfile}" .

# docker push "${1}:${2}"
