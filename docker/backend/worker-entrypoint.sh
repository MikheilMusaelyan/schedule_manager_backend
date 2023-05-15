#!/bin/sh

until cd /app/my_new_manager
do
    echo "Waiting for server volume..."
done

# run a worker :)
celery -A my_new_manager worker --loglevel=info --concurrency 1 -E
