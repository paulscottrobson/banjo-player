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

import os,sys

# ***************************************************************************************************
#									Exception Class
# ***************************************************************************************************

class BanjoException(Exception):
	pass

# ***************************************************************************************************
#						Translate Level 1 format, which is very simple
# ***************************************************************************************************

class Level1Compiler(object):
	def __init__(self,equates):
		self.fretting = "00000"
		self.equates = equates

	def translate(self,barDef):
		barDef = [x for x in barDef.split("[") if x.strip() != ""]					# split up into chord changes
		return "/".join([self.convert(x) for x in barDef])

	def convert(self,section):
		p = section.find("]")														# chord change
		if p >= 0:																	# if so
			chord = section[:p].strip()												# get and validate chord
			assert chord in self.equates,"Unknown chord "+chord
			self.fretting = self.equates[chord]										# set fretting
			section = section[p+1:].strip()											# rest is chord.
		return "/".join([self.oneNote(x) for x in section])							# convert the rest

	def oneNote(self,c):
		assert ".p12345".find(c) >= 0,"Unknown string/pair "+c
		if c == ".":
			return ""
		if c == "p":
			return self.encode(1)+self.encode(5)
		return self.encode(int(c))

	def encode(self,stringNo):
		return str(stringNo)+chr(65+int(self.fretting[stringNo-1]))

# ***************************************************************************************************
#									Compiler class
# ***************************************************************************************************

class BanjoCompiler(object):
	def __init__(self):
		pass

	def compile(self,sourceFile,targetFile):
		sourceFile = sourceFile.replace("/",os.sep)									# Handle slashes.
		targetFile = targetFile.replace("/",os.sep)
		#print("Compiling {0} to {1}".format(sourceFile,targetFile))

		if not os.path.isfile(sourceFile):											# check file exists
			return "File "+sourceFile+" cannot be found"
		src = [x.strip().replace("\t"," ") for x in open(sourceFile).readlines()]	# read source in
		src = [x if x.find("//") < 0 else x[:x.find("//")].strip() for x in src]	# remove comments
		src = [x.lower() for x in src]												# make everything LC

		equates = { "format":"0" }													# work out equates.
		equates["name"] = sourceFile.split(os.sep)[-1][:-6].replace("_"," ")		# default name
		for equate in [x for x in src if x.find(":=") >= 0]:						# search for them
			parts = [x.strip() for x in equate.split(":=")]							# split around :=
			if parts[0] == "" or len(parts) != 2:
				raise BanjoException("Bad equate "+equate)
			equates[parts[0]] = parts[1]											# update equates hash
		src = [x for x in src if x.find(":=") < 0]									# remove equates.

		if equates["format"] == "1":												# workout the compiler/translator
			trans = Level1Compiler(equates)
		else:
			raise BanjoException("Bad source format "+equates["format"])
		#print("\tUsing format {0}.".format(equates["format"]))

		try:
			hOut = open(targetFile,"w")												# open target file.
		except FileNotFoundError as e:
			return "Cannot open "+targetFile+" to write."

		barCount = 0
		for k in equates.keys():													# output the defined equates
			hOut.write(".{0}:={1}\n".format(k,equates[k]))
		for i in range(0,len(src)):													# work through the source.
			for bar in [x.strip() for x in src[i].split("|") if x.strip() != ""]:	# split into bars
				try:
					cvt = trans.translate(bar).lower()								# translate it
					assert cvt.count("/") < 8,"Too many beats"
					hOut.write("|"+cvt+"\n")										# write out
				except AssertionError as e:											# if translator fails.
					return "Error '{0}' at {1}".format(e.args[0],i+1)
				barCount += 1
		#print("\tCompiled {0} bars.".format(barCount))
		hOut.close()
		return None

if __name__ == "__main__":
	err = BanjoCompiler().compile("./cripple.banjo","../agkbanjo/music/cripple.plux")
	if err is not None:
		print(err)