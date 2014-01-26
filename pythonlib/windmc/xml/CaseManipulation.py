__author__ = 'vance'

import xml.etree.ElementTree as ET
import math

def createProbeEL(name,x,y,z):
    probe = ET.Element('probe',{'name':str(name),'status':'on'})
    probe_x = ET.Element('probe_x')
    probe_x.text = str(x)
    probe_y = ET.Element('probe_y')
    probe_y.text = str(y)
    probe_z = ET.Element('probe_z')
    probe_z.text = str(z)
    probe.append(probe_x)
    probe.append(probe_y)
    probe.append(probe_z)
    return probe

def insertCrossSecProbe(owner,x,start,step,density,startCount):
    loc = []
    for i in range(density):
        loc.append(start+(i*step))
    print "Created locs>",loc
    const = 0
    count = startCount
    # Create the probes in positive and then negative z
    for l in loc:
       owner.append(createProbeEL(count,x,0,l))
       count+=1
    for l in loc:
       owner.append(createProbeEL(count,x,0,-l))
       count+=1

    # Create the probes in positive and then negative y
    for l in loc:
       owner.append(createProbeEL(count,x,l,0))
       count+=1
    for l in loc:
       owner.append(createProbeEL(count,x,-l,0))
       count+=1
    return count


def insertActuatorDiskTunnelProbes(caseFilePath,outputPath):
    doc = ET.parse(caseFilePath)
    root = doc.getroot()
    output = root.findall('./analysis_control/output')[0]
    for child in output.findall('probe'):
        output.remove(child)
    count = 1
    # Probe set 1
    x = 5
    count = insertCrossSecProbe(output,x,2,3,3,count)
    # Probe set 2
    x = 30
    count = insertCrossSecProbe(output,x,2,3,3,count)
    # Probe set 3, far beyond the actuator disk
    x = 60
    count = insertCrossSecProbe(output,x,2,3,3,count)
    # Insert probe at outlet
    x = 95
    count = insertCrossSecProbe(output,x,2,3,3,count)
    # Insert probe at inlet of actuator disk
    x = 49
    count = insertCrossSecProbe(output,x,1,2,4,count)
    # Insert probe in middle of actuator disk
    x = 50.05
    count = insertCrossSecProbe(output,x,1,2,4,count)
    # Insert probe at outlet of actuator disk
    x = 51
    count = insertCrossSecProbe(output,x,1,2,4,count)

    doc.write(outputPath)

if __name__=='__main__':
    print "In main"
    insertActuatorDiskTunnelProbes(\
        '/home/vance/Downloads/Capstone/MCCapstone13-14/pythonlib/cluster/code_saturne/TEMPLATES/actuator_disk_case.xml', \
        '/home/vance/Downloads/Capstone/MCCapstone13-14/pythonlib/cluster/code_saturne/TEMPLATES/actuator_disk_case_2.xml')

