"""
    interppolates the matrix veloc and plot a contourplot
"""

import numpy as np
from scipy.interpolate import interp1d
from matplotlib import pyplot as plt
from matplotlib import ticker as ti


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
    for wdth in range(int(gesdis/mini)):
        newvelocdepth = interp1d(np.append(np.arange(0, 458, 20), 458), np.append(newmat[::20, wdth], newmat[457, wdth]), kind="linear")
        for le in range(len(newmat)):
            newmat[le, wdth] = newvelocdepth(le)

    return np.flip(newmat)


def conplot(veloc, direction, maxdepth, lons):

    plt.xlim(0, 278)
    if direction == "u":
        cs = plt.contourf(veloc, levels=np.arange(-0.4, 0.85, 0.01),
                          cmap="jet", extend='both')
    else:
        cs = plt.contourf(veloc, levels=np.arange(-0.75, 0.6, 0.01),
                          cmap="jet", extend='both')
    plt.colorbar(cs)
    cs.cmap.set_under('grey')
    plt.xticks([(36-lons[0])*278/(lons[1]-lons[0]), (38-lons[0])*278/(lons[1]-lons[0]), (40-lons[0])*278/(lons[1]-lons[0]), (42-lons[0])*278/(lons[1]-lons[0]), (44-lons[0])*278/(lons[1]-lons[0])], ["36°", "38°", "40°", "42°", "44°"])
    plt.yticks([458-4000*458/maxdepth, 458-3000*458/maxdepth, 458-2000*458/maxdepth, 458-1000*458/maxdepth, 458], [-4000, -3000, -2000, -1000, 0])
    plt.text(350, 350, "velocity in m/s, N-S", fontsize=14, rotation=270)
    plt.xlabel("West-Longitude", fontsize=16)
    plt.ylabel("Depth in [m]", fontsize=16)
    plt.show()
