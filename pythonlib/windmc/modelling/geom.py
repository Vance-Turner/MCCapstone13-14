import salome
import geompy
import math
import smesh
import StdMeshers
from geompy import *

class BasicGeom:

	'''
	A vector for used when providing a standard axis for the cylinder.
	This points along the x-axis.
	'''
	DX = MakeVectorDXDYDZ(0.001,0,0)

	'''
	A vector for used when providing a standard axis for the cylinder.
	This points along y-axis.
	'''
	DY = MakeVectorDXDYDZ(0,0.001,0)

	'''
	A vector for used when providing a standard axis for the cylinder.
	This points along the z-axis.
	'''
	DZ = MakeVectorDXDYDZ(0,0,0.001)

	def __init__(self):
		pass

class BasicCylinder(BasicGeom):

	def __init__(self,name):
		BasicGeom.__init__(self)
		self._name = name
		self._geom = None

	def doGeom(self,radius,height,x=0,y=0,z=0,axis=BasicGeom.DX):
		point = MakeVertex(x,y,z)
		self._radius = radius
		self._height = height
		self._geom = MakeCylinder(point,axis,radius,height)
		print "Just made cylinder, height>",height
		#geompy.addToStudy(self._geom,self._name+"_geom_cylinder")

		# build base circle
		p0 = MakeVertex(x, y, z)
		base_circle = MakeCircle(p0,axis,self._radius)

		# build face
		f_duct = MakeFace(base_circle, 1)

		# extrude along the z axis
		v_duct = MakePrismVecH(f_duct, axis, self._height)
		addToStudy(v_duct, self._name+"_geom_cyl")
		self._geom=v_duct
		return self._geom

	def getGeom(self):
		if self._geom == None:
			return None
		else:
			return self._geom

	def doEdges(self,geom):
		self.circleEdges = []
		self.lengthEdge = []
		circleEdges = GetEdgesByLength(geom,math.pi*self._radius*2,math.pi*self._radius*2,1,1)
		print "In cylinder got edges:",circleEdges
		lengthEdges = GetEdgesByLength(geom,self._height,self._height*1.01,1,1)
		print "Got length edges:",lengthEdges
		geompy.addToStudyInFather(geom,circleEdges,self._name+"circle")
		geompy.addToStudyInFather(geom,lengthEdges,self._name+"length")
		self.circleEdges.append(circleEdges)
		self.lengthEdge.append(lengthEdges)

	def getLengthEdges(self):
		return self.lengthEdge
	
	def getCircleEdges(self):
		return self.circleEdges

