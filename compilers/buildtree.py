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

import os,sys,banc,erbsen

class MusicBuilder(object):

	def buildTree(self,treeDir):
		self.tree = treeDir.replace("/",os.sep)
		self.compiler = banc.BanjoCompiler()
		self.latestTime = 0
		self.latestFile = None
		for root,dirs,files in os.walk(self.tree):
			for f in [x for x in files if x[-6:] == ".banjo"]:
				print("Compiling  : \"{0}\"".format(f.split(os.sep)[-1]))
				self.buildFile(root+os.sep+f)
			for f in [x for x in files if x[-7:] == ".erbsen"]:
				print("Processing : \"{0}\"".format(f.split(os.sep)[-1]))
				erbsen.ErbsenProcessor(root+os.sep+f,root)
		print()
		print("Recent     : \"{0}\" to \"__test.plux\"".format(self.latestFile.split(os.sep)[-1]))
		result = self.compiler.compile(self.latestFile,self.tree+os.sep+"__test.plux")
		if result is not None:
			print(result)
			sys.exit(-1)

	def buildFile(self,sourceFile):
		targetFile = sourceFile[:-6]+".plux"
		self.compiler.compile(sourceFile,targetFile)
		#print("Now compiling \"{0}\".".format(sourceFile))
		fTime = os.stat(sourceFile).st_mtime
		if fTime > self.latestTime:
			self.latestTime = fTime
			self.latestFile = sourceFile

if __name__ == "__main__":
	MusicBuilder().buildTree("../agkbanjo/media/music")
