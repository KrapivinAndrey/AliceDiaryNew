import time

auth_service = None
perf_monitor = None


def perfmon(func):
    def func_wrapper(*args, **kwargs):
        if perf_monitor is None:
            return func(*args, **kwargs)
        start = time.time()
        result = func(*args, **kwargs)
        stop = time.time()
        perf_monitor.save_measure(method=func.__name__, start=start, stop=stop)
        return result

    return func_wrapper
