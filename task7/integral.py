
import matplotlib.pyplot as plt
from mpi4py import MPI
import numpy as np
import argparse

def f(x):
    return np.exp(np.arccos(x))

def f_int(x):
    return (x - np.sqrt(1 - x**2)) * f(x) / 2

def integrate(f, limits, step):
    """
    Compute function integral by using trapezoid rule.
        f: function to integrate
        limits: ends of a segment over which we wish to integrate
        steps: # of discretization steps
    """
    x = np.linspace(limits[0], limits[1], step)
    f_x = f(x)
    result = (f_x[0] + f_x.sum() * 2 + f_x[-1]) * 0.5 * (x[1] - x[0])
    return result

def main(steps=1e+5):
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    all_nodes = np.linspace(-1, 1, num=size + 1)
    s = integrate(f, limits=all_nodes[rank: rank + 2], step = steps // size)
    comm.Barrier()

    s = comm.gather(s, root=0)

    if rank == 0:
        return sum(s)

if __name__ == '__main__':
    parser = argparse.ArgumentParser("Task 7")
    parser.add_argument("-steps",  help="# of discretization steps", type=int)
    args = parser.parse_args()
    main(args.steps)
