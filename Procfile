web: gunicorn -b $HOST:$PORT -b [::1]:$PORT -k ${GUNICORN_WORKER_TYPE:-eventlet} -t ${GUNICORN_TIMEOUT:-60} --graceful-timeout ${GUNICORN_TIMEOUT:-60} --keep-alive ${GUNICORN_KEEP_ALIVE:-4} -w ${GUNICORN_WORKERS:-8} readthestuff.app:app
dev: python manage.py runserver --host=$HOST --port=$PORT
rq: rqworker -c readthestuff.settings
