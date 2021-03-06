
import matplotlib.pyplot as plt
from mpi4py import MPI
import numpy as np

def parallel_bifurcation(proc, points_X = 1000, n_proc = 8, minX = 0, maxX = 4, steps = 10000, m = 30):
    block_X = points_X // n_proc # integer blocks of x axis
    remainder = points_X % n_proc # remainder for the last block

    add = 0 # addition of the last block
    if proc == n_proc - 1: # if current process is last
        add = remainder # addition is equal to remainder
    
    # current x array
    arrayX = np.arange(block_X * proc, block_X * (proc + 1) + add, 1)
    
    r = np.linspace((proc) * maxX / n_proc, (proc + 1) * maxX / n_proc, arrayX.size)
    
    X = np.zeros((block_X, m)) # array for scatterplot
    Y = np.zeros((block_X, m)) # array for scatterplot
    x = np.zeros(steps)
    
    for j in range(0, block_X, 1):
        x[0] = np.random.rand()
        
        for n in range(1, steps):
            x[n] = r[j] * x[n-1] * (1 - x[n-1])
            
        X[j] = (x[steps - m:steps]) # take into account the last m values
        Y[j] = r[j] # set r value for each x[inf] - for scatter plot
    return X, Y

comm = MPI.COMM_WORLD
n_proc = comm.Get_size() # processors
rank = comm.Get_rank() # current rank

if rank == 0:
    t0 = MPI.Wtime() # measure start time

X, Y = parallel_bifurcation(proc = rank, points_X = 2000, n_proc = n_proc, minX = 0, maxX = 4, steps = 500, m = 40)
X, Y = comm.gather(X, root=0), comm.gather(Y, root=0)

if rank == 0:
    t = MPI.Wtime() - t0
    with open('./time.csv', 'a+') as f:
         f.write(f'{n_proc}, {np.round(t, 4) * 1000}\n')

    fig = plt.scatter(Y, X, c = 'b', s = 0.05)

    plt.title('Bifurcation diagram', fontsize=12)
    plt.ylabel('Values of static points', fontsize=12)
    plt.xlabel('Value of r', fontsize=12)
    plt.savefig(f'./bifurcation_{n_proc}_processes', dpi=300)
    plt.close()
