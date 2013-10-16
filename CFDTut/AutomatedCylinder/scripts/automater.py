# Automates my process...
#import importscript
import os
import sys
sys.path.append(os.path.join("/","home","vance","Capstone13-14","MCCapstone13-14","pythonlib",""))
import salome
salome.salome_init()
from windmc.modelling import mesh
points = [(1,10),(2,13),(3,16)]
cylinder = mesh.SectionedCylinder(points,8)
cylinder.generateMesh([])
salome.sg.updateObjBrowser(1)
