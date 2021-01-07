"""
    interppolates the matrix veloc and plot a contourplot
"""

import numpy as np
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
    for wdth in range(int(gesdis/mini)):
        newvelocdepth = interp1d(np.append(np.arange(0, 458, 20), 458), np.append(newmat[::20, wdth], newmat[457, wdth]), kind="linear")
        for le in range(len(newmat)):
            newmat[le, wdth] = newvelocdepth(le)

    return np.flip(newmat), gesdis


def conplot(veloc, direction, maxdepth, lons, volumes):

    plt.title("Velocity and volume transport", fontsize=22)
    plt.rcParams["figure.figsize"] = [9, 11]
    plt.xlim(0, int(veloc.size/len(veloc)))
    if direction == "u":
        cs = plt.contourf(veloc, levels=np.arange(-0.4, 0.85, 0.01),
                          cmap="jet", extend='both')
    else:
        cs = plt.contourf(veloc, levels=np.arange(-0.75, 0.6, 0.01),
                          cmap="jet", extend='both')
    plt.plot(np.linspace(0, len(volumes)-1, len(volumes)), volumes/45000-200, linewidth=3)
    plt.plot([0, len(volumes)-1], [-200, -200], linewidth=2, color="grey")
    plt.colorbar(cs).ax.tick_params(labelsize=15)
    cs.cmap.set_under('grey')
    plt.xticks([(lons[1]-44)*int(veloc.size/len(veloc))/(lons[1]-lons[0]), (lons[1]-42)*int(veloc.size/len(veloc))/(lons[1]-lons[0]), (lons[1]-40)*int(veloc.size/len(veloc))/(lons[1]-lons[0]), (lons[1]-38)*int(veloc.size/len(veloc))/(lons[1]-lons[0]), (lons[1]-36)*int(veloc.size/len(veloc))/(lons[1]-lons[0])], ["44°", "42°", "40°", "38°", "36°"], fontsize=15)
    plt.yticks([-5000/45-200, -2500/45-200, -200, 2500/45-200, 5000/45-200, 458-4000*458/maxdepth, 458-3000*458/maxdepth, 458-2000*458/maxdepth, 458-1000*458/maxdepth, 458], [-5, -2.5, 0, 2.5, 5, -4000, -3000, -2000, -1000, 0], fontsize=15)
    plt.text(300, 100, "Velocity in [m/s], N-S", fontsize=18, rotation=270)
    plt.xlabel("West-Longitude", fontsize=20)
    plt.text(-55, 300, "Depth in [m]", fontsize=20, rotation=90)
    plt.text(-55, 0, "Volume transport in [SV] pro 4310m", fontsize=20, rotation=90)
    plt.show()


def volumeplot(volumes, errors):
    plt.title("Volume transport between each meassurement", fontsize=22)
    plt.scatter(np.linspace(0, len(volumes)-1, len(volumes)), volumes)
    plt.errorbar(np.linspace(0, len(volumes)-1, len(volumes)), volumes, yerr=errors)
    plt.plot([0, len(volumes)-1], [0, 0], linewidth=2, color="grey")
    plt.show
