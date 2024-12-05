import time


def measure_func_exec_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()  # Record the start time
        result = func(*args, **kwargs)  # Call the original function
        end_time = time.time()  # Record the end time
        elapsed_time = end_time - start_time  # Calculate the elapsed time
        print(f"Function '{func.__name__}' executed in {elapsed_time:.2f} seconds")
        return result

    return wrapper
