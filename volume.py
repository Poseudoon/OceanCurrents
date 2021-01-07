"""
    Integrate the velocities
"""

import numpy as np


def integrator(mat, gesdis, maxdepth):
    """
        Calculates the Volume-transport
    """

    area = gesdis/mat.size*len(mat) * maxdepth/len(mat)
    volumes = np.zeros(int(mat.size/len(mat)))
    fullvolume = 0
    error = 0
    errors = np.zeros(int(mat.size/len(mat)))
    fullerror = 0
    for wdth in range(int(mat.size/len(mat))):
        volume = 0
        for leng in range(len(mat)):
            if mat[leng, wdth] > -0.76:
                volume += mat[leng, wdth]*area
                error += 0.02*area
                fullvolume += np.abs(volume)
                fullerror += error/np.sqrt(mat.size)
        volumes[wdth] = volume
        errors[wdth] = error/np.sqrt(len(mat))

    return volumes, fullvolume, errors, fullerror
