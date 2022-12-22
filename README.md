# Randomized simple polygon generation
Implementation and experiments for random simple polygon generation.

There are two different generations, one being based on circles and the other being based on a set of random
points from the convex hull.

## Dependencies
The only dependencies are `matplotlib`, `argparse`, and `numpy`, and some working version of 'Python 3'. There is also a requirements.txt file included if necessary.

## Running the program
Included is a Jupyter notebook called 'visualize.ipynb' that can be viewed, but if you want to run your own experiments, use 'main.py'. There are a few arguments such as `--n` for specifying the number of points, and `--algo` for the different algorithms (angular, iterative, iterative_gauss, iterative_beta). For example, you can run
```
python main.py --n 100 --algo iterative_gauss
```
