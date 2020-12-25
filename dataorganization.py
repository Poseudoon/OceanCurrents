"""
reads data and calculates
"""

import os.path
import numpy as np
#from geopy import distance


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
    """

    deccords = []
    distance = []
    lats = []
    lons = []
    depths = []
    uvelocs = np.array([])
    vvelocs = np.array([])
    maxveloc = 0

    for datanumber in datarange:
        if datanumber == 40:
            continue
        else:
            lat, lon, currentdata = datareader(datanumber)
            depth = np.transpose(currentdata)[0]
            uveloc = np.transpose(currentdata)[1]
            vveloc = np.transpose(currentdata)[2]
            depths.append(depth)
            np.append(vvelocs, np.array(vveloc), axis=0)
            np.append(uvelocs, uveloc, axis=0)
            lats.append(lat.split(" "))
            lons.append(lon.split(" "))

            if len(vveloc) > maxveloc:
                maxveloc = len(vveloc)

    print("vveloc: ", np.array(vveloc))

    for i in range(0, len(datarange)):
        lats[i][0] = lats[i][0].strip("°N")
        lons[i][0] = lons[i][0].strip("°W")
        lats[i][1] = lats[i][1].strip("'\n")
        lons[i][1] = lons[i][1].strip("'\n")

        declat = float(lats[i][0]) + float(lats[i][1]) / 60
        declon = float(lons[i][0]) + float(lons[i][1]) / 60
        deccords.append((declat, declon))

#        if len(vvelocs[i]) < maxveloc:
#            difference = maxveloc - len(vvelocs[i])

    for i in range(0, len(datarange)-1):
        distance.append(np.sqrt(((deccords[i+1][0] - deccords[i][0]) ** 2 + (deccords[i+1][1] - deccords[i][1]) ** 2)))
        print(distance[i])
        distance[i] = 2 * np.pi * 6371000 * distance[i] / 360

    return depths, uvelocs, vvelocs, distance


def interpolator(mat, distance):
    """
        Interpoltes the matrix mat and returns the matrix with steady steps.
    """

    gesdistance = np.zeros(len(distance))
    gesdistance[0] = distance[0]
    gesdis = distance[0]
    for i in range(1, len(distance)):
        gesdistance[i] = gesdistance[i-1] + distance[i]
        gesdis = gesdis + distance[i]

    for wth in range(1, mat.size/len(mat)-1):
        for leng in range(len(mat)):
            xmed = wth*gesdis/len(mat)
            if gesdistance[wth-1] < wth*xmed:
                newmat[wth, leng] = (1-(wth*xmed - gesdistance[wth])/(wth*xmed-gesdistance[wth]+wth*xmed-gesdistance[wth+1]))


ds, us, vs, dcs = dataconverter((31, 32, 33, 34, 35, 38))
print("depths:", ds)
#print("len(depths): ", w(ds))
print("uvelocs:", us)
print("uvelocs2:", vs)
print("distance:", dcs)