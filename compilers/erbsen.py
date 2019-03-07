# ***************************************************************************************************
# ***************************************************************************************************
#
#		Name:		erbsen.py
#		Purpose:	Generates variants for Wayne Erbsen's Clawhammer book
#		Date:		7th March 2019
#		Author:		Paul Robson (paul@robsons.org.uk)
#
# ***************************************************************************************************
# ***************************************************************************************************

import os,sys,re

class ErbsenGenerator:
	def __init__(self,directory,sourceFile):
		self.directory = directory
		self.fileRoot = sourceFile[:-7]
																				# Read file and preprocess
		src = [x.replace("\t"," ").strip() for x in open(directory+os.sep+sourceFile).readlines()]
		src = [x if x.find("#") < 0 else x[:x.find("#")].strip() for x in src]
		src = [x.lower().strip() for x in src if x != ""]
		self.equates = { "beats":"2","tempo":"60","format":"1","step":"4" }		# Sort out equates
		for f in [x for x in src if x.find(":=") >= 0]:
			parts = [x.strip() for x in f.split(":=") if x.strip() != ""]
			assert len(parts) == 2
			self.equates[parts[0]] = parts[1]
		src = [x for x in src if x.find(":=") < 0]								# Remove equates
		typeList = [x for x in src if x.startswith("(") and x.endswith(")")]	# Find the list of options
		assert len(typeList) == 1
		self.typeList = [x.strip() for x in typeList[0][1:-1].split(":") if x.strip() != ""]
		src = [x for x in src if not(x.startswith("(") and x.endswith(")"))]	# remove options
																				# convert into bars in a list
		self.barSource = [x.strip() for x in "|".join(src).split("|") if x.strip() != ""]

		print(self.barSource,self.typeList)

for root,dirs,files in os.walk(".."):
	for f in [x for x in files if x.endswith(".erbsen")]:
		if f.find("road") >= 0:
			ErbsenGenerator(root,f)



