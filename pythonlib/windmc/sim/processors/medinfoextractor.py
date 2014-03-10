'''
Created on Mar 1, 2014

@author: vance
@summary: This file is to be used by salome to post-process a MED file to extract
pressure and velocity information at the inlet and disk location.
The WindMC library uses this file along with CodeSatPostProcessorCaller to build
a custom python processing file for each post-processing run. 
'''

import MEDLoader
import numpy as np
from MEDLoader import ON_CELLS

def extractPressure(tunnelWidth, actuatorX, actuatorRadius,inputFile,outputPath,outputID, diskPoints=30,radiusPoints=10):
    meshName = 'Fluid domain'
    pressureField = MEDLoader.MEDLoader_ReadField(ON_CELLS,inputFile,meshName,0,'Pressure',10,-1)
    angles = np.linspace(0.0,np.pi,diskPoints)
    magnitudes = np.linspace(0.25,actuatorRadius-0.1,radiusPoints)
    points = []
    values = []
    for mag in magnitudes:
        for angle in angles:
            point = [actuatorX,mag*np.cos(angle),mag*np.sin(angle)]
            print "Trying to get point on:",str(point)
            try:
                values.append(pressureField.getValueOn(point)[0])
                points.append(point)
            except:
                print "Was unable to get value at:",str(point)
    import csv
    import os
    with open(os.path.join(outputPath,outputID+'_pressure_.csv'),'wb') as csvfile:
        csvWriter = csv.writer(csvfile,delimiter=',',)
        csvWriter.writerow(points)
        csvWriter.writerow(values)
    print "Wrote pressure values"
    
def extractVelocity(crossSectionWidth,profileX,inputFile,outputPath,outputID,diskPoints=30,radiusPoints=10,component=0):
    meshName = 'Fluid domain'
    velocityField = MEDLoader.MEDLoader_ReadField(ON_CELLS,inputFile,meshName,0,'Velocity',10,-1)
    angles = np.linspace(0.0,np.pi,diskPoints)
    magnitudes = np.linspace(0.25,crossSectionWidth-0.1,radiusPoints)
    points = []
    values = []
    for mag in magnitudes:
        for angle in angles:
            point = [profileX,mag*np.cos(angle),mag*np.sin(angle)]
            print "Trying to get point on:",str(point)
            try:
                values.append(velocityField.getValueOn(point)[component])
                points.append(point)
            except:
                print "Was uanble to get velocity at:",str(point)
    import csv
    import os
    with open(os.path.join(outputPath,outputID+'_velocity_.csv'),'wb') as csvfile:
        csvWriter = csv.writer(csvfile,delimiter=',',)
        csvWriter.writerow(points)
        csvWriter.writerow(values)
    print "Wrote velocity values"