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
		self.compileAllSources()
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
			dirName = root if root != sourceDir else "root"						# get directory name or root.
			assert dirName not in self.indexes,"Duplicate directory "+dirName 	# check directory name unique
			banjoFiles.sort()													# sort list of files/dirs
			self.indexes[dirName] = banjoFiles									# save it.
		print("Found {0} indexes.".format(len([x for x in self.indexes.keys()])))
	#
	#		Compile all sources and give them names
	#
	def compileAllSources(self):
		self.uniqueID = 1														# unique ID counter.
		self.xUniqueID = 1														# same for indices
		self.compileIndex("root","home.index")									# compile the index called root.
	#
	#		Compile the index with the given name
	#
	def compileIndex(self,name,indexFile):
		print(name,indexFile)
		assert name in self.indexes 											# check it exists - it should !
		elements = self.indexes[name]
		hIndex = open(self.targetDir+os.sep+indexFile,"w")						# create index file
		for subdir in [x for x in elements if x[-6:] != ".banjo"]:				# do all subindexes first.
			newIndexFile = "idx"+str(self.xUniqueID)+".index"
			self.xUniqueID += 1
			self.compileIndex(subdir,newIndexFile)
		for tuneFile in [x for x in elements if x[-6:] == ".banjo"]:			# do all source files next.
			targetFile = "tune"+str(self.uniqueID)+".plux"
			print(tuneFile,targetFile)
			self.uniqueID += 1
			bc = banc.BanjoCompiler()
			bc.compile(tuneFile,self.targetDir+os.sep+targetFile)
		hIndex.close()
	#
	#		Locate and compile most recently modified file as test.plux
	#
	def mostRecent(self):
		self.latestFile = None
		latestFileTime = 0
		for key in self.indexes.keys():											# scan all indexes
			for fName in [x for x in self.indexes[key] if x[-6:] == ".banjo"]:	# scan all files
				fTime = os.stat(fName).st_mtime									# get modification time
				if fTime > latestFileTime:										# update latest found
					latestFileTime = fTime
					self.latestFile = fName
		print("Most recent file "+self.latestFile+" compiled to test.plux")		# print and compile it.
		banc.BanjoCompiler().compile(self.latestFile,self.targetDir+os.sep+"test.plux")

if __name__ == "__main__":
	MusicBuilder().buildTree("../music","../agkbanjo/media/music")
