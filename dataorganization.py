"""
reads data and calculates
"""

import os.path
import numpy as np
from scipy.interpolate import interp1d


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
    depths = []
    uvelocs = []
    vvelocs = []
    maxveloc = 0

# save data from datarange in value arrays
    for datanumber in datarange:
        if datanumber == 40:
            continue
        else:
            lat, lon, currentdata = datareader(datanumber)
# depth = np.transpose(currentdata)[0]
            uveloc = np.transpose(currentdata)[1]
            vveloc = np.transpose(currentdata)[2]

            vvelocs.append(vveloc.tolist())
            uvelocs.append(uveloc.tolist())
            lats.append(lat.split(" "))
            lons.append(lon.split(" "))

# find velocity array with most items
            if len(vveloc) > maxveloc:
                maxveloc = len(vveloc)


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
                                   (np.ones(difference) * -1000))
            uvelocs[i] = np.append(np.array(uvelocs[i]),
                                   (np.ones(difference) * -1000))
    uvelocys = np.transpose(uvelocs)
    vvelocys = np.transpose(vvelocs)

# calculate distance between measurement points
    for i in range(0, len(datarange)-2):
        distance.append(np.sqrt(((deccords[i+1][0] - deccords[i][0]) ** 2 +
                                 (deccords[i+1][1] - deccords[i][1]) ** 2)))
        distance[i] = 2 * np.pi * 6371000 * distance[i] / 360

    return depths, uvelocys, vvelocys, distance


def interpolator(mat, distance):
    """
        Interpoltes the matrix mat and returns the matrix newmat with steady
        steps in distance of the smallest distance.
    """

# calculate the place of each meassurement relative to the whole yourney of the
# ship
    gesdistance = np.zeros(len(distance)+1)
    gesdis = distance[0]
    print("wdth: ", mat.size/len(mat))
    print("length: ", len(mat))
    print("mat: ", mat[0, :])
    print("gesdistance: ", gesdistance[0])
    for i in range(1, len(distance)+1):
        gesdistance[i] = gesdistance[i-1] + distance[i-1]
        if i < len(distance):
            gesdis = gesdis + distance[i]
        print("gesdis: ", (i)*1205876/len(distance))
        print("gesdistance: ", gesdistance[i])

# calculates the minimum distance for number of points of the interpolation
    mini = distance[0]
    for i in range(len(distance)):
        if distance[i] < mini:
            mini = distance[i]

#
    newmat = np.zeros((len(mat), int(gesdis/mini)))

    point = -1
    wth = 0
    xmed = 0
    for leng in range(len(newmat)):
        print("mat: ", mat[leng, :-1])
        newveloc = interp1d(gesdistance, mat[leng, :], kind='cubic')
        for wth in range(int(gesdis/mini)):
            if gesdistance[point] <= xmed:
                point += 1
#            wth += 1
#            xmed = wth*gesdis/mini
#            print("length: ", leng)
#            print("width: ", wth)
#            print("punkt: ", wth*mini)
            newmat[leng, wth] = newveloc(wth*mini)
#        dminus = xmed-gesdistance[point-1]
#        delta = gesdistance[point]-xmed
#        for leng in range(len(newmat)):
#            newmat[wth, leng] = delta/(dminus+delta)*mat[point-1, leng]+dminus/(dminus+delta)*mat[point, leng]
"""
    for wth in range(1, mat.size/len(mat)-1):
        for leng in range(len(mat)):
            xmed = wth*gesdis/len(mat)
            if gesdistance[wth-1] < wth*xmed:
                newmat[wth, leng] = (1-(wth*xmed - gesdistance[wth])/(wth*xmed-gesdistance[wth]+wth*xmed-gesdistance[wth+1]))
"""

ds, us, vs, dcs = dataconverter(range(31, 54))
print("uvelocs:", us)
print("distances: ", dcs)
interpolator(us, dcs)
