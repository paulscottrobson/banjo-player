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

import os,sys,banc

class MusicBuilder(object):

	def buildTree(self,treeDir):
		self.tree = treeDir.replace("/",os.sep)
		self.compiler = banc.BanjoCompiler()
		self.latestTime = 0
		self.latestFile = None
		for root,dirs,files in os.walk(self.tree):
			for f in [x for x in files if x[-6:] == ".banjo"]:
				print("Compiling  : \"{0}\"".format(f.split(os.sep)[-1]))
				self.buildFile(root+os.sep+f,0)
			for f in [x for x in files if x[-7:] == ".ebanjo"]:
				print("Compiling  : \"{0}\" (multiple)".format(f.split(os.sep)[-1]))
				self.buildFile(root+os.sep+f,0)
				self.buildFile(root+os.sep+f,1)
				self.buildFile(root+os.sep+f,2)
		print()
		print("Recent     : \"{0}\" to \"__test.plux\"".format(self.latestFile.split(os.sep)[-1]))
		result = self.compiler.compile(self.latestFile,self.tree+os.sep+"__test.plux",0)
		if result is not None:
			print(result)
			sys.exit(-1)

	def buildFile(self,sourceFile,modifier):
		namefix = [ "","_(straight)","_(melody)"]
		targetFile = sourceFile[:-6] if sourceFile.endswith(".banjo") else sourceFile[:-7]
		targetFile = targetFile + namefix[modifier] + ".plux"
		self.compiler.compile(sourceFile,targetFile,modifier)
		#print("Now compiling \"{0}\" \"{1}\".".format(sourceFile,targetFile))
		fTime = os.stat(sourceFile).st_mtime
		if fTime > self.latestTime:
			self.latestTime = fTime
			self.latestFile = sourceFile

if __name__ == "__main__":
	MusicBuilder().buildTree("../agkbanjo/media/music")
