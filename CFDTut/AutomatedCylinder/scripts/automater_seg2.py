# Automates my process...
import importscript
import os
import sys
sys.path.append(os.path.join("/","home","vance","Capstone13-14","MCCapstone13-14","pythonlib",""))
import salome
salome.salome_init()
from windmc.modelling import mesh
points = [(1,4),(5,10),(10,20)]
print points
cylinder = mesh.SectionedCylinder(points,5**2)
cylinder.generateMesh([])
salome.sg.updateObjBrowser(1)
print("Mesh calculated...now exporting...")
cylinder.export("mesh_export.med")

