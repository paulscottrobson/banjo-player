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
#									Bar Data Class
# ***************************************************************************************************

class Bar(object):
	def __init__(self,notesPerBar):
		self.bar = [ None ] * notesPerBar
		self.pos = 0
		self.lastpos = None

	def advance(self):
		assert self.pos < len(self.bar),"Too many notes in bar"
		self.pos += 1

	def rewind(self):
		assert self.pos > 0,"Can't rewind at the start"
		self.pos -= 1

	def getPos(self):
		return self.pos

	def setChord(self,chord):
		self.default()
		self.bar[self.pos]["chord"] = chord[0].upper()+chord[1:].lower() if chord != "" else ""

	def setPlay(self,fretting,string):
		self.default()
		self.bar[self.pos]["play"][string-1] = fretting
		self.lastPos = self.pos
		#print(fretting,string)

	def modify(self,modifier):
		assert self.lastPos is not None,"Trying to modify note when none given"
		self.bar[self.lastPos]["modifier"] = modifier
		self.bar[self.lastPos]["modcount"] += 1

	def default(self):
		if self.bar[self.pos] is None:
			self.bar[self.pos] = { "play":[None]*5,"chord":None,"modifier":None,"modcount":0 }

	def render(self):
		return ".".join([self.renderNote(x) for x in self.bar])

	def renderNote(self,note):
		r = ""
		if note is not None:
			if note["chord"] is not None:
				r = r + "("+note["chord"]+")"
			if note["play"] is not None:
				for s in range(0,5):
					if note["play"][s] is not None:
						r = r + chr(s+49)+chr(note["play"][s]+65)
						if note["modifier"] is not None:
							r = r + note["modifier"] * note["modcount"]
		return r

# ***************************************************************************************************
#						Translate Level 1 format, which is very simple
# ***************************************************************************************************

class Level1Compiler(object):
	def __init__(self,equates):
		self.equates = equates
		self.frettingCode = equates["fretting"]
		self.beats = int(equates["beats"])
		self.noteCount = 6 if self.beats == 3 else 8
		self.fretting = [ None ] * 5
		self.strings = [ None ] * self.noteCount
		self.stringOverride = None

	def translate(self,barDef):
		self.bar = Bar(self.noteCount)
		barDef = barDef.lower().strip()
		while barDef != "":
			barDef = self.process(barDef).strip()
		return self.bar.render()

	def process(self,df):
		if df[0] == "*":															# one note from pattern
			self.addNote(None)
			return df[1:]
		#
		if df[0] == "&":															# one note rest
			self.bar.advance()
			return df[1:]
		#
		n = self.frettingCode.find(df[0])											# single fretting
		if n >= 0:
			self.addNote(n)
			return df[1:]
		#
		if df[0] == "/" or df[0] == "+" or df[0] == "-":							# modifier
			self.bar.modify(df[0])
			self.fretting[self.lastPlayedString-1] += (-1 if df[0] == "-" else 1)
			return df[1:]
		#
		m = re.match("^\\.([1-5])(.*)$",df)											# .string override
		if m is not None:
			self.stringOverride = int(m.group(1))
			return m.group(2)
		#
		m = re.match("^{([1-5\\.]+)}(.*)$",df)										# check for {strings}
		if m is not None:
			assert len(m.group(1)) == self.noteCount,"Wrong number of strings"
			self.strings = [ None ] * self.noteCount
			for i in range(0,self.noteCount):
				if m.group(1)[i] != '.':
					self.strings[i] = int(m.group(1)[i])
			return m.group(2)
		#
		m = re.match("^\[(["+self.frettingCode+"\\.]+)\](.*)$",df)					# check for [fretting]
		if m is not None:
			assert len(m.group(1)) == 5,"Should be 5 frets in fretting" 
			self.fretting = [ None ] * 5
			for i in range(0,5):
				if m.group(1)[i] != '.':
					self.fretting[i] = self.frettingCode.find(m.group(1)[i])
			return m.group(2)
		#
		m = re.match("^\((.*?)\)(.*)$",df)											# check for (chord)
		if m is not None:
			self.bar.setChord(m.group(1))
			return m.group(2)
		assert False,"Cannot process '"+df+"'"										# give up.

	def addNote(self,overrideFret):
		string = self.strings[self.bar.getPos()]									# string we should play
		string = self.stringOverride if self.stringOverride is not None else string # string override ?
		self.stringOverride = None
		if string is not None:														# playing something
			fretting = self.fretting[string-1] if overrideFret is None else overrideFret # get fret can be overridden
			if fretting is not None:												# fretting set
				self.bar.setPlay(fretting,string)									# play that note
				self.fretting[string-1] = fretting 									# update current fretting
				self.lastPlayedString = string 										# remember what was played
				#print("last",self.lastPlayedString)
		self.bar.advance()

# ***************************************************************************************************
#									Compiler class
# ***************************************************************************************************

class BanjoCompiler(object):
	def __init__(self):
		pass

	def compile(self,sourceFile,targetFile):
		sourceFile = sourceFile.replace("/",os.sep)									# Handle slashes.
		targetFile = targetFile.replace("/",os.sep)
		print("Compiling\n\t{0}\n\t{1}".format(sourceFile,targetFile))

		if not os.path.isfile(sourceFile):											# check file exists
			return "File "+sourceFile+" cannot be found"
		src = [x.strip().replace("\t"," ") for x in open(sourceFile).readlines()]	# read source in
		src = [x if x.find("#") < 0 else x[:x.find("#")].strip() for x in src]		# remove comments
		src = [x.lower() for x in src]												# make everything LC

		equates = { "format":"0" }													# work out equates.
		equates["beats"] = "4" 														# standard beats/bar
		equates["fretting"] = "0123456789tewhufxv"									# standard fretting
		equates["notes"] = "8"														# standard notes.
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
					while bar.find("<") >= 0:
						bar = self.macroExpand(bar,equates)
					cvt = trans.translate(bar).lower()								# translate it
					cvt = cvt if cvt != "" else "/"									# non empty if empty
					#print('"'+bar+'"',cvt)
					hOut.write("|"+cvt+"\n")										# write out
				except AssertionError as e:											# if translator fails.
					err = "Error '{0}' at {1}".format(e.args[0],i+1)
					return err
				barCount += 1
		#print("\tCompiled {0} bars.".format(barCount))
		hOut.close()
		return err

	def macroExpand(self,bar,equates):
		s = re.split("(\\<.*?\\>)",bar)
		for i in range(0,len(s)):
			if s[i].startswith("<"):
				assert s[i][1:-1].lower() in equates,"Unknown macro "+s[i][1:-1]
				s[i] = equates[s[i][1:-1].lower()]
		return "".join(s)

if __name__ == "__main__":
	err = BanjoCompiler().compile("./cripple.banjo","../agkbanjo/media/music/__test.plux")
	if err is not None:
		print(err)
