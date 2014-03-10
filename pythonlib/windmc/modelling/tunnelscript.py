ACTUATOR_TUNNEL_GEN = "ActuatorTunnelGenerator"

def createTunnel(fileName, kwargs, doGUI=False,doMeshing=True,killSalomeAfter=True):
    '''
    @author: Vance Turnewitsch
    @date: Feb 20, 2014
    This code is to be run with salome-meca 2014.1 not an earlier version.
    '''
    try:
        import salome
        import math
    
        salome.salome_init()
        import GEOM
        from salome.geom import geomBuilder
        theStudy = salome.myStudy
        #from SMESH_mechanic import SMESH
    
        geompy = geomBuilder.New(salome.myStudy)
        if doGUI:
            gg = salome.ImportComponentGUI("GEOM")
    
        #import SMESH
        #from salome.smesh import smeshBuilder
    
        # Get the parameters
        diskX = kwargs['diskX']
        diskY = kwargs['diskY']
        diskZ = kwargs['diskZ']
    
        diskHeight = kwargs['diskHeight']
        diskRadius = kwargs['diskRadius']
        tunnelHeight = kwargs['tunnelHeight']
        tunnelRadius = kwargs['tunnelRadius']
        '''
        tunnelFineness=kwargs['tunnelFineness']
        diskFineness=kwargs['diskFineness']
    
        tunnelMaxTetraSize=kwargs['tunnelMaxTetraSize']
        tunnelMinTetraSize=kwargs['tunnelMinTetraSize']
        diskMaxTetraSize=kwargs['diskMaxTetraSize']
        diskMinTetraSize=kwargs['diskMinTetraSize']
        '''
        tunnelMaxSize = kwargs['tunnelMaxSize']
        
        # These are the raw coordinates for the shroud points
        shroudCoords = kwargs['shroudPoints']
        # This is the thickness of the shroud material
        shroudThickness = kwargs['shroudThickness']
    
        print "Creating tunnel with following properties:",kwargs
    
        #smesh = smeshBuilder.New(salome.myStudy)
    
        # Make the actuator disk
        startDiskBase = geompy.MakeVertex(diskX, diskY, diskZ)
        startDiskBaseID = geompy.addToStudy(startDiskBase, 'StartDiskBase')
        if doGUI:
            gg.createAndDisplayGO(startDiskBaseID)
    
        vx = geompy.MakeVectorDXDYDZ(100, 0, 0)
        vxID = geompy.addToStudy(vx, 'vx')
    
    
        if doGUI:
            gg.createAndDisplayGO(vxID)
    
        diskCyl = geompy.MakeCylinder(startDiskBase, vx, diskRadius, diskHeight)
        diskCylID = geompy.addToStudy(diskCyl, 'Disk')
        #geompy.addToStudy(diskCyl,'Disk')
        if doGUI:
            gg.createAndDisplayGO(diskCylID)
    
        # Make the cyliner
        origin = geompy.MakeVertex(0, 0, 0)
        tunnelCyl = geompy.MakeCylinder(origin, vx, tunnelRadius, tunnelHeight)
        
        # Make the shroud
        # The actual shroud vertices created from the raw data points
        shroudPoints = []
        # We better sort the points first
        shroudCoords.sort(key=lambda item: item[0])
        print "The shroud points to be meshed>",shroudCoords
        print "The sorted shroud coords:",shroudCoords
        for raw in shroudCoords:
            # The points are in x and z
            vertex = geompy.MakeVertex(raw[0],0,raw[1])
            shroudPoints.append(vertex)
            geompy.addToStudy(vertex,'Point:'+str(raw[0]))
            
        # Now make the line that we will extrude for the base that gets revolved
        ShroudLine = geompy.MakePolyline(shroudPoints)
        geompy.addToStudy(ShroudLine,'ShroudLine')
        # Now make a vector so that we can extrude this line
        vz = geompy.MakeVectorDXDYDZ(0,0,1)
        geompy.addToStudy(vz,'vz')
        # This is the extruded shroud line
        ShroudOutline = geompy.MakePrismVecH(ShroudLine,vz,0.25)
        geompy.addToStudy(ShroudOutline,'ShroudOutline')
        # Let's make the shroud!
        Shroud = geompy.MakeRevolution2Ways(ShroudOutline,vx,180*math.pi/180.0)
        geompy.addToStudy(Shroud,'Shroud')
    
        # Now make the tunnel by cutting the disk from cylinder and then the shroud
        tunnel = geompy.MakeCut(tunnelCyl, diskCyl)
        tunnel = geompy.MakeCut(tunnel,Shroud)
        tunnelID = geompy.addToStudy(tunnel, 'Tunnel')
    
        if doGUI:
            gg.createAndDisplayGO(tunnelID)
            gg.setDisplayMode(tunnelID, 1)
    
        # Get the faces of the Tunnel
        inletFace = geompy.GetShapesOnPlaneWithLocationIDs(tunnel, geompy.ShapeType["FACE"], vx, origin, GEOM.ST_ON)
        if len(inletFace) == 1:
            print "Got inlet face:", inletFace[0]
            inletFace = inletFace[0]
    
        outletFace = geompy.GetShapesOnPlaneWithLocationIDs(tunnel, geompy.ShapeType["FACE"], vx,
                                                            geompy.MakeVertex(tunnelHeight, 0, 0), GEOM.ST_ON)
        if len(outletFace) == 1:
            print "Got outlet face:", outletFace[0]
            outletFace = outletFace[0]
    
        tunnelWall = geompy.GetShapesOnCylinderWithLocationIDs(tunnel, geompy.ShapeType["FACE"], vx, origin, tunnelRadius,GEOM.ST_ON)
        if len(tunnelWall) == 1:
            print "Got tunnelWall:", tunnelWall[0]
            tunnelWall = tunnelWall[0]
    
        diskInletFace = geompy.GetShapesOnPlaneWithLocationIDs(tunnel, geompy.ShapeType["FACE"], vx, startDiskBase,GEOM.ST_ON)
        if len(diskInletFace) == 1:
            print "Got inlet face:", diskInletFace[0]
            diskInletFace = diskInletFace[0]
    
        diskOutletFace = geompy.GetShapesOnPlaneWithLocationIDs(tunnel, geompy.ShapeType["FACE"], vx,geompy.MakeVertex(diskX + diskHeight, diskY, diskZ),GEOM.ST_ON)
        if len(diskOutletFace) == 1:
            print "Got outlet face:", diskOutletFace[0]
            diskOutletFace = diskOutletFace[0]
    
        diskWall = geompy.GetShapesOnCylinderWithLocationIDs(tunnel, geompy.ShapeType["FACE"], vx, startDiskBase,diskRadius, GEOM.ST_ON)
        if len(diskWall) == 1:
            print "Got diskWall:", diskWall[0]
            diskWall = diskWall[0]
    
        # Build the groups of the faces of the tunnel
        def createFaceGroup(theGeom, groupName, *faces):
            '''
            @Return: The group created
            '''
            print "Creating group:", groupName
            theGroup = geompy.CreateGroup(theGeom, geompy.ShapeType["FACE"])
            for face in faces:
                print "Adding a face to group:", groupName
                geompy.AddObject(theGroup, face)
            if doGUI:
                groupID = geompy.addToStudyInFather(theGeom, theGroup, groupName)
    
            if doGUI:
                gg.createAndDisplayGO(groupID)
            return theGroup
    
        inletGroup = createFaceGroup(tunnel, 'Inlet', inletFace)
        outletGroup = createFaceGroup(tunnel, 'Outlet', outletFace)
        wallGroup = createFaceGroup(tunnel, 'TunnelWall', tunnelWall)
    
        diskInletGroup = createFaceGroup(tunnel, 'DiskInlet', diskInletFace)
        diskOutletGroup = createFaceGroup(tunnel, 'DiskOutlet', diskOutletFace)
        diskWallGroup = createFaceGroup(tunnel, 'DiskWall', diskWall)
        
        # Create the group for the 
        AllFaces = geompy.CreateGroup(tunnel, geompy.ShapeType["FACE"])
        AllFaceIDs = geompy.SubShapeAllSortedCentresIDs(tunnel,geompy.ShapeType["FACE"])
        geompy.UnionIDs(AllFaces, AllFaceIDs)
        tunnelWallGroup = geompy.CutListOfGroups([AllFaces], [inletGroup,outletGroup,wallGroup,diskInletGroup,diskOutletGroup,diskWallGroup])
        geompy.addToStudyInFather(tunnel,AllFaces,'AllFaces')
        geompy.addToStudyInFather(tunnel,tunnelWallGroup,'TunnelWall')
    
        # Get faces on the disk
        diskInletFace_Orig = geompy.GetShapesOnPlaneWithLocationIDs(diskCyl, geompy.ShapeType["FACE"], vx, startDiskBase, GEOM.ST_ON)[0]
        diskOutletFace_Orig = geompy.GetShapesOnPlaneWithLocationIDs(diskCyl, geompy.ShapeType["FACE"], vx,geompy.MakeVertex(diskX + diskHeight, 0, 0),GEOM.ST_ON)[0]
        diskWallFace_Orig = geompy.GetShapesOnCylinderWithLocationIDs(diskCyl, geompy.ShapeType["FACE"], vx, startDiskBase, diskRadius,GEOM.ST_ON)[0]
    
        # Create the face groups of the disk
        diskInletGroup_Orig = createFaceGroup(diskCyl, 'DiskInletOrig', diskInletFace_Orig)
        diskOutletGroup_Orig = createFaceGroup(diskCyl, 'DiskOutletOrig', diskOutletFace_Orig)
        diskWallGroup_Orig = createFaceGroup(diskCyl, 'DiskWallOrig', diskWallFace_Orig)
    
        ###
        ### SMESH component
        ###
        if doMeshing:
            import  SMESH, SALOMEDS
            from salome.smesh import smeshBuilder
        
            # calculate the number of segments for the disk
            numOfSegments = round(60.0*3.0/tunnelMaxSize)
            smesh = smeshBuilder.New(theStudy)
            TunnelSansDisk = smesh.Mesh(tunnel)
            Regular_1D = TunnelSansDisk.Segment()
            Max1D_3 = Regular_1D.MaxSize(tunnelMaxSize)
            MEFISTO_2D = TunnelSansDisk.Triangle(algo=smeshBuilder.MEFISTO)
            MaxArea2D_5 = MEFISTO_2D.MaxElementArea(5)
            NETGEN_3D = TunnelSansDisk.Tetrahedron()
            Max2D_3 = smesh.CreateHypothesis('MaxElementArea')
            Max2D_3.SetMaxElementArea( 3 )
            a60_Segments1D = smesh.CreateHypothesis('NumberOfSegments')
            a60_Segments1D.SetNumberOfSegments( int(numOfSegments) )
            a60_Segments1D.SetDistrType( 0 )
            status = TunnelSansDisk.AddHypothesis(Regular_1D,diskInletGroup)
            status = TunnelSansDisk.AddHypothesis(a60_Segments1D,diskInletGroup)
            status = TunnelSansDisk.AddHypothesis(MEFISTO_2D,diskInletGroup)
            status = TunnelSansDisk.AddHypothesis(Max2D_3,diskInletGroup)
            status = TunnelSansDisk.AddHypothesis(Regular_1D,diskOutletGroup)
            status = TunnelSansDisk.AddHypothesis(a60_Segments1D,diskOutletGroup)
            status = TunnelSansDisk.AddHypothesis(MEFISTO_2D,diskOutletGroup)
            status = TunnelSansDisk.AddHypothesis(Max2D_3,diskOutletGroup)
            status = TunnelSansDisk.AddHypothesis(MEFISTO_2D,diskWallGroup)
            status = TunnelSansDisk.AddHypothesis(Max2D_3,diskWallGroup)
            MaxSize_1D_2 = smesh.CreateHypothesis('MaxLength')
            MaxSize_1D_2.SetLength( 2 )
            Disk_1 = smesh.Mesh(diskCyl)
            status = Disk_1.AddHypothesis(MaxSize_1D_2)
            status = Disk_1.AddHypothesis(Regular_1D)
            status = Disk_1.AddHypothesis(Max2D_3)
            status = Disk_1.AddHypothesis(MEFISTO_2D)
            status = Disk_1.AddHypothesis(NETGEN_3D)
            Inlet_1 = TunnelSansDisk.GroupOnGeom(inletGroup,'Inlet',SMESH.FACE)
            Outlet_1 = TunnelSansDisk.GroupOnGeom(outletGroup,'Outlet',SMESH.FACE)
            TunnelWall_1 = TunnelSansDisk.GroupOnGeom(wallGroup,'TunnelWall',SMESH.FACE)
            DiskInlet_1 = TunnelSansDisk.GroupOnGeom(diskInletGroup,'DiskInlet',SMESH.FACE)
            DiskOutlet_1 = TunnelSansDisk.GroupOnGeom(diskOutletGroup,'DiskOutlet',SMESH.FACE)
            DiskWall_1 = TunnelSansDisk.GroupOnGeom(diskWallGroup,'DiskWall',SMESH.FACE)
            ShroudWall_Mesh = TunnelSansDisk.GroupOnGeom(tunnelWallGroup,'ShroudWall',SMESH.FACE)
            Import_1D2D = Disk_1.UseExisting2DElements(geom=diskInletGroup_Orig)
            DiskInlet_Faces = Import_1D2D.SourceFaces([ DiskInlet_1 ],0,0)
            DiskOutlet_Faces = smesh.CreateHypothesis('ImportSource2D')
            DiskOutlet_Faces.SetSourceFaces( [ DiskOutlet_1 ] )
            DiskOutlet_Faces.SetCopySourceMesh( 0, 0 )
            status = Disk_1.AddHypothesis(Import_1D2D,diskOutletGroup_Orig)
            status = Disk_1.AddHypothesis(DiskOutlet_Faces,diskOutletGroup_Orig)
            DiskWall_Faces = smesh.CreateHypothesis('ImportSource2D')
            DiskWall_Faces.SetSourceFaces( [ DiskWall_1 ] )
            DiskWall_Faces.SetCopySourceMesh( 0, 0 )
            status = Disk_1.AddHypothesis(Import_1D2D,diskWallGroup_Orig)
            status = Disk_1.AddHypothesis(DiskWall_Faces,diskWallGroup_Orig)
            isDone = TunnelSansDisk.Compute()
            isDone = Disk_1.Compute()
            Tunnel_1 = smesh.Concatenate([TunnelSansDisk.GetMesh(), Disk_1.GetMesh()], 1, 1, 1e-05)
            [ Inlet_2, Outlet_2, TunnelWall_2, DiskInlet_2, DiskOutlet_2, DiskWall_2, ShroudWall_2 ] = Tunnel_1.GetGroups()
            aCriteria = []
            aCriterion = smesh.GetCriterion(SMESH.VOLUME,SMESH.FT_BelongToGeom,SMESH.FT_EqualTo,diskCyl)#SMESH.VOLUME,SMESH.FT_BelongToGeom,SMESH.FT_Undefined,'Disk')
            aCriteria.append(aCriterion)
            aFilter_1 = smesh.GetFilterFromCriteria(aCriteria)
            aFilter_1.SetMesh(Tunnel_1.GetMesh())
            Disk_2 = Tunnel_1.GroupOnFilter( SMESH.VOLUME, 'Group_1', aFilter_1 )
            Disk_2.SetColor( SALOMEDS.Color( 1, 0.666667, 0 ))
            Disk_2.SetName( 'Disk' )
            DiskInlet_Sub = TunnelSansDisk.GetSubMesh( diskInletGroup, 'DiskInlet_Sub' )
            DiskOutlet_Sub = TunnelSansDisk.GetSubMesh( diskOutletGroup, 'DiskOutlet_Sub' )
            DiskWall_Sub = TunnelSansDisk.GetSubMesh( diskWallGroup, 'DiskWall_Sub' )
            DiskInlet_3 = Import_1D2D.GetSubMesh()
            DiskOutlet_3 = Disk_1.GetSubMesh( diskOutletGroup_Orig, 'DiskOutlet' )
            DiskWall_3 = Disk_1.GetSubMesh( diskWallGroup_Orig, 'DiskWall' )
        
        
            ## Set names of Mesh objects
            smesh.SetName(Regular_1D.GetAlgorithm(), 'Regular_1D')
            smesh.SetName(NETGEN_3D.GetAlgorithm(), 'NETGEN_3D')
            smesh.SetName(MEFISTO_2D.GetAlgorithm(), 'MEFISTO_2D')
            smesh.SetName(MaxArea2D_5, 'MaxArea2D_5')
            smesh.SetName(Import_1D2D.GetAlgorithm(), 'Import_1D2D')
            smesh.SetName(Max1D_3, 'Max1D_3')
            smesh.SetName(a60_Segments1D, '60_Segments1D')
            smesh.SetName(MaxSize_1D_2, 'MaxSize_1D_2')
            smesh.SetName(Inlet_1, 'Inlet')
            smesh.SetName(Outlet_1, 'Outlet')
            smesh.SetName(Max2D_3, 'Max2D_3')
            smesh.SetName(TunnelWall_1, 'TunnelWall')
            smesh.SetName(DiskInlet_1, 'DiskInlet')
            smesh.SetName(DiskInlet_Sub, 'DiskInlet_Sub')
            smesh.SetName(DiskInlet_Faces, 'DiskInlet_Faces')
            smesh.SetName(DiskOutlet_1, 'DiskOutlet')
            smesh.SetName(DiskOutlet_Faces, 'DiskOutlet_Faces')
            smesh.SetName(DiskWall_1, 'DiskWall')
            smesh.SetName(DiskOutlet_3, 'DiskOutlet')
            smesh.SetName(DiskWall_Sub, 'DiskWall_Sub')
            smesh.SetName(DiskWall_3, 'DiskWall')
            smesh.SetName(DiskOutlet_Sub, 'DiskOutlet_Sub')
            smesh.SetName(DiskInlet_3, 'DiskInlet')
            smesh.SetName(TunnelSansDisk.GetMesh(), 'TunnelSansDisk')
            smesh.SetName(Tunnel_1.GetMesh(), 'Tunnel')
            smesh.SetName(Disk_1.GetMesh(), 'Disk')
            smesh.SetName(Disk_2, 'Disk')
            smesh.SetName(DiskWall_Faces, 'DiskWall_Faces')
            smesh.SetName(DiskWall_2, 'DiskWall')
            smesh.SetName(DiskInlet_2, 'DiskInlet')
            smesh.SetName(DiskOutlet_2, 'DiskOutlet')
            smesh.SetName(Outlet_2, 'Outlet')
            smesh.SetName(TunnelWall_2, 'TunnelWall')
            smesh.SetName(Inlet_2, 'Inlet')
            smesh.SetName(ShroudWall_2,'ShroudWall')
        
        
            if salome.sg.hasDesktop():
              salome.sg.updateObjBrowser(1)
        
            '''
            Old meshing stuff...
            # Now do the meshing
            cylinderMesh = smesh.Mesh(tunnel, 'Cylinder')
        
            cylAlgo3D = cylinderMesh.Tetrahedron(smeshBuilder.FULL_NETGEN)
            cylAlgo3DParams = cylAlgo3D.Parameters()
            cylAlgo3DParams.SetMaxSize(tunnelMaxTetraSize)
            cylAlgo3DParams.SetMinSize(tunnelMinTetraSize)
            cylAlgo3DParams.SetFineness(tunnelFineness)
            cylAlgo3DParams.SetOptimize(True)
            print "Computing Tunnel Mesh..."
            #cylinderMesh.Compute()
        
            # Now create groups on the mesh from the geometry
            meshInlet = cylinderMesh.GroupOnGeom(inletGroup, "Inlet")
            meshOutlet = cylinderMesh.GroupOnGeom(outletGroup, "Outlet")
            meshWall = cylinderMesh.GroupOnGeom(wallGroup, "TunnelWall")
            meshDiskInlet = cylinderMesh.GroupOnGeom(diskInletGroup, "DiskInlet")
            meshDiskOutlet = cylinderMesh.GroupOnGeom(diskOutletGroup, "DiskOutlet")
            meshDiskWall = cylinderMesh.GroupOnGeom(diskWallGroup, "DiskWall")
        
            # Now compute the disk using 2D elements from the tunnel so that the compound can be made later
            diskMesh = smesh.Mesh(diskCyl, 'Disk')
            print "Assigning inlet src..."
            diskInletAlgo = diskMesh.UseExisting2DElements(diskInletGroup_Orig)
            diskInletAlgo.SourceFaces([meshDiskInlet])
            print "Assigning outlet src..."
            diskOutletAlgo = diskMesh.UseExisting2DElements(diskOutletGroup_Orig)
            diskOutletAlgo.SourceFaces([meshDiskOutlet])
            print "Assigning wall src..."
            diskWallAlgo = diskMesh.UseExisting2DElements(diskWallGroup_Orig)
            diskWallAlgo.SourceFaces([meshDiskWall])
            diskMesh.SetMeshOrder([[diskWallAlgo.GetSubMesh(), diskOutletAlgo.GetSubMesh(), diskInletAlgo.GetSubMesh()]])
            print "Assigning Tetrahedron..."
            diskAlgo3D = diskMesh.Tetrahedron(smeshBuilder.FULL_NETGEN)
            diskAlgo3DParams = diskAlgo3D.Parameters()
            diskAlgo3DParams.SetMaxSize(diskMaxTetraSize)
            diskAlgo3DParams.SetMinSize(diskMinTetraSize)
            diskAlgo3DParams.SetFineness(diskFineness)
            #diskMesh.Compute()
        
            windTunnelMesh = smesh.Concatenate([cylinderMesh.GetMesh(), diskMesh.GetMesh()], False, True, 1e-05, False,
                                               'WindTunnel')
            # Create group of volumes that make up the actuator disk
            volumeFilter = smesh.GetFilter(SMESH.VOLUME,SMESH.FT_BelongToGeom,SMESH.FT_EqualTo,diskCyl)
            volumeGroup = windTunnelMesh.GroupOnFilter(SMESH.VOLUME,'Disk',volumeFilter)
            '''
            # Ok, let's spit it out!
            # Get Information About Mesh by GetMeshInfo
            print "\nInformation about mesh by GetMeshInfo:"
            info = smesh.GetMeshInfo(Tunnel_1)
            keys = info.keys(); keys.sort()
            for i in keys:
               print " %s : %d" % ( i, info[i] )
            # Silly salome-meca can only deal with strings not unicode types...so we have to make sure we have one.
            print "Saving MED to>",str(fileName),type(str(fileName))
            Tunnel_1.ExportMED(str(fileName), autoDimension=False)
    
        if doGUI:
            salome.sg.updateObjBrowser(1)
            
    except:
        print "Salome Failed!"

    #import runSalome
    #runSalome.kill_salome({'portkill':True,'kilall':False})
    if killSalomeAfter:
        import os
        from killSalomeWithPort import killMyPort
        killMyPort(os.getenv('NSPORT'))    


if __name__ == '__main__':
    # parse the arguments
    # This map holds the defaults for creating a tunnel and disk
    import json, os, sys
    print 'Args:',sys.argv
    jsonFile = os.path.join(os.path.dirname(sys.argv[0]),'actuator.json')
    print "loading json from>",jsonFile
    defaultMap = json.load(open(jsonFile,'r'))
    
#     defaultMap = {
#     "diskX": 79.5, "diskY": 0.0, "diskZ": 0.0,
#     "tunnelHeight": 160.0, "tunnelRadius": 100.0, "tunnelFineness": 4,
#     "diskHeight": 1.0, "diskRadius": 27.0, "diskFineness": 4,
#     "tunnelMaxSize": 3.0, "shroudPoints":[[60,35],[70,20],[78,28],[82,28],[90,35],[110,30]],"shroudThickness":0.25,
#     "outputPath":"/home/vance/Downloads/tunnel_23.med"
#     }
    
    createTunnel(defaultMap['outputPath'],defaultMap,doGUI=False)
    print "Tunnel created!"
