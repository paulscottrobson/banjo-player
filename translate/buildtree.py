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
from clawhammer import *
from bluegrass import *

class MusicBuilder(object):

	def buildTree(self,sourceDir,targetDir):
		self.sourceDir = sourceDir.replace("/",os.sep)
		self.targetDir = targetDir.replace("/",os.sep)
		self.latestTime = 0
		self.latestFile = None
		for root,dirs,files in os.walk(self.sourceDir):
			for f in files:
				targetDir = self.targetDir+root[len(self.sourceDir):]
				self.buildFile(root,targetDir,f,None)
		print()
		if self.latestFile is not None:
			print("Newest file: {0} __test.plux".format(self.latestFile[1].split(os.sep)[-1]))
			self.buildFile(self.latestFile[0],"",self.latestFile[1],"../agkbanjo/media/music/__test.plux")

	def buildFile(self,sourceDir,targetDir,fileName,override):
		if not os.path.exists(targetDir) and targetDir != "":
			os.makedirs(targetDir)
		compiled = False
		if fileName[-5:] == ".claw":
			compiled = True
			ClawhammerTune(sourceDir+os.sep+fileName).write(targetDir,override)
			ClawhammerTune(sourceDir+os.sep+fileName,{ "subtype":"melody" }).write(targetDir,override)
			ClawhammerTune(sourceDir+os.sep+fileName,{ "subtype":"basic" }).write(targetDir,override)

		if fileName[-6:] == ".banjo":
			compiled = True
			BluegrassTune(sourceDir+os.sep+fileName).write(targetDir,override)

		if fileName[-7:] == ".clawex":
			compiled = True
			ClawhammerTune(sourceDir+os.sep+fileName).write(targetDir,override)

		if compiled:
			#print(">>>",sourceDir,fileName,override)
			print("Compiling "+fileName)
			fTime = os.stat(sourceDir+os.sep+fileName).st_mtime
			if fTime > self.latestTime:
				self.latestTime = fTime
				self.latestFile = [sourceDir,fileName]

if __name__ == "__main__":
	MusicBuilder().buildTree("../music","../agkbanjo/media/music")
