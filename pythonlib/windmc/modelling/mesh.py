import salome
import geompy
import smesh
import StdMeshers
from geompy import *
# This contains classes for generating meshes.
class BasicMesh:

	def __init__(self):
		pass
	
	def generateMesh(self,params):
		pass

	def doGeometry(self,params):
		pass

	def doEdges(self,params):
		pass

class SectionedCylinder(BasicMesh):

	'''
	The salomeStudy is the study that this object will be added to.
	The points list is a list of tuples that contains the radius of
	the cylinder at various locations along it.
	'''
	def __init__(self,points,baseRadius):
		BasicMesh.__init__(self)
		self.points = points
		self.sortPoints()
		#self.normalizePoints()
		self.baseRadius = baseRadius

	def sortPoints(self):
		# We will use the key method to sort the points
		print(self.points)
		self.points.sort(key=lambda point: point[0])

	def normalizePoints(self):
		# First, get the scale factor, which is just the
		# point that is the farthest from zero. 
		# TODO: We need to look into having shrowds that
		# start not from zero.
		maxNumber = max(self.points,key=lambda point:point[0])
		print "The maxNumber",maxNumber	
		self.points = map(lambda point: (point[0]/maxNumber[0],point[1]),self.points)
	
	def doGeometry(self,params):
		# First, create the wire which we will get our vertex info from.
		# Create the command string. For now, the path starts at 0,0
		# The cylinder will be centered at 0,0 for now.
		command = "Sketcher: F 0 0"
		for point in self.points:
			command += ":TT "+str(point[0])+" 0"
		print "The command path is:",command
		# This list with the 0,0,0,... is the origin, and the dz,dx coordinates
		self.extruWire = geompy.MakeSketcher(command, [0, 0, 0, 0, 0, 1, 1, 0, -0])

		# Now get the vertices of this wire and the edges. We use the vertices
		# as the center of the circles.
		centres = geompy.SubShapeAll(self.extruWire, geompy.ShapeType["VERTEX"])
		normal = geompy.MakeVectorDXDYDZ(0.001, 0, 0)
		
		# Build the circles for extrusion
		circles = []
		face_circles = []
		self.points.insert(0,(0,self.baseRadius))
		for i in xrange(len(centres)):
			print "Now creating circle:",str(i)
			circles.append(geompy.MakeCircle(centres[i],normal,self.points[i][1]))
			face_circles.append(geompy.MakeFace(circles[i],1))
		
		# Make the pipe!!
		self.pipeGeom = geompy.MakePipeWithDifferentSections(circles, centres, self.extruWire, 0, 0)

		# Now add them to the study
		for i in xrange(len(circles)):
			geompy.addToStudy(circles[i],"circle"+str(i))
		geompy.addToStudy(self.extruWire,"ExtrusionPath")
		geompy.addToStudy(self.pipeGeom,"PipeGeom")
		
	def doFaceGroups(self):
		dx = geompy.MakeVectorDXDYDZ(0.001,0,0)
		# FACE groups definition:
		# 1. inlet
		# 2. outlet
		# 5. sym

		# sym is declared and filled
		sub_faces = SubShapeAllSorted(self.pipeGeom, ShapeType["FACE"])
		print("The faces are:",sub_faces)
		self.g_sym = CreateGroup(self.pipeGeom, ShapeType["FACE"])
		UnionList(self.g_sym, sub_faces)

		# inlet
		# This for some reason returns a single shape instead of a list.		
		sub_faces = GetShapesNearPoint(self.pipeGeom,MakeVertex(-0.01,0,0),4,0.01)#GetShapesOnPlane(self.pipeGeom, ShapeType["FACE"], dx, GEOM.ST_ON)
		self.g_inlet = CreateGroup(self.pipeGeom, ShapeType["FACE"])
		# Adds to the group g_inlet all the faces in sub_faces
		UnionList(self.g_inlet, [sub_faces])
		# Removes all the sym group (g_sym) all the faces in sub_faces. These are the faces in the x-plane
		DifferenceList(self.g_sym, [sub_faces])

		# Seems to add the group to the "father" v_duct.
		geompy.addToStudyInFather(self.pipeGeom, self.g_inlet, "inlet")

		# outlet
		# Get all the shapes with the normal dx and the location p1 which is the end of our cylinder
		sub_faces = GetShapesNearPoint(self.pipeGeom,MakeVertex(self.points[-1][0],0,0),4,0.001)#GetShapesOnPlaneWithLocation(self.pipeGeom, ShapeType["FACE"], dx, MakeVertex(0,0,0), GEOM.ST_ON)

		self.g_outlet = CreateGroup(self.pipeGeom, ShapeType["FACE"])
		UnionList(self.g_outlet, [sub_faces])
		DifferenceList(self.g_sym, [sub_faces])

		addToStudyInFather(self.pipeGeom, self.g_outlet, "outlet")

		# sym is finally obtained
		addToStudyInFather(self.pipeGeom, self.g_sym, "sym")

		print "FACE groups defined..."
	def doEdges(self,params):
		pipeEdgeGroup = CreateGroup(self.pipeGeom, ShapeType["EDGE"])
		print("The original edges:",pipeEdgeGroup)
		self.circleEdges = []
		import math
		circleEdgeGroup = None
		for i in xrange(len(self.points)):
			circleEdges = GetEdgesByLength(self.pipeGeom,math.pi*self.points[i][1]*2,math.pi*self.points[i][1]*2*1.01,1,1)
			print(circleEdges)
			addToStudyInFather(self.pipeGeom,circleEdges,"circle"+str(i))
			self.circleEdges.append(circleEdges)
			circle_let = self.pipeMesh.Segment(circleEdges)
			seg = circle_let.NumberOfSegments(50)
			if circleEdgeGroup == None:
				circleEdgeGroup = circleEdges
			else:
				circleEdgeGroup = UnionGroups(circleEdgeGroup,circleEdges)
		print("The two groups are now:",pipeEdgeGroup,circleEdgeGroup)
		pipeEdgeGroup = CutGroups(pipeEdgeGroup,circleEdgeGroup)
		addToStudyInFather(self.pipeGeom,pipeEdgeGroup,"length")
		length_let = self.pipeMesh.Segment(pipeEdgeGroup)
		seg = length_let.NumberOfSegments(100)

	def generateMesh(self,params):
		self.doGeometry([])		
		self.doFaceGroups()
		self.pipeMesh = smesh.Mesh(self.pipeGeom,"mesh_d")
		self.doEdges([])
		self.basicMeshAlgo = self.pipeMesh.Segment()
		self.basicMeshAlgo.NumberOfSegments(1)
		self.triaMeshAlgo = self.pipeMesh.Triangle()
		self.tetraMeshAlgo = self.pipeMesh.Tetrahedron()
		sub_faces = geompy.SubShapeAllSortedCentres(self.pipeGeom,geompy.ShapeType["FACE"])
		sub_faces = sub_faces[1]
		algo2d = self.pipeMesh.Quadrangle(geom=sub_faces)
		status = self.pipeMesh.Compute()
	
		self.pipeMesh.GroupOnGeom(self.g_inlet,"inlet")
		self.pipeMesh.GroupOnGeom(self.g_outlet,"outlet")
		self.pipeMesh.GroupOnGeom(self.g_sym,"sym")
