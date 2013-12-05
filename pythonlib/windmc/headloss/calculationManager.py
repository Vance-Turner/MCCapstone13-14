'''
This manages a single calculation and reports a result
'''
import subprocess
import xml.etree.ElementTree as ET
import os
import os.path
'''
@param: basePath This should be to the directory containing the DATA and RESU directories
It should be the case directory.
'''
def startCalc(basePath,studyXMLName,headLossX,headLossY,headLossZ):
	tree = ET.parse(basePath+"/DATA/"+studyXMLName+".xml")
	root = tree.getroot()
	thermoModels = root[1]
	headLosses = thermoModels[-1]
	innerLosses = headLosses[0]
	xx = innerLosses[0]
	yy = innerLosses[1]
	zz = innerLosses[2]
	xx.text = str(headLossX)
	yy.text = str(headLossY)
	zz.text = str(headLossZ)
	tree.write(basePath+"/DATA/"+studyXMLName+"2.xml")
	subprocess.call(["code_saturne","run","--param",basePath+"/DATA/"+studyXMLName+"2.xml"])

	# Now get the results
	resultsDir = os.path.join(basePath,"RESU")
	print resultsDir
	big = None
	bigName = ""
	print "Walking>",resultsDir
	direcs = os.listdir(resultsDir)
	print "Direcs>",direcs
	for direc in direcs:
		#print os.path.join(basePath,"RESU",direc)
		if os.path.isdir(os.path.join(basePath,"RESU",direc)) and not direc=="check_mesh":
			print "Processing>",direc
			name = direc
			parts = name.split("-")
			print parts
			if big == None:
				big = int(parts[0])
				bigName = name
			elif int(parts[0]) > big:
				big = int(parts[0])
				bigName = name
	print "Got big first>",bigName
	# Now get the largest within the first index number
	big = None
	for direc in direcs:
		#print os.path.join(basePath,"RESU",direc)
		if os.path.isdir(os.path.join(basePath,"RESU",direc)) and not direc=="check_mesh" and not "OLD" in direc:
			print "Processing2>",direc
			name = direc
			parts = name.split("-")
			if parts[0]==bigName.split("-")[0]:
				if big == None:
					bigName = name
					big = int(parts[1])
				elif int(parts[1]) > big:
					big = int(parts[1])
					bigName = name
	print "The largest name!",bigName

	# Now let's get the velocity data
	from datFileProcessor import twoColumnProcessor
	data = twoColumnProcessor(os.path.join(basePath,"RESU",bigName,"monitoring","probes_VelocityX.dat"))
	print "We got the data!!>",data

	# We need to rename the directory so that code_saturen doesn't run out of space or get its working dir messed up
	import time
	subprocess.call(["mv",os.path.join(basePath,"RESU",bigName),os.path.join(basePath,"RESU",bigName+"_OLD_"+str(time.time()))])
	print "Finished code_saturne!"
	return data

# testing...
if __name__ == "__main__":
	basePath = "/home/vance/Downloads/Capstone/MCCapstone13-14/CFDTut/BetzLimitTesting/betzlimit_testing_basic"
	xmlName = "betzlimit_cylinder_basic"
	startCalc(basePath,xmlName,0.33,0.23,0.12)
