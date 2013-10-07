#######################################################################
# Geometry construction and meshing creation for a typical
# 2d channel flow between two infinite parallel plates.
#
# Written by: salad
# Manchester, UK
# 06/02/2010
#######################################################################
import os
import sys
import salome
from math import *
from geompy import *
import copy

# basic unit
unit = 0.001
# extrusion length
extru = unit

duct_height = unit * 5
duct_length = unit * 100
duct_y_addition = unit * 2
#
# basic coordinate
#
p0 = MakeVertex(0, 0, 0)
dx = MakeVectorDXDYDZ(unit, 0, 0)
dy = MakeVectorDXDYDZ(0, unit, 0)
dz = MakeVectorDXDYDZ(0, 0, unit)
addToStudy(p0, "p0")
addToStudy(dx, "dx")
addToStudy(dy, "dy")
addToStudy(dz, "dz")

print "basic coordinate built..."

#
# geometry construction
#

# points
p1 = MakeVertex(duct_length, -duct_y_addition, 0)
p2 = MakeVertex(0, duct_height, 0)
p3 = MakeVertex(duct_length, duct_height+duct_y_addition, 0)

# build edges
e0 = MakeEdge(p0, p1)
e1 = MakeEdge(p2, p3)
e2 = MakeEdge(p0, p2)
e3 = MakeEdge(p1, p3)

# build face
f_duct = MakeFaceWires([e0, e1, e2, e3], 1)

# extrude along the z axis
v_duct = MakePrismVecH(f_duct, dz, extru)
addToStudy(v_duct, "v_duct")

print "channel geometry constructed..."

# FACE groups definition:
# 1. inlet
# 2. outlet
# 3. bottom
# 4. top
# 5. sym

# sym is declared and filled
sub_faces = SubShapeAllSorted(v_duct, ShapeType["FACE"])
g_sym = CreateGroup(v_duct, ShapeType["FACE"])
UnionList(g_sym, sub_faces)

# inlet
# Get's all the faces that have the normal dx and GEOM.ST_ON is a shape on the surface
sub_faces = GetShapesOnPlane(v_duct, ShapeType["FACE"], dx, GEOM.ST_ON)
print("We have",sub_faces," in the normal x direction");
g_inlet = CreateGroup(v_duct, ShapeType["FACE"])
# Adds to the group g_inlet all the faces in sub_faces
UnionList(g_inlet, sub_faces)
# Removes all the sym group (g_sym) all the faces in sub_faces. These are the faces in the x-plane
DifferenceList(g_sym, sub_faces)

# Seems to add the group to the "father" v_duct.
addToStudyInFather(v_duct, g_inlet, "inlet")

# outlet
# Get all the shapes with the normal dx and the location p1 which is the lower right
# vertex of our 2D geometry.
sub_faces = GetShapesOnPlaneWithLocation(v_duct, ShapeType["FACE"], dx, p1, GEOM.ST_ON)

g_outlet = CreateGroup(v_duct, ShapeType["FACE"])
UnionList(g_outlet, sub_faces)
DifferenceList(g_sym, sub_faces)

addToStudyInFather(v_duct, g_outlet, "outlet")

# bottom
sub_faces = GetShapesOnPlane(v_duct, ShapeType["FACE"], dy, GEOM.ST_ON)

g_bottom = CreateGroup(v_duct, ShapeType["FACE"])
UnionList(g_bottom, sub_faces)
DifferenceList(g_sym, sub_faces)

addToStudyInFather(v_duct, g_bottom, "bottom")

# top
sub_faces = GetShapesOnPlaneWithLocation(v_duct, ShapeType["FACE"], dy, p2, GEOM.ST_ON)

g_top = CreateGroup(v_duct, ShapeType["FACE"])
UnionList(g_top, sub_faces)
DifferenceList(g_sym, sub_faces)

addToStudyInFather(v_duct, g_top, "top")

# sym is finally obtained
addToStudyInFather(v_duct, g_sym, "sym")

print "FACE groups defined..."

# EDGE groups definition:
# 1. let (inlet & outlet of the channel)
# 2. tb (top & bottom of the channel)
# 3. extru (the extrusion length)

# let
print("Trying to get edges with height")
g_let = GetEdgesByLength(v_duct, duct_height+(2*duct_y_addition), duct_height+(2*duct_y_addition), 1, 1)
addToStudyInFather(v_duct, g_let, "let")
import math
# tb
print("Trying to get length edges")
g_tb = GetEdgesByLength(v_duct, math.sqrt(duct_length**2+duct_y_addition**2)-(duct_length*0.1), math.sqrt(duct_length**2+duct_y_addition**2)+(duct_length*0.1), 1, 1)
addToStudyInFather(v_duct, g_tb, "tb")

# extru
print("Trying to get extrusion edges")
g_extru = GetEdgesByLength(v_duct, extru, extru, 1, 1)
addToStudyInFather(v_duct, g_extru, "extru")

print "EDGE groups defined..."
'''
#
# meshing
#
import smesh
import StdMeshers

# Creates, I think an smeshDC instance
mesh_d = smesh.Mesh(v_duct, "mesh_d")

print "prepare for meshing..."

# construction of mesh

# as default, a 1D edge is meshed with only 1 cell
# it is for the extrusion length
algo1d = mesh_d.Segment()
algo1d.NumberOfSegments(1)

# structured rectangular mesh is preferred for 2D faces
algo2d = mesh_d.Quadrangle()
algo2d.QuadranglePreference()

algo3d = mesh_d.Hexahedron()

# submesh

# for inlet & outlet, use parabolic mesh density profile
algo1d_let = mesh_d.Segment(g_let)
seg = algo1d_let.NumberOfSegments(50)
seg.SetDistrType(3)
seg.SetConversionMode(1)
seg.SetExpressionFunction('(t-0.5)^2+0.1')

# for top & bottom, use a decreasing profile from the inlet to the outlet
algo1d_tb = mesh_d.Segment(g_tb)
seg = algo1d_tb.NumberOfSegments(250)
seg.SetDistrType(3)
seg.SetConversionMode(0)
seg.SetExpressionFunction('(t-1)^4+0.1')

status = mesh_d.Compute()

print "mesh computed..."

#
# mesh groups
#

mesh_d.GroupOnGeom(g_inlet, "inlet")
mesh_d.GroupOnGeom(g_outlet, "outlet")
mesh_d.GroupOnGeom(g_bottom, "bottom")
mesh_d.GroupOnGeom(g_top, "top")
mesh_d.GroupOnGeom(g_sym, "sym")

print "mesh groups defined..."
'''
# update
salome.sg.updateObjBrowser(1)