class BasicShroud(BasicGeom):
	
	def __init__(self,name,points,baseRadius, thickness):
		BasicGeom.__init__(self)
		self._name = name
		self._geom = None
		self._points = points
		self._baseRadius = baseRadius
		self._innerRadius = baseRadius - thickness
		self._thickness = thickness
		ready = True
		# Build the points for the inner circle from the outer circle
		self._innerPoints = map(lambda point: (point[0],point[1]-thickness),self._points)
		print "The inner points:",self._innerPoints,self._points
		# Now check the inner radii
		for i in xrange(len(self._innerPoints)):
			if self._innerPoints[i][1] <= 0 or self._innerPoints[i][1] > self._points[i][1]:
				raise ArithmeticError("Inner radius cannot be negative, zero, or greater than the baseRadius!")
				self._ready = False
		self._ready = True
		self.sortPoints()
		self._thickness = thickness

	def checkReady(self):
		if self._ready == False:
			print "There is an error with input, cannot compute BasicShroud Geom!"
		return self._ready

	def sortPoints(self):
		if self.checkReady():
			# We will use the key method to sort the points
			print(self._points)
			self._points.sort(key=lambda point: point[0])

	def normalizePoints(self):
		if self.checkReady():
			# First, get the scale factor, which is just the
			# point that is the farthest from zero. 
			# TODO: We need to look into having shrowds that
			# start not from zero.
			maxNumber = max(self._points,key=lambda point:point[0])
			print "The maxNumber",maxNumber	
			self._points = map(lambda point: (point[0]/maxNumber[0],point[1]),self._points)

	def doGeom(self):
		if self.checkReady():
			# First, create the wire which we will get our vertex info from.
			# Create the command string. For now, the path starts at 0,0
			# The cylinder will be centered at 0,0 for now.
			command = "Sketcher: F 0 0"
			for point in self._points:
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
			inner_circles = []
			self._points.insert(0,(0,self._baseRadius))
			self._innerPoints.insert(0,(0,self._baseRadius-self._thickness))
			for i in xrange(len(centres)):
				circles.append(geompy.MakeCircle(centres[i],normal,self._points[i][1]))
				inner_circles.append(geompy.MakeCircle(centres[i],normal,self._innerPoints[i][1]))
			# Make the pipe!!
			self.pipeGeom = geompy.MakePipeWithDifferentSections(circles, centres, self.extruWire, 0, 0)
			self.innerPipeGeom = geompy.MakePipeWithDifferentSections(inner_circles,centres,self.extruWire,0,0)

			# Now add them to the study
			for i in xrange(len(circles)):
				geompy.addToStudy(circles[i],self._name+"circle"+str(i))
				geompy.addToStudy(inner_circles[i],self._name+"innerCircle"+str(i))
			geompy.addToStudy(self.extruWire,self._name+"ExtrusionPath")

			# Make the faces
			face_circles = []
			inner_face_circles = []
			for i in xrange(len(circles)):
				face_circles.append(geompy.MakeFaceWires([circles[i],inner_circles[i]],True))
			print("Just added these many circles:",len(face_circles))
			for i in xrange(len(face_circles)):
				geompy.addToStudy(face_circles[i],self._name+"face:"+str(i))
			geompy.addToStudy(self.pipeGeom,self._name+"PipeGeom")

			# Make a shell
			self.pipeShell = geompy.MakeShell([self.pipeGeom,self.innerPipeGeom,face_circles[0],face_circles[-1]])
			self.pipeSolid = geompy.MakeSolid([self.pipeShell])
			geompy.addToStudy(self.pipeSolid,self._name+"PipeSolid")
			self.pipeGeom = self.pipeSolid
			self._geom = self.pipeGeom

	def doEdges(self,geom):
		pipeEdgeGroup = CreateGroup(self.pipeGeom, ShapeType["EDGE"])

		self.circleEdgesComplete = []
		circleEdgeGroup = None
		for i in xrange(len(self._points)):
			print "Getting edge:",self._points[i]
			circleEdges = GetEdgesByLength(geom,math.pi*self._points[i][1]*2,math.pi*self._points[i][1]*2*1.01,1,1)
			print(circleEdges)
			geompy.addToStudyInFather(geom,circleEdges,self._name+"circle"+str(i))
			self.circleEdgesComplete.append(circleEdges)
			#circle_let = self.pipeMesh.Segment(circleEdges)
			#seg = circle_let.NumberOfSegments(50)	
		for i in xrange(len(self._innerPoints)):
			print "Getting edge:",self._innerPoints[i]
			circleEdges = GetEdgesByLength(geom,math.pi*self._innerPoints[i][1]*2,math.pi*self._innerPoints[i][1]*2*1.01,1,1)
			print(circleEdges)
			geompy.addToStudyInFather(geom,circleEdges,self._name+"circle"+str(i))
			#circle_let = self.pipeMesh.Segment(circleEdges)
			#seg = circle_let.NumberOfSegments(50)	
			self.circleEdgesComplete.append(circleEdges)
		
		return self.circleEdgesComplete		
	
	def getGeom(self):
		if self._geom == None:
			raise AttributeError("You must call doGeom first.")
		else:
			return self._geom

	'''
	Get the length of the shroud.
	'''
	def getLength(self):
		return self._points[-1][0]

