"""
reads data and calculates
"""

import os.path
import numpy as np


def datareader(datanumber):
    """Reads the latidude, longitude, currentdata from dataname
    Args: dataname is the name of the .lad-file wich data is to be read

    Returns: latitude(lat), longitude(lon), depth with velocities(currentdata)
    """

    dataname = "0{number}.lad".format(number=datanumber)
    fp = open(os.path.join("measurements", dataname))
    readdata = fp.readlines()
    fp.close

    lat = readdata[3].strip("Start_Lat   = ")
    lon = readdata[4].strip("Start_Lon   = ")
    currentdata = readdata[7:]

    for i in range(0, len(currentdata)):
        currentdata[i] = currentdata[i].strip(" \n").split()
        for j in range(0, 4):
            currentdata[i][j] = float(currentdata[i][j])

    return lat, lon, currentdata


def dataconverter(datarange):
    """Converts data from datareader into usable data for contourplot
    Args: datarange: the indices from the data files wich data
                     is to be extracted
    """
# define value arrays
    deccords = []
    distance = []
    lats = []
    lons = []
    uvelocs = []
    vvelocs = []
    maxveloc = 0

# save data from datarange in value arrays
    for datanumber in datarange:
        if datanumber == 40:
            continue
        else:
            lat, lon, currentdata = datareader(datanumber)
            uveloc = np.transpose(currentdata)[1]
            vveloc = np.transpose(currentdata)[2]

            vvelocs.append(vveloc.tolist())
            uvelocs.append(uveloc.tolist())
            lats.append(lat.split(" "))
            lons.append(lon.split(" "))
# find velocity array with most items
            if len(vveloc) > maxveloc:
                maxveloc = len(vveloc)
                maxdepth = np.transpose(currentdata)[0]


# convert coordinates to decimal degree
    for i in range(0, len(datarange)-1):
        lats[i][0] = lats[i][0].strip("°N")
        lons[i][0] = lons[i][0].strip("°W")
        lats[i][1] = lats[i][1].strip("'\n")
        lons[i][1] = lons[i][1].strip("'\n")

        declat = float(lats[i][0]) + float(lats[i][1]) / 60
        declon = float(lons[i][0]) + float(lons[i][1]) / 60
        deccords.append((declat, declon))


# fill short velocity arrays with filler constants (ground)
        if len(vvelocs[i]) < maxveloc:
            difference = maxveloc - len(vvelocs[i])
            vvelocs[i] = np.append(np.array(vvelocs[i]),
                                   (np.ones(difference) * -2))
            uvelocs[i] = np.append(np.array(uvelocs[i]),
                                   (np.ones(difference) * -2))
    declons = [deccords[0][1], deccords[-1][1]]
    uvelocys = np.transpose(uvelocs)
    vvelocys = np.transpose(vvelocs)

# calculate distance between measurement points
    for i in range(0, len(datarange)-2):
        distance.append(np.sqrt(((deccords[i+1][0] - deccords[i][0]) ** 2 +
                                 (deccords[i+1][1] - deccords[i][1]) ** 2)))
        distance[i] = 2 * np.pi * 6371000 * distance[i] / 360

    return maxdepth[-1], uvelocys, vvelocys, distance, declons
