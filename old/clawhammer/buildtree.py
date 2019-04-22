# ***************************************************************************************************
# ***************************************************************************************************
#
#		Name:		buildtree.py
#		Purpose:	Build all music entries in music tree and compiles most recently 
#					changed to test.plux
#		Date:		8th February 2019
#		Author:		Paul Robson (paul@robsons.org.uk)
#
# ***************************************************************************************************
# ***************************************************************************************************

import os,sys
from tune import *

class MusicBuilder(object):

	def __init__(self):
		self.latestTime = 0
		self.latestFile = None

	def buildTree(self,sourceDir,targetDir):
		self.sourceDir = sourceDir.replace("/",os.sep)
		self.targetDir = targetDir.replace("/",os.sep)

		for root,dirs,files in os.walk(self.sourceDir):
			for f in files:
				target = self.targetDir + root[len(self.sourceDir):]
				self.buildFile(root,target,f,None)

		if self.latestFile is not None:
			print("Recompiling "+self.latestFile)
			f = ClawHammerTune()
			f.loadFile(self.latestFile)
			f.write(self.targetDir+os.sep+"__test.plux","w")

	def buildFile(self,sourceDir,targetDir,fileName,override):
		compiled = False
		if fileName[-5:] == ".claw":
			print("Compiling "+fileName)
			if not os.path.exists(targetDir):
				os.makedirs(targetDir)
			compiled = True
			f = ClawHammerTune()
			f.loadFile(sourceDir+os.sep+fileName)
			targetFile = ".".join((targetDir+os.sep+fileName).split(".")[:-1])+".plux"
			print(sourceDir+os.sep+fileName,targetFile)
			f.write(targetFile)
			self.update(sourceDir+os.sep+fileName)

	def update(self,fileName):
		time = os.stat(fileName).st_mtime
		if time > self.latestTime:
			self.latestTime = time
			self.latestFile = fileName

if __name__ == "__main__":
	MusicBuilder().buildTree("../music","../agkbanjo/media/music")
