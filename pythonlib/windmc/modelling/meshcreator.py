__author__ = 'vance'

'''
This script contains functions for creating various mesh files. We unfortunately cannot call
the mesh script creation files directly ourselves because salome libraries aren't really
available to be imported. Thus we must use the runSalomeScript bash file.
'''

from windmc.sim.tasks import salomeInstallLocation
import os

def createWindTunnelSansShroud(outputPath,diskX=50.0,diskY=0.0,diskZ=0.0,diskHeight=0.1,diskRadius=4.0,tunnelHeight=100.0,tunnelRadius=40.0):
    scriptName = os.path.join(salomeInstallLocation,'runSalomeScript')
    subprocess.call(['sbatch',os.path.join(scriptName,'DATA','doSaturne.sh')])