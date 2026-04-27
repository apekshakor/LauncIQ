import time

class RateLimiter:
    def __init__(self):
        self.last_call = 0
        self.min_delay = 2

    def wait(self):
        now = time.time()
        if now - self.last_call < self.min_delay:
            time.sleep(self.min_delay - (now - self.last_call))
        self.last_call = time.time()

rate_limiter = RateLimiter()