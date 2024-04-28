#!/bin/bash


# Perform a git pull to update the code
git pull

# install packages
docker compose run --rm taxgpt-backend pip install -r requirements.txt

docker compose up -d --build taxgpt-backend
docker compose up -d --build celery-worker
docker compose run --rm taxgpt-backend python manage.py migrate
docker compose run --rm taxgpt-backend python manage.py collectstatic
# remove danging images
echo "Running Docker image prune..."
yes | docker image prune
