import numpy as np



def cart2pol(x, y):
    r = np.hypot(x, y)
    angle = np.arctan2(y, x)
    return (r, angle)

def pol2cart(r, angle):
    x = r * np.cos(angle)
    y = r * np.sin(angle)
    return (x, y)



def concentrical_circles(
    num_points, num_circles, radius, z_distance=None, angle_offset="distribute"
):
    a = num_circles // 2
    if z_distance is not None:
        zValues = [i * z_distance for i in range(-a, -a + num_circles)]
        if num_circles % 2 == 0:
            zValues = [zVal + z_distance / 2 for zVal in zValues]
    else:
        zValues = [None for i in range(num_circles)]

    pointsPerCircle = [num_points // num_circles for _ in range(num_circles)]
    for i in range(num_points - num_circles * (num_points // num_circles)):
        pointsPerCircle[i] += 1

    if angle_offset == "random":
        startAngles = np.random.rand(num_circles) * np.pi * 2
    elif angle_offset == "same":
        startAngles = np.zeros(num_circles)
    elif angle_offset == "almostSame":
        angleSection = 2 * np.pi / pointsPerCircle[0]
        startAngles = np.random.rand(num_circles) * (angleSection / 10)
    elif angle_offset == "distribute":
        angleSection = 2 * np.pi / pointsPerCircle[0]
        startAngles = np.arange(num_circles) * angleSection / num_circles

    coords = [
        equiangular_circle(circlePoints, radius, angle, zVal)
        for i, (circlePoints, angle, zVal) in enumerate(
            zip(pointsPerCircle, startAngles, zValues)
        )
    ]

    coords = np.concatenate(coords)
    return coords


def equiangular_circle(num_points, radius, start_angle=0, z=None, rng=None):
    """
    Generates equiangularly spaced points on a circle

    Parameters
    ----------
    num_points : int
        number of points on the circle
    radius : int or 2-tuple
        radius of the circle
        if a tuple is suppled, as (inner_radius, outer_radius)
        each point will be placed randomly (uniform distribution)
        between the inner and outer radius 
    start_angle : float
        the angle in radians of the first point
    z : None or float
        if z is supplied, the all points are given the same z-coordinate
        according to the value of the argument
    rng : None or numpy Generator object
        can be supplied to control the seed of the random number
        generator
    

    Returns
    -------
    coordinates : ndarray of shape (num_points, 2) or (num_points, 3)
        if argument z was supplied
    """
    if rng is None:
        rng = np.random.default_rng()
    
    if isinstance(radius, (int, float)):
        radius = (radius, radius)

    angle_step = 2 * np.pi / num_points

    angles = start_angle + np.arange(num_points) * angle_step
    angles = np.mod(angles, 2 * np.pi)
    radia = rng.uniform(radius[0], radius[1], size=num_points)
    [x, y] = pol2cart(radia, angles)

    if z is not None:
        pos = np.zeros((num_points, 3))
        pos[:, 2] = z
    else:
        pos = np.zeros((num_points, 2))
    pos[:, 0:2] = np.stack((x, y)).T
    return pos


def uniform_cylinder(num_points, radius, height):
    numPlanes = 4
    zVals = np.linspace(-height / 2, height / 2, numPlanes + 2)
    zVals = zVals[1:-1]

    pointsPerPlane = num_points // numPlanes
    allPoints = np.zeros((pointsPerPlane * numPlanes, 3))

    for n in range(numPlanes):
        xyPoints = sunflower_pattern(
            pointsPerPlane, radius, np.random.rand() * 2 * np.pi
        )
        allPoints[n * pointsPerPlane : (n + 1) * pointsPerPlane :, 0:2] = xyPoints
        allPoints[n * pointsPerPlane : (n + 1) * pointsPerPlane, 2] = zVals[n]
    return allPoints



def sunflower_pattern(N, radius, offset_angle=0):
    """ translated from user3717023's MATLAB code from stackoverflow
        could be updated using the method in this paper 
        'A better way to construct the sunflower head'"""
    phisq = np.square((np.sqrt(5) + 1) / 2)
    # golden ratio
    k = np.arange(1, N + 1)
    r = radius * np.sqrt(k - (1 / 2)) / np.sqrt(N - 1 / 2)
    theta = k * 2 * np.pi / phisq
    [x, y] = pol2cart(r, theta)
    return np.stack((x, y)).T


def uniform_disc(point_distance, radius, z_axis=None):
    lim = (-radius, radius)
    numPoints = int(2 * radius / point_distance)
    x = np.linspace(lim[0], lim[1], numPoints)
    y = np.linspace(lim[0], lim[1], numPoints)
    [xGrid, yGrid] = np.meshgrid(x, y)
    xGrid = xGrid.flatten()
    yGrid = yGrid.flatten()

    coords = np.vstack((xGrid, yGrid))
    dist = np.linalg.norm(coords, axis=0)
    idxs2 = dist <= radius
    coordsCircle = coords[:, idxs2].T

    if z_axis is not None:
        coordsCircle = np.concatenate(
            (coordsCircle, np.full((coordsCircle.shape[0], 1), z_axis)), axis=-1
        )
    return coordsCircle


def uniform_filled_rectangle(num_points, lim=(-2.4, 2.4), z_axis=None):
    pointsPerAxis = int(np.sqrt(num_points))
    assert np.isclose(pointsPerAxis ** 2, num_points)
    if len(lim) == 2:
        x = np.linspace(lim[0], lim[1], pointsPerAxis)
        y = np.linspace(lim[0], lim[1], pointsPerAxis)
    elif len(lim) == 4:
        x = np.linspace(lim[0], lim[2], pointsPerAxis)
        y = np.linspace(lim[1], lim[3], pointsPerAxis)

    [xGrid, yGrid] = np.meshgrid(x, y)
    evalPoints = np.vstack((xGrid.flatten(), yGrid.flatten())).T

    if z_axis is not None:
        evalPoints = np.concatenate(
            (evalPoints, np.full((pointsPerAxis ** 2, 1), z_axis)), axis=-1
        )
    return evalPoints

def uniform_filled_cuboid(num_points, dims, z_num_points=4):
    pointsPerAxis = int(np.sqrt(num_points / z_num_points))
    assert np.isclose(pointsPerAxis ** 2 * z_num_points, num_points)
    x = np.linspace(-dims[0] / 2, dims[0] / 2, 2 * pointsPerAxis + 1)[1::2]
    y = np.linspace(-dims[1] / 2, dims[1] / 2, 2 * pointsPerAxis + 1)[1::2]
    z = np.linspace(-dims[2] / 2, dims[2] / 2, 2 * z_num_points + 1)[1::2]
    [xGrid, yGrid, zGrid] = np.meshgrid(x, y, z)
    evalPoints = np.vstack((xGrid.flatten(), yGrid.flatten(), zGrid.flatten())).T

    return evalPoints


def four_equidistant_rectangles(
    num_points, side_length, side_offset, z_low, z_high, offset="distributed"
):
    if offset != "distributed":
        raise NotImplementedError
    points = np.zeros((num_points, 3))
    points[:, 0:2] = equidistant_rectangle(num_points, (side_length, side_length))
    # points[0::2,2] = zLow
    # points[1::2,2] = zHigh

    # idxSet = np.sort(np.concatenate((np.arange(numPoints)[2::4], np.arange(numPoints)[3::4])))
    # for i in idxSet:
    #     if np.isclose(points[i,0], sideLength/2):
    #         points[i,0] += sideOffset
    #     elif np.isclose(points[i,0], -sideLength/2):
    #         points[i,0] -= sideOffset
    #     elif np.isclose(points[i,1], sideLength/2):
    #         points[i,1] += sideOffset
    #     elif np.isclose(points[i,1], -sideLength/2):
    #         points[i,1] -= sideOffset
    #     else:
    #         raise ValueError
    idxSet = np.sort(
        np.concatenate((np.arange(num_points)[2::4], np.arange(num_points)[3::4]))
    )
    points[:, 2] = z_low
    points[idxSet, 2] = z_high
    # points[]
    # points[0::2,2] = zLow
    # points[1::2,2] = zHigh

    for i in np.arange(num_points)[1::2]:
        if np.isclose(points[i, 0], side_length / 2):
            points[i, 0] += side_offset
        elif np.isclose(points[i, 0], -side_length / 2):
            points[i, 0] -= side_offset
        elif np.isclose(points[i, 1], side_length / 2):
            points[i, 1] += side_offset
        elif np.isclose(points[i, 1], -side_length / 2):
            points[i, 1] -= side_offset
        else:
            raise ValueError
    return points


def stacked_equidistant_rectangles(
    num_points, num_rect, dims, z_distance, offset="distributed"
):
    a = num_rect // 2
    zValues = [i * z_distance for i in range(-a, -a + num_rect)]
    if num_rect % 2 == 0:
        zValues = [zVal + z_distance / 2 for zVal in zValues]

    pointsPerRect = [num_points // num_rect for _ in range(num_rect)]
    for i in range(num_points - num_rect * (num_points // num_rect)):
        pointsPerRect[i] += 1

    offsets = np.linspace(0, 1, 2 * num_rect + 1)[1::2]

    points = np.zeros((num_points, 3))
    idxCount = 0
    for i in range(num_rect):
        points[idxCount : idxCount + pointsPerRect[i], 0:2] = equidistant_rectangle(
            pointsPerRect[i], dims, offset=offsets[i]
        )
        points[idxCount : idxCount + pointsPerRect[i], 2] = zValues[i]
        idxCount += pointsPerRect[i]
    return points


def equidistant_rectangle(num_points, dims, offset=0.5, z=None):
    if num_points == 0:
        if z is None:
            return np.zeros((0, 2))
        else:
            return np.zeros((0,3))
    totalLength = 2 * (dims[0] + dims[1])
    pointDist = totalLength / num_points

    points = np.zeros((num_points, 2))
    if num_points < 4:
        points = equidistant_rectangle(4, dims)
        #pointChoices = np.random.choice(4, numPoints, replace=False)
        #points = points[pointChoices, :]
        points = points[:num_points,:]
    else:
        lengths = [dims[0], dims[1], dims[0], dims[1]]
        xVal = [-dims[0] / 2, dims[0] / 2, dims[0] / 2, -dims[0] / 2]
        yVal = [-dims[1] / 2, -dims[1] / 2, dims[1] / 2, dims[1] / 2]

        startPos = pointDist * offset
        xFac = [1, 0, -1, 0]
        yFac = [0, 1, 0, -1]
        numCounter = 0

        for i in range(4):
            numAxisPoints = 1 + int((lengths[i] - startPos) / pointDist)
            axisPoints = startPos + np.arange(numAxisPoints) * pointDist
            distLeft = lengths[i] - axisPoints[-1]
            points[numCounter : numCounter + numAxisPoints, 0] = (
                xVal[i] + xFac[i] * axisPoints
            )
            points[numCounter : numCounter + numAxisPoints, 1] = (
                yVal[i] + yFac[i] * axisPoints
            )
            numCounter += numAxisPoints
            startPos = pointDist - distLeft
    if z is not None:
        points = np.concatenate((points, np.full((points.shape[0], 1), z)), axis=-1)
    return points


def equidistant_rectangle_for_fewer(num_points, dims):
    totalLength = 2 * (dims[0] + dims[1])
    pointDist = totalLength / num_points

    points = np.zeros((num_points, 2))
    if num_points == 1:
        points[0, 0] = np.random.rand() * dims[0] / 4 - dims[0] / 4
        points[0, 1] = np.random.choice([-1, 1]) * dims[1] / 2
    elif num_points == 2:
        points[:, 0] = np.random.rand(2) * dims[0] / 4 - dims[0] / 4
        points[0, 1] = dims[1] / 2
        points[1, 1] = dims[1] / 2
    elif num_points == 3:
        points[0:2, 0] = np.random.rand(2) * dims[0] / 4 - dims[0] / 4
        points[0, 1] = dims[1] / 2
        points[1, 1] = dims[1] / 2
        points[2, 0] = np.random.choice([-1, 1]) * dims[0] / 2
        points[2, 1] = np.random.rand() * dims[1] / 4 - dims[1] / 4
    else:
        lengths = [dims[0], dims[1], dims[0], dims[1]]
        xVal = [-dims[0] / 2, dims[0] / 2, dims[0] / 2, -dims[0] / 2]
        yVal = [-dims[1] / 2, -dims[1] / 2, dims[1] / 2, dims[1] / 2]
        startPos = np.random.rand() * pointDist
        xFac = [1, 0, -1, 0]
        yFac = [0, 1, 0, -1]
        numCounter = 0

        for i in range(np.min((4, num_points))):
            numAxisPoints = 1 + int((lengths[i] - startPos) / pointDist)
            axisPoints = startPos + np.arange(numAxisPoints) * pointDist
            distLeft = lengths[i] - axisPoints[-1]
            points[numCounter : numCounter + numAxisPoints, 0] = (
                xVal[i] + xFac[i] * axisPoints
            )
            points[numCounter : numCounter + numAxisPoints, 1] = (
                yVal[i] + yFac[i] * axisPoints
            )
            numCounter += numAxisPoints
            startPos = pointDist - distLeft

    return points