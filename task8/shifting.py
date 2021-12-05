import numpy as np
from mpi4py import MPI
import matplotlib.pyplot as plt
from PIL import Image
import time
import sys
import os


def main(a_path, h):
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    img = np.array(Image.open(a_path), dtype=np.uint8)
    img_h = img.shape[0]
    img_w = img.shape[1]
    roll  = img.shape[2]
        
    # Data preparation
    if rank == 0:
        # count the size of the array of each process
        q = img_w // size
        r = img_w % size

        sizes = [q + 1 if i < r else q for i in range(size)]
        sizes = np.array(sizes, dtype=np.int32)
        
        # the starting index of each process
        shifts = [sum(sizes[:i]) for i in range(size)]
        shifts = np.array(shifts, dtype=np.int32)
    else:
        sizes = np.zeros(size, dtype=np.int32)
        shifts = np.zeros(size, dtype=np.int32)

    # Broadcasting
    comm.Bcast(sizes)
    comm.Bcast(shifts)
    
    # Initial shifts
    img = np.roll(img, roll * shifts[rank], axis=1)
    for shift in range(shifts[rank], shifts[rank] + sizes[rank]):
        Image.fromarray(img).save(f"../imgs/task8/img_{shift:09d}.png")
        img = np.roll(img, roll, axis=1)

    # Memory usage
    if h:
        mem_used = h.heap().size
        mem_usage = comm.reduce(mem_used, op=MPI.SUM)
    else:
        mem_usage = None
        comm.Barrier()

    if rank == 0:
        return img_w, mem_usage
    else:
        return None, mem_usage

if __name__ == "__main__":
    path = sys.argv[1]
    
    # Memory check
    h = None
    arg = None
    if len(sys.argv) == 3:
        arg = sys.argv[2]
        if arg == "memory":
            from guppy import hpy
            h = hpy()

    MPI.COMM_WORLD.Barrier()

    start = time.time()
    n, mem = main(path, h)
    elapsed = time.time() - start

    if n is not None:
        if arg == "save":
            images = []
            for i in range(n):
                fname = f"../imgs/task8/img_{i:09d}.png"
                images.append(Image.open(fname))
            images[0].save('./shifted.gif', save_all=True, append_images=images[1:], loop=0, duration=50)
            print(f"Elapsed time: {elapsed}")
        elif arg == "memory":
            print(mem)
        else:
            print(elapsed)
        for i in range(n):
            fname = f"../imgs/task8/img_{i:09d}.png"
            os.remove(fname)
