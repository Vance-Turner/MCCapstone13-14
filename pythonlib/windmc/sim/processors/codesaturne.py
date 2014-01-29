__author__ = 'vance'

import os
import csv
import re
import json, StringIO
import pandas as pd
import numpy as np

def parsePiece(string, start, end, returnInt=True):
    theStr = string[start:end]
    if returnInt:
        return int(theStr)
    else:
        return theStr

def getRecentRESUDir(resuPath):
    """
    This function returns the directory name with the most recent results created by a code-saturne simulation.
    resuPath -- The absolute path to the RESU direction of a code-saturne case. The directories within this
    directory will be searched to find the one with the most recent results.
    """
    '''
    This function works by the following process: directories within the RESU directory are named according to the
    following scheme by code-saturne:{year}{month}{day}-{number}.The month and day are two digit codes. The function
    simply parses each directory name and searches for the most recent one.
    '''
    direcs = os.listdir(resuPath)
    # Parse for years.
    year = 0
    for direc in direcs:
        if re.match('\A[0-9]{8}[-][0-9]+',direc) and parsePiece(direc,0,4) > int(year):
            year = parsePiece(direc,0,4,False)
    #print "Got year:",year
    # Now get largest month
    month = 0
    for direc in direcs:
        if re.match('\A[0-9]{8}[-][0-9]+',direc) and parsePiece(direc,4,6) > int(month):
            month = parsePiece(direc,4,6,False)
    #print "Got month:",month
    # Now get the largest day
    day = 0
    for direc in direcs:
        if re.match('\A[0-9]{8}[-][0-9]+',direc) and parsePiece(direc,6,8) > int(day):
            day = parsePiece(direc,6,8,False)
    #print "Got day:",day
    largestDate = str(year)+str(month)+str(day)
    #print "The largest date:",largestDate
    numCode = 0
    for direc in direcs:
        #print "testing:",direc
        if re.match('\A[0-9]{8}[-][0-9]+',direc) and direc[0:8]==largestDate and parsePiece(direc,9,len(direc)) > int(numCode):
            numCode = parsePiece(direc,9,len(direc),False)
    print "Code-saturne post processing, using directory:",str(largestDate+'-'+numCode)
    return largestDate+'-'+str(numCode)

def processNumber(text):
    # Now process the number
    parts = text.split("e")
    base = float(parts[0])
    exp = float(parts[1])
    return base * (10 ** exp)


def getInletOutletVelocity(resultsPath):
    '''
    This function gets the velocity at the monitoring points 1,2 which should be the inlet and outlet of the tunnel.
    '''
    # Get the path to the postprocessing folder
    postProcPath = os.path.join(resultsPath,getRecentRESUDir(resultsPath),'monitoring')
    probesVelXFilePath = os.path.join(postProcPath,'probes_VelocityX.csv')
    probesVelYFilePath = os.path.join(postProcPath,'probes_VelocityY.csv')
    probesVelZFilePath = os.path.join(postProcPath,'probes_VelocityZ.csv')
    '''
    We no longer use this manual processing, instead let's use PANDAS
    with open(probesVelXFilePath,'rb') as probesVelX:
        csvread = csv.reader(probesVelX,delimiter=',')
        # Now get the last line
        firstRow = csvread.next()
        inletIndex = 0
        outletIndex = 0
        for row in csvread:
            pass
        # Now computer average inlet and average outlet velocities
        totalInlet = 0
        for i in range(1,43):
            totalInlet += processNumber(row[i])
        averageInlet = totalInlet/42
        totalOutlet = 0
        for i in range(43,85):
            totalOutlet += processNumber(row[i])
        averageOutlet = totalOutlet/42
        print "The average inlet and outlet velocities are:",averageInlet,averageOutlet
    '''
    # Get the data frames
    dfx = pd.read_csv(probesVelXFilePath)
    dfy = pd.read_csv(probesVelYFilePath)
    dfz = pd.read_csv(probesVelZFilePath)

    # Get the rows we are concerned with
    row9x = dfx[9:10]
    row9y = dfy[9:10]
    row9z = dfz[9:10]

    # Now start processing probe groups
    # inlet probes 1-12
    probe1 = (row9x.icol(slice(1,13))**2 + row9y.icol(slice(1,13))**2 + row9z.icol(slice(1,13))**2).apply(np.sqrt).mean(axis=1)[9]

    # next probe at x=30 probes 1-12
    probe2 = (row9x.icol(slice(13,25))**2 + row9y.icol(slice(13,25))**2 + row9z.icol(slice(13,25))**2).apply(np.sqrt).mean(axis=1)[9]

    # next probe at x=60 probes 25-37
    probe3 = (row9x.icol(slice(25,37))**2 + row9y.icol(slice(25,37))**2 + row9z.icol(slice(25,37))**2).apply(np.sqrt).mean(axis=1)[9]

    # next probe at x=95 probes 1-12, the outlet
    probe4 = (row9x.icol(slice(37,49))**2 + row9y.icol(slice(37,49))**2 + row9z.icol(slice(37,49))**2).apply(np.sqrt).mean(axis=1)[9]

    # next probe at x=49 probes 1-12, just before actuator disk
    probe5 = (row9x.icol(slice(49,65))**2 + row9y.icol(slice(49,65))**2 + row9z.icol(slice(49,65))**2).apply(np.sqrt).mean(axis=1)[9]

    # next probe at x=50.05 probes 1-12, in the middle of the actuator disk
    probe6 = (row9x.icol(slice(65,81))**2 + row9y.icol(slice(65,81))**2 + row9z.icol(slice(65,81))**2).apply(np.sqrt).mean(axis=1)[9]

    # next probe at x=50.05 probes 1-12, just beyond the actuator disk
    probe7 = (row9x.icol(slice(81,97))**2 + row9y.icol(slice(81,97))**2 + row9z.icol(slice(81,97))**2).apply(np.sqrt).mean(axis=1)[9]

    dict = {'probe1':probe1,'probe2':probe2,'probe3':probe3,'probe4':probe4,'probe5':probe5,'probe6':probe6,'probe7':probe7,}
    print "Post-processing>",dict
    return dict

def __twoColumnProcessor__(path, upStreamVelocColumn=1, downStreamVelocColumn=2):
    """
    The points we are interested are the velocity at (x,y,z)=(startX,0,0) and (x,y,z)=(endX,0,0)
    """
    datFile = file(path, 'r')
    # We ignore all lines that start with #
    # These
    previousLine = ""
    for line in datFile:
        if line[0] == "#":
            # ignore such lines
            pass
        previousLine = line

    #print "Previous line>", previousLine
    # Ok, now we have the last line of data, there are three spaces at the beginning
    pieces = previousLine.split("  ")
    #print "Previous line pieces>", pieces
    upStreamVeloc = pieces[upStreamVelocColumn + 1]
    downStreamVeloc = pieces[downStreamVelocColumn + 1]

    # Now process the number
    parts = upStreamVeloc.split("e")
    base = float(parts[0])
    exp = float(parts[1])
    upStreamVeloc = base * (10 ** exp)

    parts = downStreamVeloc.split("e")
    base = float(parts[0])
    exp = float(parts[1])
    downStreamVeloc = base * (10 ** exp)
    datFile.close()
    return [upStreamVeloc, downStreamVeloc]

if __name__=='__main__':
    #print "In testing code-saturne processors..."
    resuDir = raw_input("Enter results directory path:")
    if os.path.exists(resuDir):
        print getRecentRESUDir(resuDir)
    else:
        print "That path doesn't exist!"
