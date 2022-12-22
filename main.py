import argparse
import numpy as np
import math
import matplotlib.pyplot as plt

from utils import (
    Polygon
)
from algos import (
    angular_random,
    iterative_hull
)

# Run a simulation and generate the plots
def run(n, algo):
    assert algo == "angular" or algo == "iterative"
    assert algo == "iterative_gauss" or algo == "iterative_beta"
    # Choice of algorithm
    if algo == "angular":
        poly = angular_random(n)

    elif algo == "iterative":
        poly = iterative_hull(n)
        
    elif algo == "iterative_gauss":
        poly = iterative_hull(n, init='gauss')
        
    elif algo == "iterative_beta":
        poly = iterative_hull(n, init='beta')

    poly.visualize()

    

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=10, help="Number of pts")
    parser.add_argument(
        "--algo",
        type=str,
        default="angular",
        help="Type of algorithm",
    )

    args = parser.parse_args()

    run(args.n, args.algo)


if __name__ == "__main__":
    main()
