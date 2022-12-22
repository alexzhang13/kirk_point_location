# ----
# Util functions
# Author: Alex Zhang
# ----

import numpy as np
import math

# use CCW to find side of c w/ respect to a-b
def CCW(a_x, a_y, b_x, b_y, c_x, c_y):
    # if A \neq B
    if a_x != b_x or a_y != b_y:
        # compute cross product, >0 is CCW
        prod = (b_y - a_y) * (c_x - b_x) - (b_x - a_x) * (c_y - b_y)

        # counterclockwise
        if prod > 0:
            return 1
        # clockwise
        elif prod < 0:
            return -1
    # otherwise
    return 0

def intersect(a_x, a_y, b_x, b_y, c_x, c_y, d_x, d_y):
    # idea is if segments intersect, CCW between (a,b,c) and (a,b,d) differ
    # AND (c,d,a) and (c,d,b) differ

    if CCW(a_x, a_y, b_x, b_y, c_x, c_y) != CCW(a_x, a_y, b_x, b_y, d_x, d_y) and CCW(
        c_x, c_y, d_x, d_y, a_x, a_y
    ) != CCW(c_x, c_y, d_x, d_y, b_x, b_y):
        return 1

    # check if all points are collinear
    if (
        CCW(a_x, a_y, b_x, b_y, c_x, c_y) == CCW(a_x, a_y, b_x, b_y, d_x, d_y)
        and CCW(a_x, a_y, b_x, b_y, c_x, c_y) == 0
        or CCW(c_x, c_y, d_x, d_y, a_x, a_y) == CCW(c_x, c_y, d_x, d_y, b_x, b_y)
        and CCW(c_x, c_y, d_x, d_y, b_x, b_y) == 0
    ):
        return 1

    return 0

# distance from b to a-c is just normalized cross product
# but we don't need to normalize
def dist_to_line(a_x, a_y, b_x, b_y, c_x, c_y):
    prod = (b_y - a_y) * (c_x - b_x) - (b_x - a_x) * (c_y - b_y)
    return abs(prod)

# check if two edges are intersecting 
def intersect_edges(edge1, edge2):
    return intersect(edge1.p[0], edge1.p[1], edge1.q[0], edge1.q[1],
                     edge2.p[0], edge2.p[1], edge2.q[0], edge2.q[1])

# min distance from a point to a line segment (same as to line except)
# line segment doesn't extend
# argument derived from http://paulbourke.net/geometry/pointlineplane/
def dist_point_to_line_seg (point, edge):
    # compute vectors
    edge_dist = (edge.p[0] - edge.q[0], edge.p[1] - edge.q[1])
    point_to_edge = (edge.p[0] - point[0], edge.p[1] - point[1])
    
    # compute norms for dot product
    norm = math.sqrt(edge_dist[0]**2 + edge_dist[1]**2)
    unit_edge_dist = (edge_dist[0] / norm, edge_dist[1] / norm)
    unit_point_to_edge = (point_to_edge[0] / norm, point_to_edge[1] / norm)
    t = unit_edge_dist[0] * unit_point_to_edge[1] + unit_edge_dist[1] * unit_point_to_edge[1]
    
    # if line goes out, clip it
    t = min(max(t, 0.0), 1.0)
    nearest = (edge_dist[0] * t, edge_dist[1] * t)
    dist = math.sqrt((nearest[0]-point_to_edge[0])**2 + (nearest[1]-point_to_edge[1])**2)
    return dist
