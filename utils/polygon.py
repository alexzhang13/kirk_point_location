# ----
# Polygon data structure
# Author: Alex Zhang
# ----

import matplotlib.pyplot as plt
import numpy as np
from utils.quickhull import quickhull
from utils.utils import (
    intersect_edges
)

class Edge:
    '''
    Helper class for edge
    '''
    def __init__(self, p, q):
        self.p = p
        self.q = q
    
    def __eq__(self, edge):
        return self.p == edge.p and self.q == edge.q
    
    def __repr__(self):
        return str(self.p) + ',' + str(self.q)

    def __str__(self):
        return str(self.p) + ',' + str(self.q)

class Polygon:
    """
    Polygon class for running sweepline triangulation
    """

    def __init__(self, points):
        
        self._polyPoints = points  # set of points [(x,y),...] in the order of connection to the (simple) polygon
        self._convexHull = []
        self._edges = []
        
        for i in range(len(points)):
            edge = Edge(points[i], points[(i+1) % len(points)])
            self._edges.append(edge)
            
    def intersects(self, e):
        '''
        Check if edge e intersects any edges in the polygon 
        '''
        for edge in self._edges:
            if (edge.p != e.p and edge.q != e.q) and \
               (edge.p != e.q and edge.q != e.p):
                   if intersect_edges(edge, e):
                       return True
        return False

    def vertexIndex(self, v):
        '''
        Check if polygon contains vertex in O(n)
        '''
        for p in self._polyPoints:
            if v == p:
                return self._polyPoints.index(p)
        return -1
    
    def edgeIndex(self, e):
        '''
        Check if polygon contains edge in O(n)
        '''
        for edge in self._edges:
            if e == edge:
                return self._edges.index(e)
        return -1

    def computeHull(self):
        self._convexHull = quickhull(self._polyPoints.copy())
        return self._convexHull

    def visualize(self, nolines=False):
        '''
        Visualize simple polygon based on order of vertices
        '''
        vertices = self._polyPoints
        
        vertices.append(vertices[0]) # add first point for completion
        
        x, y = zip(*vertices)
        
        if nolines:
            plt.plot(x, y, 'ro')
        else:
            plt.plot(x, y, 'r-')
        plt.show()