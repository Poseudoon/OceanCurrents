"""
reads data and calculates
"""

import os.path
import numpy as np


def datareader(datanumber):
    """reads the latidude, longitude, data from dataname
    Args: dataname is the name of the .lad-file wich data is to be read

    Returns: latitude(lat), longitude(lon), and depth with velocities(data)
    """
    dataname = "0{number}.lad".format(number=datanumber)
    fp = open(os.path.join("processed", dataname))
    readdata = fp.readlines()
    fp.close

    lat = readdata[3].strip("Start_Lat   = ")
    lon = readdata[4].strip("Start_Lon   = ")
    data = readdata[7:]

    for i in range(0, len(data)):
        data[i] = data[i].strip(" \n").split()
        for j in range(0, 4):
            data[i][j] = float(data[i][j])

    return lat, lon, data
