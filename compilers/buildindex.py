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

import re,os,sys

# ***************************************************************************************************
#								Index building class
# ***************************************************************************************************

class BuildIndex(object):

	def build(self,baseDirectory):
		for root,dirs,files in os.walk(baseDirectory):
			files = [x for x in files if not x.endswith(".banjo") and not x.startswith("__") and not x.endswith(".txt")]
			dirs = [x for x in dirs if not x.startswith("__")]
			files.sort()
			dirs.sort()
			if len(files) + len(dirs) > 0:
				self.buildOneIndex(baseDirectory,root,files,dirs)

	def buildOneIndex(self,stem,root,files,dirs):		
		root = root.replace("\\","/")
		print(root,files,dirs)
		h = open((root+os.sep+"index.txt").replace("/",os.sep),"w")
		h.write("//\n// "+root+"\n//\n")
		for f in dirs:
			h.write(f+"\n")
			h.write(self.process(f)+" (folder)\n")
		for f in files:
			h.write(f+"\n")
			h.write(self.process(f[:-5])+"\n")
		h.close()

	def process(self,s):
		s = [x for x in s.replace("_"," ").split(" ") if x != ""]
		s = [x[0].upper()+x[1:].lower() for x in s]
		return " ".join(s)

if __name__ == "__main__":
	BuildIndex().build("../agkbanjo/media/music")
	