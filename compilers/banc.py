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

import os,sys,re

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
		self.frettingCode = equates["fretting"]
		self.beats = int(equates["beats"])
		self.fretting = "....."

	def translate(self,barDef):
		self.bar = [ None ] * (self.beats * 4)
		self.pos = 0
		self.lastNote = None

		barDef = barDef.lstrip()
		while barDef != "":
			barDef = self.processOne(barDef).lstrip()
		return "/".join([self.render(x) for x in self.bar])

	def processOne(self,df):

		if df[0] == "&":															# single rest.
			self.pos += 1
			return df[1:]

		if df[0] == "+" or df[0] == "-" or df[0] == ">":							# modifier.
			assert self.lastNote is not None,"No note to modify"
			self.bar[self.lastNote]["modifier"] = df[0]
			self.bar[self.lastNote]["modcount"] += 1
			return df[1:]

		if df[0] >= '1' and df[0] <= '5':
			self.default()
			f = self.fretting[int(df[0])-1]
			f = f if f != '.' else "0"
			self.bar[self.pos]["play"][int(df[0])-1] = self.frettingCode.find(f)
			self.lastNote = self.pos
			self.pos += 1
			return df[1:]

		if df[0] == '!':
			self.default()
			if self.pos % 2 == 0:
				for i in range(0,5):
					f = self.frettingCode.find(self.fretting[i])
					if f >= 0:
						self.bar[self.pos]["play"][i] = f
			else:
				self.bar[self.pos]["play"][4] = 0
			self.pos += 1
			return df[1:]

		m = re.match("^\[(["+self.frettingCode+"\.]*)\](.*)$",df)					# check for [frets]
		if m is not None:
			self.fretting = m.group(1)
			assert len(self.fretting) == 5,"Bad fretting "+df
			return m.group(2)

		m = re.match("^\((.*?)\)(.*)$",df)											# check for (<chord>)
		if m is not None:
			self.default()
			self.bar[self.pos]["chord"] = m.group(1)
			return m.group(2)

		assert False,"Cannot process '"+df+"'"										# give up.

	def default(self):
		if self.bar[self.pos] is None:
			self.bar[self.pos] = { "play":[None]*5,"chord":None,"modifier":None,"modcount":0 }

	def render(self,bar):
		r = ""
		if bar is not None:
			if bar["chord"] is not None:
				r = r + "("+bar["chord"]+")"
			if bar["play"] is not None:
				for s in range(0,5):
					if bar["play"][s] is not None:
						r = r + chr(s+49)+chr(bar["play"][s]+65)
						if bar["modifier"] is not None:
							r = r + bar["modifier"] * bar["modcount"]
		return r

# ***************************************************************************************************
#									Compiler class
# ***************************************************************************************************

class BanjoCompiler(object):
	def __init__(self):
		pass

	def compile(self,sourceFile,targetFile):
		sourceFile = sourceFile.replace("/",os.sep)									# Handle slashes.
		targetFile = targetFile.replace("/",os.sep)
		print("Compiling {0} to {1}".format(sourceFile,targetFile))

		if not os.path.isfile(sourceFile):											# check file exists
			return "File "+sourceFile+" cannot be found"
		src = [x.strip().replace("\t"," ") for x in open(sourceFile).readlines()]	# read source in
		src = [x if x.find("//") < 0 else x[:x.find("//")].strip() for x in src]	# remove comments
		src = [x.lower() for x in src]												# make everything LC

		equates = { "format":"0" }													# work out equates.
		equates["beats"] = "4" 														# standard beats/bar
		equates["fretting"] = "0123456789tewhufxvgn"								# standard fretting

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
		err = None
		for k in equates.keys():													# output the defined equates
			hOut.write(".{0}:={1}\n".format(k,equates[k]))
		for i in range(0,len(src)):													# work through the source.
			for bar in [x.strip() for x in src[i].split("|") if x.strip() != ""]:	# split into bars
				try:
					cvt = trans.translate(bar).lower()								# translate it
					cvt = cvt if cvt != "" else "/"									# non empty if empty
					#print(bar,cvt)
					#assert cvt.count("/") <= 8,"Too many beats"
					hOut.write("|"+cvt+"\n")										# write out
				except AssertionError as e:											# if translator fails.
					err = "Error '{0}' at {1}".format(e.args[0],i+1)
					return err
				barCount += 1
		#print("\tCompiled {0} bars.".format(barCount))
		hOut.close()
		return err

if __name__ == "__main__":
	err = BanjoCompiler().compile("./cripple.banjo","../agkbanjo/music/__test.plux")
	print(err)
	if err is not None:
		print(err)
