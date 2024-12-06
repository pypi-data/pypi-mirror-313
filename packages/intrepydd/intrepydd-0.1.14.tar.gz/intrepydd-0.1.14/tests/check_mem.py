import gc
import numpy as np

def list_all_numpy_objects():
    all_objects = gc.get_objects()  # Get all objects tracked by the garbage collector
    numpy_objects = [obj for obj in all_objects if isinstance(obj, np.ndarray)]  # Filter for numpy arrays
    return numpy_objects

def foo(a, r, b, iters):
    for i in range(iters):
        # Check the number of objects in memory before the operation
        before_count = len(gc.get_objects())
        
        c = 1.0 / (a @ b)  # Compute intermediate result
        
        # Check the number of objects in memory after the operation
        after_count = len(gc.get_objects())
        
        # Assign b to new value
        b = r @ c
        
        print(f"Iteration {i}: Objects before: {before_count}, Objects after: {after_count}")
    
    return b

# Example usage with dummy arrays
import numpy as np
a = np.random.rand(1000, 1000)
r = np.random.rand(1000, 1000)
b = np.random.rand(1000, 1000)
iters = 5

foo(a, r, b, iters)
print(list_all_numpy_objects())
