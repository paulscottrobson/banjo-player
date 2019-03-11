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
	def __init__(self,notesPerBar = 8):
		self.bar = [ None ] * notesPerBar											# Bar notes
		self.pos = 0																# Position in bar
		self.lastpos = None 														# Last position played

	def movePos(self,count = 1):													# change position
		self.pos += count

	def getPos(self):																# get position
		return self.pos

	def setCurrentFretting(self,fretting):											# update all fretting
		assert len(fretting) == 5
		for i in range(0,5):
			self.setPlay(fretting[i],i+1,False)

	def getCurrentFretting(self):													# get all fretting
		return Bar.fretting

	def setDisplayChord(self,chord):												# set chord displayed
		self.__default()
		chord = chord.strip()
		self.bar[self.pos]["chord"] = chord[0].upper()+chord[1:].lower() if chord != "" else ""

	def setPlay(self,fretting,string,playIt = True):								# set individual fret for string, playing it if required
		assert string >= 1 and string <= 5
		if fretting is not None:
			assert (fretting >= 0 and fretting <= 16) 
		assert self.pos >= 0 and self.pos < len(self.bar),"Too many notes"
		if fretting is not None and playIt:
			self.__default()
			self.bar[self.pos]["play"][string-1] = fretting
			self.lastPos = self.pos
		Bar.fretting[string-1] = fretting

	def modify(self,modifier):														# apply modifier to last played note(s)
		assert self.lastPos is not None,"Trying to modify note when none given"
		assert "/+-".find(modifier) >= 0,"Unknown modifier"
		self.bar[self.lastPos]["modifier"] = modifier
		self.bar[self.lastPos]["modcount"] += 1

	def __default(self):
		if self.bar[self.pos] is None:												# set to default empty
			self.bar[self.pos] = { "play":[None]*5,"chord":None,"modifier":None,"modcount":0 }

	def render(self):
		return ".".join([self.__renderNote(x) for x in self.bar])					# render and join notes

	def __renderNote(self,note):													# render a note
		r = ""	
		if note is not None:
			if note["chord"] is not None:											# chord if present
				r = r + "("+note["chord"]+")"
			if note["play"] is not None:											# add all played notes
				for s in range(0,5):
					if note["play"][s] is not None:
						r = r + chr(s+49)+chr(note["play"][s]+65)
						if note["modifier"] is not None:							# modifying them.
							r = r + note["modifier"] * note["modcount"]
		return r

Bar.fretting = [ None ] * 5															# Current fretting

# ***************************************************************************************************
#						Translate Level 1 format, which is very simple
# ***************************************************************************************************

class Level1Compiler(object):
	def __init__(self,equates):
		self.equates = equates
		self.frettingCode = equates["fretting"]
		self.beats = int(equates["beats"])
		self.noteCount = int(equates["notes"])
		self.currentStrings = [ None ] * self.noteCount

	def translate(self,barDef):
		self.bar = Bar(self.noteCount)
		barDef = barDef.lower().strip()
		while barDef != "":
			barDef = self.process(barDef).strip()
		return self.bar.render()

	def process(self,df):
		#
		if df[0] == '.':															# advance one don't play.
			self.bar.movePos(1)
			return df[1:]
		#
		if df[0] == "*" or self.frettingCode.find(df[0]) >= 0:						# sequence note or override
			pos = self.bar.getPos()
			if self.currentStrings[pos] is not None:
				cString = self.currentStrings[pos]
				fretting = self.bar.getCurrentFretting()[cString-1]
				if df[0] != '*':
					fretting = self.frettingCode.find(df[0])
				self.bar.setPlay(fretting,cString)
			self.bar.movePos(1)
			return df[1:]
		#
		m = re.match("^\[(["+self.frettingCode+"\\.]+)\](.*)$",df)					# [fffff] set fretting		
		if m is not None:
			assert len(m.group(1)) == 5,"Has to be 5 fret positions in a fret setting"
			frets = [self.frettingCode.find(x) for x in m.group(1)]					# decode frets
			frets = [x if x >= 0 else None for x in frets]							# ., which will be -1 => None
			self.bar.setCurrentFretting(frets)										# update fretting
			return m.group(2)
		#
		m = re.match("^\{([1-5\\.]+)\}(.*)$",df)									# {ssssssss} set strings
		if m is not None:
			assert len(m.group(1)) == self.noteCount,"Wrong number of notes in string set"
			self.currentStrings = [int(x) if x != "." else None for x in m.group(1)]
			return m.group(2)
		#
		m = re.match("^\((.*?)\)\s*(.*)$",df)										# check for chord
		if m is not None:
			self.bar.setDisplayChord(m.group(1))
			return m.group(2)	
		#
		assert False,"Cannot process \""+df+"\""									# give up.


# ***************************************************************************************************
#									Compiler class
# ***************************************************************************************************

class BanjoCompiler(object):
	def __init__(self):
		pass

	def compile(self,sourceFile,targetFile):
		sourceFile = sourceFile.replace("/",os.sep)									# Handle slashes.
		targetFile = targetFile.replace("/",os.sep)
		#print("Compiling\n\t{0}\n\t{1}".format(sourceFile,targetFile))

		if not os.path.isfile(sourceFile):											# check file exists
			return "File "+sourceFile+" cannot be found"
		src = [x.strip().replace("\t"," ") for x in open(sourceFile).readlines()]	# read source in
		src = [x if x.find("#") < 0 else x[:x.find("#")].strip() for x in src]		# remove comments
		src = [x.lower() for x in src]												# make everything LC

		equates = {}
		equates["format"] = "1" 													# standard format
		equates["beats"] = "4" 														# standard beats/bar
		equates["fretting"] = "0123456789tewhufs"									# standard fretting
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
			line = src[i]
			while line.find("<") >= 0:
					line = self.macroExpand(line,equates)
			for bar in [x.strip() for x in line.split("|") if x.strip() != ""]:		# split into bars			
				try:
					cvt = trans.translate(bar).lower()								# translate it
					cvt = cvt if cvt != "" else "/"									# non empty if empty
					#print('"'+bar+'"',cvt)
					hOut.write("|"+cvt+"\n")										# write out
				except AssertionError as e:											# if translator fails.
					if len(e.args) == 0:
						raise e
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
				original = s[i]
				assert s[i][1:-1].lower() in equates,"Unknown macro "+s[i][1:-1]
				s[i] = equates[s[i][1:-1].lower()]
		return "".join(s)

if __name__ == "__main__":
	err = BanjoCompiler().compile("./cripple.banjo","../agkbanjo/media/music/__test.plux")
	if err is not None:
		print(err)
