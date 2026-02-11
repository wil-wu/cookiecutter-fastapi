#!/bin/bash
set -e

# Docker 镜像构建变量
REPO="${REPO:-{{ cookiecutter.docker_repo }}}"
APP_NAME="${APP_NAME:-{{ cookiecutter.project_slug }}}"
VERSION="${VERSION:-{{ cookiecutter.project_version }}}"
TIMESTAMP="${TIMESTAMP:-$(date +%Y%m%d%H%M%S)}"

# 完整镜像名
IMAGE_TAG="${REPO}/${APP_NAME}:${VERSION}-${TIMESTAMP}"

echo "Building Docker image..."
echo "  REPO:      ${REPO}"
echo "  APP_NAME:  ${APP_NAME}"
echo "  VERSION:   ${VERSION}"
echo "  TIMESTAMP: ${TIMESTAMP}"
echo "  Tag:       ${IMAGE_TAG}"
echo ""

docker build -t "${IMAGE_TAG}" .
