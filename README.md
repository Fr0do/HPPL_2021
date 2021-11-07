## Assignments for High Performance Python Lab @ Skoltech, 2021

**Task 1**: Bifurcation diagram     
Plot classical bifurcation map. $x_{n+1} = r * x_n * (1 - x_n)$ where $x_0 = rand(0, 1)$, $r$ - const.

| | Criteria  | Points |
| -- | ------------- | -- |
|1| Implement the map, plot the evolution of x | 1 |
|2| Create a linspace of r’s, for every r save the last “m” values of x after the first “n” values (can be m=200, n=200), play around with values | 1 |
|3| Plot the bifurcation map | 1 |


**Task 2**: Julia set    
For a fixed complex number c, the Julia set Jc is the set of complex numbers for which the iterative process 
z -> z^2 + c
does not diverge to infinity.
| | Criteria  | Points |
| -- | ------------- | -- |
|1| Black and white colors of pixels are correct | 1 |
|2| Different colors for bifurcation points (you can also create your own coloring logic or look for proposals on the internet) | 1 |
|3| Generate figure of Julia set (c = 1-r) where r is the golden ratio. Label the axes (Re(z0), Im(z0)), fontsize should be 20, figsize = (14,11) | 2 |
|4| Plot figures for c=exp(ia), a = range(0,2pi) & write down axes like in subtask 3, create animation of these figures slowly changing the a | 2 |


**Task 3**: Schelling model    
1) Suppose there are two types of agents: X and O. Two populations of the two agent types are initially placed into random locations of a neighborhood
represented by a grid. After placing all the agents in the grid, each cell is either occupied by an agent or is empty.
2) Now we must determine if each agent is satisfied with its current location. A satisfied agent is one that is surrounded by at least t percent of agents that are like itself. This threshold t is one that will apply to all agents in the model.
3) When an agent is not satisfied, it can be moved to any vacant location in the grid. Any algorithm can be used to choose this new location. For example, a randomly selected cell may be chosen, or the agent could move to the nearest available location.
4) All dissatisfied agents must be moved in the same round. After the round is complete, a new round begins, and dissatisfied agents are once again moved to new locations in the grid.

| | Criteria  | Points |
| -- | ------------- | -- |
|1| Create 9 gifs of map evolution for 9 values of R | 5 |
|2| Plot the number of households that want to move versus time for 9 values of R on one graph, label 9 curves, label the axes and title the graph. | 2 |



**Task 4**: Spectrogram    
A *spectrogram* is a plot of signal intensity versus time and frequency. It is produced using the windowed Fourier transform. To do the home task use the code provided during the session.

| | Criteria  | Points |
| -- | ------------- | -- |
|1| Add 4th wave packet (frequency = 4 and time_shift = 7 cycles). Demonstrate the effect on the plot of the FFT spectrum | 1 |
|2|  Implement the spectrogram, show the effect of (1) on the spectrogram. Don’t forget to label the axes | 2 |
|3| Change the number of time steps in your signal to the power of 2 (i.e. 2^14) and then slightly change the number of timesteps (i.e 2^14 +- 5). Measure the timing, can you explain the difference? Write something as a possible explanation. | 2 |


