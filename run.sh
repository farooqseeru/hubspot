uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
#gunicorn -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8000 --workers 4 &
