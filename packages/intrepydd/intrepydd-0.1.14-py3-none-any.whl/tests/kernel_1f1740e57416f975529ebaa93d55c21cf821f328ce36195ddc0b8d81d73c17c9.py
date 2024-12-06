from intrepydd.lang import *
def foo(a: Array(float64, 2), b: Array(float64, 2), c: Array(float64, 2)) -> Array(float64, 2):
    return div(c, matmult(a, b))
