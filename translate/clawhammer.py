# ***************************************************************************************************
# ***************************************************************************************************
#
#		Name:		clawhammer.py
#		Purpose:	Class representing a tune from .claw (Clawhammer) format
#		Date:		18th March 2019
#		Author:		Paul Robson (paul@robsons.org.uk)
#
# ***************************************************************************************************
# ***************************************************************************************************

import os,re,sys
from musicex import *
from bar import *
from tune import *

# ***************************************************************************************************
#
#									Clawhammer Tune class
#
# ***************************************************************************************************

class ClawhammerTune(BaseTune):
	#
	#		Initialise anything needed for translation
	#
	def initialiseTranslation(self):
		self.fretting = [ "0" ] * 5 											# current fretting
		self.noteCount = 8
		self.brushCount = 3
		self.melodyOnly = False
		self.simple = False
		if "subtype" in self.equates:
			self.melodyOnly = self.equates["subtype"] == "melody"
			self.simple = self.equates["subtype"] == "simple"
	#
	#		Create bar from a format specification.
	#
	def createBar(self,definition):
		bar = self.decodeBar(definition)
		#print(bar.toString())
		return bar
	#
	#		Decode an element
	#
	def decode(self,bar,df):
		#
		if df[0] == "&":														# Rest
			bar.movePos(2)
			return df[1:]
		#
		if df[0] == "-":														# Back
			bar.movePos(-1)
			return df[1:]
		#
		if df[0] == "!":														# brush
			if not self.melodyOnly:
				bar.setNotes("".join(self.fretting[0:self.brushCount]),1)
			bar.movePos(2)
			return df[1:]
		#
		if df[0] == ".":														# pluck
			bar.movePos(-1)
			if not self.melodyOnly:
				bar.setNotes("0",5)
			bar.movePos(1)
			return df[1:]
		#
		m = re.match("^\((.*?)\)(.*)$",df)										# chord
		if m is not None:
			bar.setDisplayChord(m.group(1))										# set display
			key = "chord."+m.group(1)
			if key not in self.equates:											# check chord defined
				raise MusicException("Chord "+m.group(1)+" unknown")
			self.fretting = [x for x in self.equates[key]]						# update it.
			return m.group(2)
		#
		m = re.match("^(x*)(["+Bar.FRETTING+"]+)([v\^\/]*)(.*)$",df)			# Note
		if m is not None:
			cString = len(m.group(1))+1											# selected string
			bar.setNotes(m.group(2),cString)									# set notes

			frettingChanged = False 											# check fretting changed.
			for f in m.group(2):												# scan each
				if f != self.fretting[cString-1]:								# changed ?
					frettingChanged = True
				cString += 1

			if frettingChanged:													# changed, clear all.
				self.fretting = [ "0" ] * 5

			cString = len(m.group(1))+1											# selected string
			if (not self.melodyOnly) and (not self.simple):	
				for f in m.group(2):											# copy new fretting in.
					self.fretting[cString-1] = f
					cString += 1

			for mo in m.group(3).replace("v","+").replace("^","-"):				# modifiers
				bar.modify(mo)

			bar.movePos(2)														# advance by two.
			return m.group(4)
		#
		raise MusicException("Cannot understand '{0}'".format(df))

if __name__ == "__main__":
	src = """
#
#		test script
#
beats := 4
tempo := 100
step := 4

x21v !.  xx158^ 2//

""".strip()
	h = open("__test.claw","w")
	h.write(src)
	h.close()
	ClawhammerTune("__test.claw").write(".",None)
	







