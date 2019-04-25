# ***************************************************************************************************
# ***************************************************************************************************
#
#		Name:		buildtree.py
#		Purpose:	Build all music entries in music tree and compiles most recently 
#					changed to test.plux
#		Date:		25th April 2019
#		Author:		Paul Robson (paul@robsons.org.uk)
#
# ***************************************************************************************************
# ***************************************************************************************************

import os,sys
from song import *

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
				f = Song(self.latestFile)
				f.render(targetDir,None,None,"__test.plux")

	def buildFile(self,sourceDir,targetDir,fileName,override):
		compiled = False
		if fileName[-5:] == ".blue":
			print("Compiling "+fileName)
			if not os.path.exists(targetDir):
				os.makedirs(targetDir)
			compiled = True
			f = Song(sourceDir+os.sep+fileName)
			f.renderAll(targetDir)
			self.update(sourceDir+os.sep+fileName)

	def update(self,fileName):
		time = os.stat(fileName).st_mtime
		if time > self.latestTime:
			self.latestTime = time
			self.latestFile = fileName

if __name__ == "__main__":
	MusicBuilder().buildTree("../music","../agkbanjo/media/music")
