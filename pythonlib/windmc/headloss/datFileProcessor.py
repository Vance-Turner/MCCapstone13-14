'''
This file processes a dat file to look for velocity data.
'''

'''
The points we are interested are the velocity at (x,y,z)=(startX,0,0) and (x,y,z)=(endX,0,0)
'''
def twoColumnProcessor(path,upStreamVelocColumn=1,downStreamVelocColumn=2):
	datFile = file(path,'r')
	# We ignore all lines that start with #
	# These 
	previousLine = ""
	for line in datFile:
		if line[0]=="#":
			# ignore such lines
			pass
		previousLine = line

	print "Previous line>",previousLine
	# Ok, now we have the last line of data, there are three spaces at the beginning
	pieces = previousLine.split("  ")
	print "Previous line pieces>",pieces
	upStreamVeloc = pieces[upStreamVelocColumn+1]
	downStreamVeloc = pieces[downStreamVelocColumn+1]
	
	# Now process the number
	parts = upStreamVeloc.split("e")
	base = float(parts[0])
	exp = float(parts[1])
	upStreamVeloc = base*(10**exp)

	parts = downStreamVeloc.split("e")
	base = float(parts[0])
	exp = float(parts[1])
	downStreamVeloc = base*(10**exp)
	datFile.close()
	return [upStreamVeloc,downStreamVeloc]

			
# Test this...
if __name__ == "__main__":
	path ="/home/vance/Downloads/Capstone/MCCapstone13-14/CFDTut/BetzLimitTesting/betzlimit_testing_basic/RESU/20131204-2352/monitoring/probes_VelocityX.dat"
	print twoColumnProcessor(path)
