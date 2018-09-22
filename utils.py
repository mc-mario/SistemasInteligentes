import time
def time_it(f, *args, **kwargs):
    def wrapper(f, *args, **kwargs):
        start_time = time.time()
        f(*args, **kwargs)
        time.time() - start_time
    return wrapper