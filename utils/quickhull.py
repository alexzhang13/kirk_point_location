# ----- #
# Alex Zhang #
# Adapted from my own PSET1/4 #
# ----- #

import sys
import math
from utils.utils import (
    CCW, 
    dist_to_line
)


def convex_sort(convexHull):
    # Sort hull in clockwise without using angles...

    sortedConvexHull = []

    # sort in clockwise with leftmost first
    leftMost, rightMost, toAdd_idx, rightMost_idx = convexHull[0], convexHull[0], 0, 0

    n = len(convexHull)
    for i in range(n):
        if convexHull[i][0] <= leftMost[0]:
            if convexHull[i][0] == leftMost[0] and convexHull[i][1] >= leftMost[1]:
                pass
            else:
                leftMost = convexHull[i]
                toAdd_idx = i
        if convexHull[i][0] >= rightMost[0]:
            if convexHull[i][0] == rightMost[0] and convexHull[i][1] <= rightMost[1]:
                pass
            else:
                rightMost = convexHull[i]
                rightMost_idx = i

    sortedConvexHull.append(leftMost)  # add leftmost point
    convexHull[toAdd_idx] = None

    # Do top hull first
    prev = leftMost
    for i in range(n - 1):
        toAdd, toAdd_idx = None, 0  # set to max value and get min
        for j in range(len(convexHull)):
            # check if taken or if not on top hull
            if convexHull[j] is None or convexHull[j][1] < prev[1]:
                continue
            if toAdd is None or convexHull[j][0] <= toAdd[0]:
                if toAdd is not None and (
                    convexHull[j][0] == toAdd[0] and convexHull[j][1] >= toAdd[1]
                ):
                    continue
                toAdd = convexHull[j]
                toAdd_idx = j

        if toAdd == rightMost or toAdd is None:
            break
        prev = toAdd
        sortedConvexHull.append(toAdd)
        convexHull[toAdd_idx] = None

    sortedConvexHull.append(rightMost)
    convexHull[rightMost_idx] = None
    # Do bottom hull
    for i in range(n - 1):
        toAdd, toAdd_idx = None, 0  # set to max value and get min
        for j in range(len(convexHull)):
            # check if taken or if not on top hull
            if convexHull[j] is None:
                continue
            if toAdd is None or convexHull[j][0] >= toAdd[0]:
                if (
                    toAdd is not None
                    and convexHull[j][0] == toAdd[0]
                    and convexHull[j][1] <= toAdd[1]
                ):
                    continue
                toAdd = convexHull[j]
                toAdd_idx = j

        if toAdd == rightMost or toAdd is None:
            break

        sortedConvexHull.append(toAdd)
        convexHull[toAdd_idx] = None

    return sortedConvexHull


def angle_sort(convexHull):
    assert len(convexHull) > 0
    sortedConvexHull = []

    left = convexHull[0]
    mid = [0.0, 0.0]
    for point in convexHull:
        mid[0] += point[0]
        mid[1] += point[1]
        if (point[0] < left[0]) or (left[0] == point[0] and left[1] > point[1]):
            left = point

    mid[0] /= len(convexHull)
    mid[1] /= len(convexHull)

    def byAngle(point):
        v = [point[0] - mid[0], point[1] - mid[1]]
        length = math.hypot(v[0], v[1])
        # If length is zero there is no angle
        if length == 0:
            return 0, 0
        # Normalize
        v[0] /= length
        v[1] /= length
        angle = math.atan2(v[0], v[1])

        # if negative deal with it
        if angle < 0:
            return 2 * math.pi + angle, length
        return angle, length

    sortedConvexHull = [i for i in reversed(sorted(convexHull, key=byAngle))]

    start = 0
    for i in range(len(sortedConvexHull)):
        if sortedConvexHull[i] == left:
            start = i
            break

    return sortedConvexHull[start:] + sortedConvexHull[:start]


convexHull = []


def quickhull(points):
    global convexHull
    if len(points) <= 2:
        return []

    n = len(points)

    # get min and max of x coord
    end_a_idx = 0
    end_b_idx = 0
    convexHull = []

    for i in range(n):
        if points[i][0] < points[end_a_idx][0]:
            end_a_idx = i
        if points[i][0] > points[end_b_idx][0]:
            end_b_idx = i

    convexHull.append(points[end_a_idx])
    convexHull.append(points[end_b_idx])

    # remove points from candidacy
    end_a = points[end_a_idx]
    end_b = points[end_b_idx]
    points[end_a_idx] = None
    points[end_b_idx] = None
    # check the left
    findhull(points, end_a, end_b, 1)
    findhull(points, end_a, end_b, -1)

    if len(convexHull) == 0:
        return []

    return angle_sort(convexHull)


def findhull(points, end_a, end_b, orientation):
    assert len(points) > 0
    n = len(points)
    farthestIdx = -1
    farthestDist = 0

    # given line formed by end_a, end_b and specified side
    # find max dist to L on correct side in O(n)
    for i in range(n):
        # on other side of the line (CCW = 1)
        if (
            points[i] is not None
            and CCW(end_a[0], end_a[1], points[i][0], points[i][1], end_b[0], end_b[1])
            == orientation
        ):
            dist = dist_to_line(
                end_a[0], end_a[1], points[i][0], points[i][1], end_b[0], end_b[1]
            )
            if dist > farthestDist:
                farthestDist = dist
                farthestIdx = i

    # add endpoints if none found, we are done
    if farthestIdx == -1:
        return

    furthest = points[farthestIdx]
    points[farthestIdx] = None
    convexHull.append(furthest)

    # check orientation that is CCW between new point, end_a, end_b
    findhull(
        points,
        furthest,
        end_a,
        -CCW(furthest[0], furthest[1], end_b[0], end_b[1], end_a[0], end_a[1]),
    )
    findhull(
        points,
        furthest,
        end_b,
        -CCW(furthest[0], furthest[1], end_a[0], end_a[1], end_b[0], end_b[1]),
    )


def main():
    # read in line by line
    line = sys.stdin.readline()

    n = int(line)

    for i in range(n):
        line = sys.stdin.readline()
        m = int(line)
        points = []

        for j in range(m):
            line = sys.stdin.readline()
            input = line.replace("\n", "").strip().split(" ")
            numbers = [float(j) for j in input]
            points.append(numbers)
        print("Case #{}".format(i + 1))
        for point in quickhull(points):
            print(int(point[0]), int(point[1]))


if __name__ == "__main__":
    main()
