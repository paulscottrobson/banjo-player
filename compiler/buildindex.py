# ***************************************************************************************************
# ***************************************************************************************************
#
#		Name:		buildindex.py
#		Purpose:	Build all index files
#		Date:		9th February 2019
#		Author:		Paul Robson (paul@robsons.org.uk)
#
# ***************************************************************************************************
# ***************************************************************************************************

import re,os,sys,shutil

# ***************************************************************************************************
#								Index building class
# ***************************************************************************************************

class BuildIndex(object):

	def build(self,baseDirectory):
		self.lastMTime = 0
		self.lastFile = None

		for root,dirs,files in os.walk(baseDirectory):
			files = [x for x in files if x.endswith(".plux") and not x.startswith("__") and not x.endswith(".txt")]
			dirs = [x for x in dirs if not x.startswith("__")]
			files.sort()
			dirs.sort()
			self.buildOneIndex(baseDirectory,root,files,dirs)

		if self.lastFile is not None:
			self.copyFile(self.lastFile,baseDirectory+os.sep+"__test.plux")

	def buildOneIndex(self,stem,root,files,dirs):		
		root = root.replace("\\","/")
		#print(root,files,dirs)
		h = open((root+os.sep+"index.txt").replace("/",os.sep),"w")
		h.write("//\n// "+root+"\n//\n")
		for f in dirs:
			h.write(f+"\n")
			h.write(self.process(f)+" (folder)\n")
		for f in files:
			h.write(f+"\n")
			h.write(self.process(f[:-5])+"\n")
			fileName = root + os.sep + f
			time = os.stat(fileName).st_mtime
			if time > self.lastMTime:
				self.lastMTime = time
				self.lastFile = fileName
		h.close()

	def process(self,s):
		s = [x for x in s.replace("_"," ").split(" ") if x != ""]
		s = [x[0].upper()+x[1:].lower() for x in s]
		return " ".join(s)

	def copyFile(self,src,tgt):
		print("Last modified file "+src)
		shutil.copyfile(src,tgt)		

if __name__ == "__main__":
	BuildIndex().build("../agkbanjo/media/music")
	