#!/usr/bin/env bash
# From https://blog.hypriot.com/post/setup-simple-ci-pipeline-for-arm-images/
set -euo pipefail

# $1 Image repo
# $2 Tag

docker push "${1}:${2}"
