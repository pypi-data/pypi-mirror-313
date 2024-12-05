from pyinstrument import Profiler
from functools import wraps


class ProfilerManager:
    def __enter__(self):
        self.profiler = Profiler()
        self.profiler.start()
        return self.profiler

    def __exit__(self, exc_type, exc_value, traceback):
        self.profiler.stop()
        print(self.profiler.output_text(unicode=True, color=True))


def profiling(enable_profiling: bool = True):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if enable_profiling:
                with ProfilerManager():
                    return func(*args, **kwargs)
            else:
                return func(*args, **kwargs)

        return wrapper

    return decorator
