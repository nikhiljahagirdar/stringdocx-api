  bind = "0.0.0.0:8080"
    workers = 1
    worker_class = "uvicorn.workers.UvicornWorker"
    worker_tmp_dir = "/dev/shm"
