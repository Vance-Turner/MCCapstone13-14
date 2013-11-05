# Automates my process...
import importscript
import os
import sys
sys.path.append(os.path.join("/","home","vance","Capstone13-14","MCCapstone13-14","pythonlib",""))
import salome
salome.salome_init()
from windmc.modelling import mesh
from windmc.modelling import geom

points = [(10,10),(20,13),(30,16)]
'''
cylinder = mesh.SectionedCylinder(points,8)
cylinder.generateMesh([])
'''
windTunnel = geom.BasicWindTunnel("WindTunnel",points,10,3,50,60,0,0,0)
windTunnel.doGeom()
windTunnel.doMesh()
salome.sg.updateObjBrowser(1)
print("Mesh calculated...now exporting...")
windTunnel.export("wind_tunnel2.med")
