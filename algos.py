# ----
# Triangulation operations over a polygon
# Author: Alex Zhang
# ----
from utils import (
    Polygon,
    Edge,
    quickhull,
    utils
)
import random
import math
import numpy as np
import heapq
from scipy.stats import halfnorm

class PointToEdge:
    def __init__(self, dist, point, edge):
        self.dist = dist
        self.point = point
        self.edge = edge
    
    # define comparator
    def __gt__(self, pte):
        return self.dist > pte.dist
    
    # print for debugging purposes
    def __repr__(self):
        return ('dist: ' + str(self.dist) + ' p,e:' + str(self.point) + str(self.edge))

    def __str__(self):
        return ('dist: ' + str(self.dist) + ' p,e:' + str(self.point) + str(self.edge))


def iterative_hull (n, debug=False):
    pts = np.random.rand(n, 2)
    pointsToAdd = list(zip(pts[:, 0], pts[:, 1]))
    points = quickhull(pointsToAdd.copy())
    
    if debug:
        print(points)
        testPoly = Polygon(pointsToAdd.copy())
        testPoly.visualize(nolines=True)
    
    poly = Polygon(points.copy())
    
    # O(v^2) update set of points to add
    for item in points:
        if item in pointsToAdd:
            pointsToAdd.remove(item)
    
    # If hull is the entire simple polygon
    if len(pointsToAdd) == 0:
        return poly
    
    # construct set of PointToEdge in min priority queue
    dist_heap = []
    heapq.heapify(dist_heap)
    
    def update_pq(edge):
        for point in pointsToAdd:
            dist = utils.dist_point_to_line_seg(point, edge)
            pte = PointToEdge(dist, point, edge)
            heapq.heappush(dist_heap, pte)
    
    for edge in poly._edges:
        update_pq(edge)
    
    if debug:
        print([str(item) + '\n' for item in list(dist_heap)])
    
    # main iteration loop
    while len(pointsToAdd) != 0 and len(dist_heap) != 0:
        pte = heapq.heappop(dist_heap)
        
        if debug:
            poly.visualize()
        
        # check if point has been dealt with
        if pte.point not in pointsToAdd:
            continue

        edgeIndex = poly.edgeIndex(pte.edge)
        e1 = Edge(pte.edge.p, pte.point)
        e2 = Edge(pte.point, pte.edge.q)
        intersects = poly.intersects(e1) or poly.intersects(e2)
        
        # Does edge exist and is point inside polygon? --> edge case of self-intersect
        if edgeIndex >= 0 and not intersects:
            # replace old edge and add two more
            poly._edges[edgeIndex] = e1
            poly._edges.insert(edgeIndex+1, e2)
            poly._polyPoints.insert(edgeIndex+1, pte.point) # add vertex in same order
            
            pointsToAdd.remove(pte.point)
            
            # update pq with new edges
            update_pq(e1)
            update_pq(e2)
    
    return poly
    

def angular_random(n, 
                   center=(0,0),
                   a_mu=1,
                   a_sigma=1,
                   l_mu=1, 
                   l_sigma=4, 
                   debug=False):
    '''
    Generate simple polygon by using random rotations around a point and random radius vectors.
    '''
    
    center = center # (random.random(), random.random())
    angle = 0 # random.uniform(0, 2*math.pi)

    angles = []
    vertices = []
    
    # generate n angles
    r = halfnorm(a_mu, a_sigma).rvs(size=n)
    for i in range(n):
        add = r[i]
        if len(angles) == 0:
            angles.append(add)
        else:
            angles.append(add + angles[-1])
    
    normalizing_factor = 2 * math.pi / (angles[-1])
    
    if debug:
        print('Angles', angles, 'normalize', normalizing_factor)
    
    for i in range(n):
        angles[i] *= normalizing_factor
    
    if debug:
        print('Center', center)
        print('Processed Angles', angles)
    
    r = halfnorm(l_mu, l_sigma).rvs(size=n)
    for i in range(n): # Primary loop O(n)
        angle = angles[i]
        length = random.uniform(0, l_mu) #r[i]
        vertices.append((
            center[0] + length * math.cos(angle),
            center[1] + length * math.sin(angle)
        ))
    
    if debug:
        print(vertices)
    
    return Polygon(vertices)
 