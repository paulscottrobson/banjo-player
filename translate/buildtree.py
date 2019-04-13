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

	def buildTree(self,treeDir):
		self.tree = treeDir.replace("/",os.sep)
		self.latestTime = 0
		self.latestFile = None
		for root,dirs,files in os.walk(self.tree):
			for f in files:
				self.buildFile(root,f,None)
		print()
		if self.latestFile is not None:
			print("Newest file: __test.plux")
			self.buildFile(self.latestFile[0],self.latestFile[1],"../agkbanjo/media/music/__test.plux")

	def buildFile(self,directory,fileName,override):
		compiled = False
		if fileName[-5:] == ".claw":
			compiled = True
			ClawhammerTune(directory+os.sep+fileName).write(directory,override)
			ClawhammerTune(directory+os.sep+fileName,{ "subtype":"melody" }).write(directory,override)
			ClawhammerTune(directory+os.sep+fileName,{ "subtype":"basic" }).write(directory,override)
		if fileName[-6:] == ".banjo":
			compiled = True
			BluegrassTune(directory+os.sep+fileName).write(directory,override)

		if fileName[-7:] == ".clawex":
			compiled = True
			ClawhammerTune(directory+os.sep+fileName).write(directory,override)

		if compiled:
			#print(">>>",directory,fileName,override)
			print("Compiling "+fileName)
			fTime = os.stat(directory+os.sep+fileName).st_mtime
			if fTime > self.latestTime:
				self.latestTime = fTime
				self.latestFile = [directory,fileName]

if __name__ == "__main__":
	MusicBuilder().buildTree("../agkbanjo/media/music")
