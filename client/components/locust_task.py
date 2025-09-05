import sys
import time

from locust import events
from locust.exception import ResponseError

def custom_locust_task(name):
    def decorator(func):
        def wrapper(*args, **kwargs):
            res, err = None, None
            start_time = time.time()
            try:
                res = func(*args, **kwargs)
            except Exception as e:
                err = "error {}".format(e)

            if res == "skip":
                return

            events.request.fire(
                request_type="postgres",
                name=name,
                response_time=int((time.time() - start_time) * 1000),
                response_length=sys.getsizeof(res) if res else 0,
                exception=err
            )
        return wrapper
    return decorator