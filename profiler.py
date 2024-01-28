from collections import defaultdict
import time

class Profiler:
    """
    A code profiling class
    Keep track of function calls and runtime
    """
    calls = defaultdict(int)
    time = defaultdict(float)

    @staticmethod
    def profile(f):
        """Profile Decorator"""
        def wrapper(*args, **kwargs):
            function_name = str(f).split()[1]
            #start timeer
            start = time.time_ns()
            #call function
            val = f(*args, **kwargs)

            # Compute elapsed time
            elapsed = (time.time_ns() - start) / 10**9
            # update calls and time dictionaries
            Profiler.calls[function_name] += 1
            Profiler.time[function_name] += elapsed
            # return the value of function
            return val


        return wrapper

    @staticmethod
    def report():
        print("Function              Calls     TotSec   Sec/Call    Call/Sec")
        for name, calls in Profiler.calls.items():
            elapsed = Profiler.time[name]
            print(f'{name:20s} {calls:6d} {elapsed:10.6f} {elapsed / calls:10.6f} {round(calls/elapsed)}')