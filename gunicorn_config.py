import os

workers = int(os.getenv("GUNICORN_WORKERS", "4"))
bind = f"0.0.0.0:{os.getenv('PORT', '8000')}"
worker_class = "uvicorn.workers.UvicornWorker"
keepalive = 120
timeout = 120 