class BasicWindTunnel:

	def __init__(self,name,shroud_points,shroud_baseRadius, shroud_thickness,tunnel_radius,tunnel_height,x=0,y=0,z=0,tunnel_axis=BasicGeom.DX):
		# TODO: Make the shroud respect the tunnel_axis
		self._name = name
		self._shroudPoints = shroud_points
		self._shroudBaseRadius = shroud_baseRadius
		self._shroudThickness = shroud_thickness
		self._tunnelRadius = tunnel_radius
		self._tunnelHeight = tunnel_height
		self._x = x
		self._y = y
		self._z = z
		self._axis = tunnel_axis
		if self._shroudBaseRadius >= self._tunnelRadius:
			raise ArithmeticError("Cannot have shroud radius larger than tunnel radius!")

		for point in shroud_points:
			if point[1] > self._tunnelRadius:
				raise ArithmeticError("Cannot have shroud radius larger than tunnel radius!")

	def doGeom(self):
		self._tunnel = BasicCylinder(self._name+"_tunnel")
		self._shroud = BasicShroud(self._name+"_shroud",self._shroudPoints,self._shroudBaseRadius,self._shroudThickness)
		self._shroud.doGeom()		
		self._tunnel.doGeom(self._tunnelRadius,self._tunnelHeight,self._x,self._y,self._z)
		# Center the shroud
		# TODO: Make the translation respect the tunnel_axis
		if self._tunnelHeight > self._shroud.getLength():
			geompy.TranslateDXDYDZ(self._shroud.getGeom(),(self._tunnelHeight-self._shroud.getLength())/2.0,0,0)

		# Now make the cut
		self._tunnelComplete = geompy.MakeCut(self._tunnel.getGeom(),self._shroud.getGeom())
		geompy.addToStudy(self._tunnelComplete,self._name+"_complete")
		self.createGroups()

	def createGroups(self):
		self._shroudEdges = self._shroud.doEdges(self._tunnelComplete)
		self._tunnel.doEdges(self._tunnelComplete)
		self._tunnelLengthEdges = self._tunnel.getLengthEdges()
		self._tunnelCircleEdges = self._tunnel.getCircleEdges()

		# FACE groups definition:
		# 1. inlet
		# 2. outlet
		# 5. wall

		# wall is declared and filled
		sub_faces = SubShapeAllSorted(self._tunnelComplete, ShapeType["FACE"])
		print("The faces are:",sub_faces)
		self.g_wall = CreateGroup(self._tunnelComplete, ShapeType["FACE"])
		UnionList(self.g_wall, sub_faces)

		# inlet	
		sub_faces = GetShapesOnPlaneWithLocation(self._tunnelComplete,ShapeType["FACE"],BasicGeom.DX,MakeVertex(0,0,0),GEOM.ST_ON)
		print("Got shapes on plane:",sub_faces)
		self.g_inlet = CreateGroup(self._tunnelComplete, ShapeType["FACE"])
		# Adds to the group g_inlet all the faces in sub_faces
		UnionList(self.g_inlet, sub_faces)
		# Removes all the wall group (g_wall) all the faces in sub_faces. These are the faces in the x-plane
		DifferenceList(self.g_wall, sub_faces)

		# Seems to add the group to the "father" v_duct.
		geompy.addToStudyInFather(self._tunnelComplete, self.g_inlet, "inlet")	

		# outlet
		sub_faces = GetShapesOnPlaneWithLocation(self._tunnelComplete,ShapeType["FACE"],BasicGeom.DX,MakeVertex(self._tunnelHeight,0,0),GEOM.ST_ON)
		print("Got shapes on plane:",sub_faces)
		self.g_outlet = CreateGroup(self._tunnelComplete, ShapeType["FACE"])
		# Adds to the group g_inlet all the faces in sub_faces
		UnionList(self.g_outlet, sub_faces)
		# Removes all the wall group (g_wall) all the faces in sub_faces. These are the faces in the x-plane
		DifferenceList(self.g_wall, sub_faces)

		# Seems to add the group to the "father" v_duct.
		geompy.addToStudyInFather(self._tunnelComplete, self.g_outlet, "outlet")
		
		# inlet of shroud
		sub_faces = GetShapesOnPlaneWithLocation(self._tunnelComplete,ShapeType["FACE"],BasicGeom.DX,MakeVertex(((self._tunnelHeight-self._shroud.getLength())/2.0),0,0),GEOM.ST_ON)
		self.shroud_g_inlet = CreateGroup(self._tunnelComplete, ShapeType["FACE"])
		UnionList(self.shroud_g_inlet, sub_faces)
		DifferenceList(self.g_wall, sub_faces)
		geompy.addToStudyInFather(self._tunnelComplete, self.shroud_g_inlet, "shroud_inlet")

		# outlet of shroud
		sub_faces = GetShapesOnPlaneWithLocation(self._tunnelComplete,ShapeType["FACE"],BasicGeom.DX,MakeVertex(((self._tunnelHeight-self._shroud.getLength())/2.0)+self._shroud.getLength(),0,0),GEOM.ST_ON)
		self.shroud_g_outlet = CreateGroup(self._tunnelComplete, ShapeType["FACE"])
		UnionList(self.shroud_g_outlet, sub_faces)
		DifferenceList(self.g_wall, sub_faces)
		geompy.addToStudyInFather(self._tunnelComplete, self.shroud_g_outlet, "shroud_outlet")
		

		# For now, just take everything else as sym!
		# TODO: Actually get the faces of the shroud walls...
		addToStudyInFather(self._tunnelComplete, self.g_wall, "wall")	
		
	def getTunnelCircleEdges(self):
		return self._tunnelCircleEdges

	def getTunnelLengthEdges(self):
		return self._tunnelLengthEdges

	def getShroudEdges(self):
		return self._shroudEdges

	# TODO: Actually move this into a WindTunnel class in the mesh.py, for now just do it in geom...
	def doMesh(self):
		self.pipeMesh = smesh.Mesh(self._tunnelComplete,"mesh_d")
		
		self.basicMeshAlgo = self.pipeMesh.Segment()
		self.basicMeshAlgo.NumberOfSegments(10)
		self.triaMeshAlgo = self.pipeMesh.Triangle()
		sub_faces = geompy.SubShapeAllSortedCentres(self._tunnelComplete,geompy.ShapeType["FACE"])
		# We must do the edge segmentation of the circles
		for circle in self.getTunnelCircleEdges():	
			circle_let = self.pipeMesh.Segment(circle)
			seg = circle_let.NumberOfSegments(50)
		for circle in self.getShroudEdges():
			circle_let2 = self.pipeMesh.Segment(circle)
			seg2 = circle_let2.NumberOfSegments(50)	
		length_let = self.pipeMesh.Segment(self.getTunnelLengthEdges()[0])
		seg3 = length_let.NumberOfSegments(20)			
		algo2d = self.pipeMesh.Quadrangle(geom=self.g_wall)
		self.tetraMeshAlgo = self.pipeMesh.Tetrahedron()
		status = self.pipeMesh.Compute()
	
		self.pipeMesh.GroupOnGeom(self.g_inlet,"inlet")
		self.pipeMesh.GroupOnGeom(self.g_outlet,"outlet")
		self.pipeMesh.GroupOnGeom(self.g_wall,"wall")
		self.pipeMesh.GroupOnGeom(self.shroud_g_inlet,"shroud_inlet")
		self.pipeMesh.GroupOnGeom(self.shroud_g_outlet,"shroud_outlet")	

	def export(self,location):
		self.pipeMesh.ExportMED(location)	
