"""
    interppolates the matrix veloc and plot a contourplot
"""

import numpy as np
import matplotlib.mlab as ml
from scipy.interpolate import interp1d
from matplotlib import pyplot as plt


def interpolator(mat, distance):
    """
        Interpoltes the matrix mat and returns the matrix newmat with steady
        steps in distance of the smallest distance.
    """

# calculate the place of each meassurement relative to the whole yourney of the
# ship
    gesdistance = np.zeros(len(distance)+1)
    gesdis = distance[0]
    for i in range(1, len(distance)+1):
        gesdistance[i] = gesdistance[i-1] + distance[i-1]
        if i < len(distance):
            gesdis = gesdis + distance[i]

# calculates the minimum distance for number of points of the interpolation
    mini = distance[0]
    for i in range(len(distance)):
        if distance[i] < mini:
            mini = distance[i]

# interpolates linear over every depth
    newmat = np.zeros((len(mat), int(gesdis/mini)))

    wth = 0
    for leng in range(len(newmat)):
        newveloc = interp1d(gesdistance, mat[leng, :], kind="linear")
        for wth in range(int(gesdis/mini)):
            newmat[leng, wth] = newveloc(wth*mini)
    return np.flip(newmat)


def conplot(veloc, direction):

#    plt.xlim(0, 278)
    if direction == "u":
        cs = plt.contourf(veloc, levels=np.arange(-0.4, 0.85, 0.01),
                          cmap="jet", extend='both')
    else:
        cs = plt.contourf(veloc, levels=np.arange(-0.75, 0.6, 0.01),
                          cmap="jet", extend='both')
    plt.colorbar(cs)
    cs.cmap.set_under('grey')
#    cs.changed()
    plt.axis()
    plt.show()
