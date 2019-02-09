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
		self.equates = equates
		self.currentString = 1
		self.currentBeat = 0
		self.currentChord = None
		self.fretting = "0123456789tewhofx"
		self.pending = ""

	def translate(self,barDef):
		parts = [x for x in barDef.replace(" ","").split("(") if x != ""]
		return "".join([self.translatePart(x) for x in parts])
		return barDef

	def translatePart(self,part):
		p = part.find(")")
		translate = ""
		if p >= 0:
			chord = part[:p]
			assert chord in self.equates,"Unknown chord "+chord
			self.currentChord = self.equates[chord]
			assert len(self.currentChord) == 5,"Bad chord definition "+chord
			chord = chord if chord.find(".") < 0 else chord[:chord.find(".")]
			translate = "("+chord+")"
		part = part[p+1:]
		return translate+"".join([self.encode(x) for x in part])

	def encode(self,ch):
		encode = ""
		if ch == "v":
			self.currentString += 1
			assert self.currentString <= 5,"Current string off bottom"
		elif ch == "^":
			self.currentString -= 1
			assert self.currentString >= 1,"Current string off top"
		elif ch == "$":
			self.currentString = 1
		elif ch == "+" or ch == "-" or ch == ">":
			self.pending += ch
		elif ch == "!":
			for i in range(0,5):
				ch = self.currentChord[i]
				if ch != ".":
					encode = encode + str(i+1)+chr(self.fretting.find(ch)+65)
			encode = encode + "/5A/"
		elif self.fretting.find(ch) >= 0:
			encode = str(self.currentString)+chr(self.fretting.find(ch)+65)+self.pending+"//"
			self.pending = ""
		else:
			assert False,"Unknown command "+ch
		return encode

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

		#hOut = sys.stdout

		barCount = 0
		for k in equates.keys():													# output the defined equates
			hOut.write(".{0}:={1}\n".format(k,equates[k]))
		for i in range(0,len(src)):													# work through the source.
			for bar in [x.strip() for x in src[i].split("|") if x.strip() != ""]:	# split into bars
				try:
					cvt = trans.translate(bar).lower()								# translate it
					cvt = cvt if cvt != "" else "/"
					#print(bar,cvt)
					assert cvt.count("/") <= 8,"Too many beats"
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