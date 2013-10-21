import salome
import geompy
import math
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
		
		print("Just added these many circles:",len(face_circles))
		# Make the pipe!!
		self.pipeGeom = geompy.MakePipeWithDifferentSections(circles, centres, self.extruWire, 0, 0)

		# Now add them to the study
		for i in xrange(len(circles)):
			geompy.addToStudy(circles[i],"circle"+str(i))
		geompy.addToStudy(self.extruWire,"ExtrusionPath")
		for i in xrange(len(face_circles)):
			geompy.addToStudy(face_circles[i],"face:"+str(i))
		geompy.addToStudy(self.pipeGeom,"PipeGeom")

		# Make a shell
		self.pipeShell = geompy.MakeShell([self.pipeGeom,face_circles[0],face_circles[-1]])
		self.pipeSolid = geompy.MakeSolid([self.pipeShell])
		geompy.addToStudy(self.pipeSolid,"PipeSolid")
		self.pipeGeom = self.pipeSolid
		
	def doFaceGroups(self):
		dx = geompy.MakeVectorDXDYDZ(0.001,0,0)
		# FACE groups definition:
		# 1. inlet
		# 2. outlet
		# 5. wall

		# wall is declared and filled
		sub_faces = SubShapeAllSorted(self.pipeGeom, ShapeType["FACE"])
		print("The faces are:",sub_faces)
		self.g_wall = CreateGroup(self.pipeGeom, ShapeType["FACE"])
		UnionList(self.g_wall, sub_faces)

		# inlet
		# This for some reason returns a single shape instead of a list.		
		#sub_faces = GetShapesNearPoint(self.pipeGeom,MakeVertex(-0.01,0,0),4,0.01)#GetShapesOnPlane(self.pipeGeom, ShapeType["FACE"], dx, GEOM.ST_ON)
		sub_faces = GetShapesOnPlaneWithLocation(self.pipeGeom,ShapeType["FACE"],dx,MakeVertex(0,0,0),GEOM.ST_ON)
		print("Got shapes on plane:",sub_faces)
		self.g_inlet = CreateGroup(self.pipeGeom, ShapeType["FACE"])
		# Adds to the group g_inlet all the faces in sub_faces
		UnionList(self.g_inlet, sub_faces)
		# Removes all the wall group (g_wall) all the faces in sub_faces. These are the faces in the x-plane
		#DifferenceList(self.g_wall, sub_faces)

		# Seems to add the group to the "father" v_duct.
		geompy.addToStudyInFather(self.pipeGeom, self.g_inlet, "inlet")

		# outlet
		# Get all the shapes with the normal dx and the location p1 which is the end of our cylinder
		#sub_faces = GetShapesNearPoint(self.pipeGeom,MakeVertex(self.points[-1][0],0,0),4,0.001)#GetShapesOnPlaneWithLocation(self.pipeGeom, ShapeType["FACE"], dx, MakeVertex(0,0,0), GEOM.ST_ON)
		sub_faces = GetShapesOnPlaneWithLocation(self.pipeGeom,ShapeType["FACE"],dx,MakeVertex(self.points[-1][0],0,0),GEOM.ST_ON)
		print("Got shapes on plane,outlet:",sub_faces)
		self.g_outlet = CreateGroup(self.pipeGeom, ShapeType["FACE"])
		UnionList(self.g_outlet, sub_faces)
		#DifferenceList(self.g_wall, sub_faces)

		addToStudyInFather(self.pipeGeom, self.g_outlet, "outlet")

		# subtract out all faces that are perpendicular to the x-axis (the circle faces)
		for i in xrange(len(self.points)):
			sub_faces = GetShapesOnPlaneWithLocation(self.pipeGeom,ShapeType["FACE"],dx,MakeVertex(self.points[i][0],0,0),GEOM.ST_ON)
			DifferenceList(self.g_wall,sub_faces)
		#DifferenceList(self.g_wall,sub_faces)
		# wall is finally obtained
		addToStudyInFather(self.pipeGeom, self.g_wall, "wall")

		print "FACE groups defined..."
	def doEdges(self,params):
		pipeEdgeGroup = CreateGroup(self.pipeGeom, ShapeType["EDGE"])
		print("The original edges:",dir(pipeEdgeGroup))
		'''
		inletEdge = GetEdgesByLength(self.pipeGeom,math.pi*self.points[0][1]*2,math.pi*self.points[0][1]*2*1.01,1,1)
		outletEdge = GetEdgesByLength(self.pipeGeom,math.pi*self.points[-1][1]*2,math.pi*self.points[-1][1]*2*1.01,1,1)
		letEdge = CutGroups(pipeEdgeGroup,inletEdge)
		letEdge = CutGroups(letEdge,outletEdge)
		print("Now have length edge:",letEdge)
		#addToStudyInFather(self.pipeGeom,letEdge,"length")
		addToStudyInFather(self.pipeGeom,inletEdge,"inletEdge")
		addToStudyInFather(self.pipeGeom,outletEdge,"outletEdge")
		
		#let_seg = self.pipeMesh.Segment(letEdge)
		#let_seg.NumberOfSegments(100)
		inlet_seg = self.pipeMesh.Segment(inletEdge)
		inlet_seg.NumberOfSegments(50)
		outlet_seg = self.pipeMesh.Segment(outletEdge)
		outlet_seg.NumberOfSegments(50

		for i in xrange(len(self.points)):
			
		'''
		self.circleEdges = []
		circleEdgeGroup = None
		for i in xrange(len(self.points)):
			print "Getting edge:",self.points[i]
			circleEdges = GetEdgesByLength(self.pipeGeom,math.pi*self.points[i][1]*2,math.pi*self.points[i][1]*2*1.01,1,1)
			print(circleEdges)
			addToStudyInFather(self.pipeGeom,circleEdges,"circle"+str(i))
			self.circleEdges.append(circleEdges)
			circle_let = self.pipeMesh.Segment(circleEdges)
			seg = circle_let.NumberOfSegments(50)
		'''
		print("The two groups are now:",pipeEdgeGroup,circleEdgeGroup)
		pipeEdgeGroup = CutGroups(pipeEdgeGroup,circleEdgeGroup)
		#addToStudyInFather(self.pipeGeom,pipeEdgeGroup,"length")
		length_let = self.pipeMesh.Segment(pipeEdgeGroup)
		seg = length_let.NumberOfSegments(100)
		'''

	def generateMesh(self,params):
		self.doGeometry([])		
		self.doFaceGroups()
		self.pipeMesh = smesh.Mesh(self.pipeGeom,"mesh_d")
		self.doEdges([])
		
		self.basicMeshAlgo = self.pipeMesh.Segment()
		self.basicMeshAlgo.NumberOfSegments(1)
		self.triaMeshAlgo = self.pipeMesh.Triangle()
		sub_faces = geompy.SubShapeAllSortedCentres(self.pipeGeom,geompy.ShapeType["FACE"])
		'''
		circle_ids = []
		for i in xrange(len(self.points)):
			circle_ids.append( GetShapesOnPlaneWithLocationIDs(self.pipeGeom,ShapeType["FACE"],MakeVectorDXDYDZ(0.1,0,0),MakeVertex(self.points[i][0],0,0),GEOM.ST_ONOUT ) )	
		print("Got circles:",circle_ids)
		sub_faces_good = []
		for sub_face in sub_faces:
			if (GetSubShapeID(self.pipeGeom,sub_face) in circle_ids[2]):
				print "Got a good face!",GetSubShapeID(self.pipeGeom,sub_face)
				sub_faces_good.append(sub_face)
			else:
				print "This face is no good!>",GetSubShapeID(self.pipeGeom,sub_face) 
		'''
		#algo2d = self.pipeMesh.Quadrangle(geom=self.g_wall)
		self.tetraMeshAlgo = self.pipeMesh.Tetrahedron()
		status = self.pipeMesh.Compute()
	
		self.pipeMesh.GroupOnGeom(self.g_inlet,"inlet")
		self.pipeMesh.GroupOnGeom(self.g_outlet,"outlet")
		self.pipeMesh.GroupOnGeom(self.g_wall,"wall")
