# Automates my process...
import importscript
import os
import sys
sys.path.append(os.path.join("/","home","vance","Capstone13-14","MCCapstone13-14","pythonlib",""))
import salome
salome.salome_init()
from windmc.modelling import mesh
points = []
for in xrange(6):
	points.append([(i*5,i**2)])
cylinder = mesh.SectionedCylinder(points,1)
cylinder.generateMesh([])
salome.sg.updateObjBrowser(1)
