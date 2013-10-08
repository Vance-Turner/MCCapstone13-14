#######################################################################
# Geometry construction and meshing creation for a typical
# 2d channel flow between two infinite parallel plates.
#
# Written by: salad
# Manchester, UK
# 06/02/2010
# Modified by: Vance Turnewitsch
# This script creates a simple cone shape by extruding a circle in the x-axis.
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

duct_length = 100 * unit
duct_radius = 10 * unit
#
# basic coordinate
#
p0 = MakeVertex(0, 0, 0)
p1 = MakeVertex(duct_length,0,0)
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
# build base circle
base_circle = MakeCircle(p0,dx,duct_radius)

# build face
f_duct = MakeFace(base_circle, 1)

# extrude along the z axis
v_duct = MakePrismVecH(f_duct, dx, duct_length)
addToStudy(v_duct, "v_duct")

print "channel geometry constructed..."

# FACE groups definition:
# 1. inlet
# 2. outlet
# 5. sym

# sym is declared and filled
sub_faces = SubShapeAllSorted(v_duct, ShapeType["FACE"])
g_sym = CreateGroup(v_duct, ShapeType["FACE"])
UnionList(g_sym, sub_faces)

# inlet
# Get's all the faces that have the normal dx and GEOM.ST_ON is a shape on the surface
sub_faces = GetShapesOnPlane(v_duct, ShapeType["FACE"], dx, GEOM.ST_ON)
g_inlet = CreateGroup(v_duct, ShapeType["FACE"])
# Adds to the group g_inlet all the faces in sub_faces
UnionList(g_inlet, sub_faces)
# Removes all the sym group (g_sym) all the faces in sub_faces. These are the faces in the x-plane
DifferenceList(g_sym, sub_faces)

# Seems to add the group to the "father" v_duct.
addToStudyInFather(v_duct, g_inlet, "inlet")

# outlet
# Get all the shapes with the normal dx and the location p1 which is the end of our cylinder
sub_faces = GetShapesOnPlaneWithLocation(v_duct, ShapeType["FACE"], dx, p1, GEOM.ST_ON)

g_outlet = CreateGroup(v_duct, ShapeType["FACE"])
UnionList(g_outlet, sub_faces)
DifferenceList(g_sym, sub_faces)

addToStudyInFather(v_duct, g_outlet, "outlet")

# sym is finally obtained
addToStudyInFather(v_duct, g_sym, "sym")

print "FACE groups defined..."

# EDGE groups definition:
# 1. let (inlet & outlet of the channel)
# 2. tb (top & bottom of the channel)
# 3. extru (the extrusion length)

# let
print("Trying to get edges with height")
g_circum = GetEdgesByLength(v_duct, 2*pi*duct_radius, 2*pi*duct_radius, 1, 1)
addToStudyInFather(v_duct,g_circum,"circum")

print("Trying to get length edges")
g_length = GetEdgesByLength(v_duct, duct_length, duct_length, 1, 1)
addToStudyInFather(v_duct, g_length, "length")

print "EDGE groups defined..."

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
# This says take all the edges and divide them into one segment.
algo1d = mesh_d.Segment()
algo1d.NumberOfSegments(1)

# structured rectangular mesh is preferred for 2D faces
# This says once we get into the 2D mesh, divide things into quadrangles which are things that have four sides, but
# not necessarily squares.
algo2d_2 = mesh_d.Triangle()
#algo2d.TrianglePreference()#QuadranglePreference()

# This says when we get into 3D, divide things into hexahedrons which are things that have six sides.
algo3d = mesh_d.Tetrahedron()#Hexahedron()

# submesh

# for inlet & outlet, use parabolic mesh density profile
# but with Vance's changes g_let is just the inlet now!
algo1d_let = mesh_d.Segment(g_circum)
seg = algo1d_let.NumberOfSegments(50)
#seg.SetDistrType(3)
#seg.SetConversionMode(1)
#seg.SetExpressionFunction('(t-0.5)^2+0.1')

# for top & bottom, use a decreasing profile from the inlet to the outlet
algo1d_tb = mesh_d.Segment(g_length)
seg = algo1d_tb.NumberOfSegments(250)
#seg.SetDistrType(3)
#seg.SetConversionMode(0)
#seg.SetExpressionFunction('(t-1)^4+0.1')

import geompy
sub_faces = geompy.SubShapeAllSortedCentres(v_duct,geompy.ShapeType["FACE"])
print(len(sub_faces))
sub_faces = sub_faces[1]
print("Subfaces:",sub_faces)#GetShapesOnPlane(v_duct, ShapeType["FACE"], dx, GEOM.ST_ON)
algo2d = mesh_d.Quadrangle(geom=sub_faces)

status = mesh_d.Compute()

print "mesh computed..."

#
# mesh groups
#

mesh_d.GroupOnGeom(g_inlet, "inlet")
mesh_d.GroupOnGeom(g_outlet, "outlet")
mesh_d.GroupOnGeom(g_sym, "sym")

print "mesh groups defined..."

# update

salome.sg.updateObjBrowser(1)
