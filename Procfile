web: gunicorn my_new_manager.wsgi
beat: celery -A my_new_manager.celery:app beat -S redbeat.RedBeatScheduler --loglevel=DEBUG --pidfile /tmp/celerybeat.pid
worker: celery -A my_new_manager.celery:app worker -Q default -n project.%%h --without-gossip --without-mingle --without-heartbeat --loglevel=INFO --max-memory-per-child=512000 --concurrency=1
