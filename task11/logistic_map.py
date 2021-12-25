
# MPI implementation

import numpy as np
from mpi4py import MPI
import matplotlib.pyplot as plt
import time
import sys


def logistic_map(x, r):
    return r*x*(1-x)

def bm_np(points=400, rs=None):
    # I will skip first 500 values and then plot following 32 values
    if rs is None:
        rs = np.linspace(0, 3.99, points)
        xn = np.array([0.5]*points)
    else:
        xn = np.array([0.5]*len(rs))
    n = 500  # skip first 500 values
    m = 32  # save last 32 values

    xs = np.zeros(points*m)
    ys = np.zeros(points*m)
        
    # skip first "n" values
    for _ in range(n):
        xn = logistic_map(xn, rs)
    
    # save last "m" values
    for i in range(m):
        ys[i*points : (i+1)*points] = xn
        xs[i*points : (i+1)*points] = rs
        xn = logistic_map(xn, rs)
    
    return xs, ys


def main(points):
    # Mantra
    comm = MPI.COMM_WORLD
    size = comm.Get_size()
    rank = comm.Get_rank()
    samples = points
    m = 32

    # Data preparation
    if rank == 0:
        rs = np.linspace(0, 3.99, samples)

        # count the size of the array of each process
        quot, rem = divmod(samples, size)
        chunk_sizes = [quot + 1 if i < rem else quot for i in range(size)]
        chunk_sizes = np.array(chunk_sizes)

        # the starting index of each process (displacement or shift)
        chunk_displs = [sum(chunk_sizes[:i]) for i in range(size)]
        chunk_displs = np.array(chunk_displs)
        
        ys_sizes = chunk_sizes*m
        ys_displs = chunk_displs*m
        
        ys = np.zeros(samples*m, dtype=np.double)
        xs = np.zeros(samples*m, dtype=np.double)
    else:      
        chunk_sizes = np.zeros(size, dtype=int)
        ys_sizes = np.zeros(size, dtype=int)
        
        rs = None
        chunk_displs = None
        ys_displs = None
        ys = None
        xs = None
    
    # Broadcasting
    comm.Bcast(chunk_sizes)
    comm.Bcast(ys_sizes)
    
    # buffer for scattering
    rs_chunk = np.zeros(chunk_sizes[rank], dtype=np.double)
    
    # Scattering data
    comm.Scatterv([rs, chunk_sizes, chunk_displs, MPI.DOUBLE], rs_chunk)
    
    # Parallel computing
    xs_chunk, ys_chunk = bm_np(chunk_sizes[rank], rs_chunk)
    
    # Gathering back
    comm.Gatherv(ys_chunk, [ys, ys_sizes, ys_displs, MPI.DOUBLE])
    comm.Gatherv(xs_chunk, [xs, ys_sizes, ys_displs, MPI.DOUBLE])
    
    # Saving
    if rank == 0:
        return (xs, ys)
    return None


if __name__ == "__main__":
    if len(sys.argv) == 2:
        points = int(sys.argv[1])
    else:
        points = 400
    
    # Logistic map calculation
    start = time.perf_counter()
    ans = main(points)
    elapsed = time.perf_counter() - start
    
    if MPI.COMM_WORLD.Get_rank() == 0:
        print(elapsed)
