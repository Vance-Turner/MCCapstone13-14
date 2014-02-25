ACTUATOR_TUNNEL_GEN = "ActuatorTunnelGenerator"

def createTunnel(fileName, kwargs, doGUI=False):
    '''
    @author: Vance Turnewitsch
    @date: Feb 20, 2014
    This code is to be run with salome-meca 2014.1 not an earlier version.
    '''
    import salome

    salome.salome_init()
    import GEOM
    from salome.geom import geomBuilder
    from SMESH_mechanic import SMESH

    geompy = geomBuilder.New(salome.myStudy)
    if doGUI:
        gg = salome.ImportComponentGUI("GEOM")

    import SMESH
    from salome.smesh import smeshBuilder

    # Get the parameters
    diskX = kwargs['diskX']
    diskY = kwargs['diskY']
    diskZ = kwargs['diskZ']

    diskHeight = kwargs['diskHeight']
    diskRadius = kwargs['diskRadius']
    tunnelHeight = kwargs['tunnelHeight']
    tunnelRadius = kwargs['tunnelRadius']

    tunnelFineness=kwargs['tunnelFineness']
    diskFineness=kwargs['diskFineness']

    tunnelMaxTetraSize=kwargs['tunnelMaxTetraSize']
    tunnelMinTetraSize=kwargs['tunnelMinTetraSize']
    diskMaxTetraSize=kwargs['diskMaxTetraSize']
    diskMinTetraSize=kwargs['diskMinTetraSize']

    print "Creating tunnel with following properties:",kwargs

    smesh = smeshBuilder.New(salome.myStudy)

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
    if doGUI:
        gg.createAndDisplayGO(diskCylID)

    # Make the cyliner
    origin = geompy.MakeVertex(0, 0, 0)
    tunnelCyl = geompy.MakeCylinder(origin, vx, tunnelRadius, tunnelHeight)

    # Now make the tunnel by cutting the disk from cylinder
    tunnel = geompy.MakeCut(tunnelCyl, diskCyl)
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

    # Get faces on the disk
    diskInletFace_Orig = geompy.GetShapesOnPlaneWithLocationIDs(diskCyl, geompy.ShapeType["FACE"], vx, startDiskBase, GEOM.ST_ON)[0]
    diskOutletFace_Orig = geompy.GetShapesOnPlaneWithLocationIDs(diskCyl, geompy.ShapeType["FACE"], vx,geompy.MakeVertex(50.0 + diskHeight, 0, 0),GEOM.ST_ON)[0]
    diskWallFace_Orig = geompy.GetShapesOnCylinderWithLocationIDs(diskCyl, geompy.ShapeType["FACE"], vx, startDiskBase, diskRadius,GEOM.ST_ON)[0]

    # Create the face groups of the disk
    diskInletGroup_Orig = createFaceGroup(diskCyl, 'DiskInletOrig', diskInletFace_Orig)
    diskOutletGroup_Orig = createFaceGroup(diskCyl, 'DiskOutletOrig', diskOutletFace_Orig)
    diskWallGroup_Orig = createFaceGroup(diskCyl, 'DiskWallOrig', diskWallFace_Orig)


    # Now do the meshing
    cylinderMesh = smesh.Mesh(tunnel, 'Cylinder')

    cylAlgo3D = cylinderMesh.Tetrahedron(smeshBuilder.FULL_NETGEN)
    cylAlgo3DParams = cylAlgo3D.Parameters()
    cylAlgo3DParams.SetMaxSize(tunnelMaxTetraSize)
    cylAlgo3DParams.SetMinSize(tunnelMinTetraSize)
    cylAlgo3DParams.SetFineness(tunnelFineness)
    cylAlgo3DParams.SetOptimize(True)
    print "Computing Tunnel Mesh..."
    cylinderMesh.Compute()

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
    diskMesh.Compute()

    windTunnelMesh = smesh.Concatenate([cylinderMesh.GetMesh(), diskMesh.GetMesh()], False, True, 1e-05, False,
                                       'WindTunnel')
    # Create group of volumes that make up the actuator disk
    volumeFilter = smesh.GetFilter(SMESH.VOLUME,SMESH.FT_BelongToGeom,SMESH.FT_EqualTo,diskCyl)
    volumeGroup = windTunnelMesh.GroupOnFilter(SMESH.VOLUME,'Disk',volumeFilter)
    # Ok, let's spit it out!
    # Get Information About Mesh by GetMeshInfo
    print "\nInformation about mesh by GetMeshInfo:"
    info = smesh.GetMeshInfo(windTunnelMesh)
    keys = info.keys(); keys.sort()
    for i in keys:
       print " %s : %d" % ( i, info[i] )
    # Silly salome-meca can only deal with strings not unicode types...so we have to make sure we have one.
    print "Saving MED to>",str(fileName),type(str(fileName))
    windTunnelMesh.ExportMED(str(fileName), autoDimension=False)

    if doGUI:
        salome.sg.updateObjBrowser(1)

    import runSalome
    runSalome.killLocalPort()

if __name__ == '__main__':
    # parse the arguments
    # This map holds the defaults for creating a tunnel and disk
    import json, os, sys
    print 'Args:',sys.argv
    jsonFile = os.path.join(os.path.dirname(sys.argv[0]),'actuator.json')
    print "loading json from>",jsonFile
    defaultMap = json.load(open(jsonFile,'r'))
    # defaultMap = {
    # "diskX": 50.0, "diskY": 0.0, "diskZ": 0.0,
    # "tunnelHeight": 100.0, "tunnelRadius": 15.0, "tunnelFineness": 3,
    # "tunnelMaxTetraSize": 2.5, "tunnelMinTetraSize": 0.1,
    # "diskHeight": 0.1, "diskRadius": 4.0, "diskFineness": 3,
    # "diskMaxTetraSize": 1, "diskMinTetraSize": 0.08,
    # "outputPath":"/home/vance/Downloads/tunnel_23.med"
    # }
    createTunnel(defaultMap['outputPath'],defaultMap,doGUI=False)
    print "Tunnel created!"
