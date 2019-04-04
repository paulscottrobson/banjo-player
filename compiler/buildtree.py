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

	def buildTree(self,treeDir):
		self.tree = treeDir.replace("/",os.sep)
		for root,dirs,files in os.walk(self.tree):
			for f in files:
				self.buildFile(root,f,None)

	def buildFile(self,directory,fileName,override):
		compiled = False
		if fileName[-10:] == ".bluegrass":
			print("Compiling "+fileName)
			compiled = True
			f = BluegrassTune()
			f.readFile(directory+os.sep+fileName)
			f.renderAll(directory)

if __name__ == "__main__":
	MusicBuilder().buildTree("../agkbanjo/media/music")
