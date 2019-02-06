# ***************************************************************************************************
# ***************************************************************************************************
#
#		Name:		banc.py
#		Purpose:	Banjo compiler, Python 
#		Date:		5th February 2019
#		Author:		Paul Robson (paul@robsons.org.uk)
#
# ***************************************************************************************************
# ***************************************************************************************************

import os,sys,banc

class MusicBuilder(object):

	def buildTree(self,sourceDir,targetDir):
		self.targetDir = targetDir.replace("/",os.sep)
		self.scanIndexes(sourceDir)
		self.mostRecent()
	#
	#		Analyse the tree structure to produce a dictionary of indexes with files/directories.
	#
	def scanIndexes(self,sourceDir):
		self.indexes = {}														# indexes with list of files/dirs
		sourceDir = sourceDir.replace("/",os.sep)								# make valid directory
		for root,dirs,files in os.walk(sourceDir):								# scan it
			banjoFiles = [x for x in files if x[-6:] == ".banjo"]				# get banjo files
			for d in dirs:														# add any subdirectories
				banjoFiles.append(d)
			banjoFiles = [root+os.sep+x for x in banjoFiles]					# make full path name
			dirName = root.split(os.sep)[-1] if root != sourceDir else "root"	# get directory name or root.
			assert dirName not in self.indexes,"Duplicate directory "+dirName 	# check directory name unique
			banjoFiles.sort()													# sort list of files/dirs
			self.indexes[dirName] = banjoFiles									# save it.
		print("Found {0} indexes.".format(len([x for x in self.indexes.keys()])))
	#
	#		Locate and compile most recently modified file as test.plux
	#
	def mostRecent(self):
		self.latestFile = None
		latestFileTime = 0
		for key in self.indexes.keys():
			for fName in [x for x in self.indexes[key] if x[-6:] == ".banjo"]:
				fTime = os.stat(fName).st_mtime
				if fTime > latestFileTime:
					latestFileTime = fTime
					self.latestFile = fName
		print("Most recent file "+self.latestFile)
		banc.BanjoCompiler().compile(self.latestFile,self.targetDir+os.sep+"test.plux")

if __name__ == "__main__":
	MusicBuilder().buildTree("../music","../agkbanjo/media/music")
