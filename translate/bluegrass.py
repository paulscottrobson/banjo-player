# ***************************************************************************************************
# ***************************************************************************************************
#
#		Name:		bluegrass.py
#		Purpose:	Class representing a tune from .banjo (BlueGrass) format
#		Date:		14th March 2019
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
#										The basic tune class
#
# ***************************************************************************************************

class BluegrassTune(BaseTune):
	#
	#		Initialise anything needed for translation
	#
	def initialiseTranslation(self):
		self.fretting = [ "0" ] * 5 											# current fretting
		self.noteCount = 8
		self.strings = [ "." ] * self.noteCount									# current strings.
	#
	#		Create bar from a format specification.
	#
	def createBar(self,definition):
		return self.decodeBar(definition)
	#
	#		Decode an element
	#
	def decode(self,bar,df):
		#
		if df[0] == "*":														# get from current settings
			string = self.strings[bar.getPos()]									# current string ?
			if string != ".":													# if one selected
				string = int(string)											# make an integer
				fretting = self.fretting[string-1]								# get fretting for string
				if fretting != ".":												# is there fretting ?
					bar.setNotes(fretting,string)								# play that note ?
			bar.movePos(1)														# advance by one.	
			return df[1:]	

		if df[0] == ".":														# . advance by one.
			bar.movePos(1)
			return df[1:]
		#
		m = re.match("^(x*)(["+Bar.FRETTING+"]+)([\\^\\/v]*)(.*)$",df)			# check for note decode.
		if m is not None:										
			bar.setNotes(m.group(2),len(m.group(1))+1)							# output the note
			for c in m.group(3).replace("^","+").replace("v","-"):				# output modifiers
				bar.modify(c)
			bar.movePos(1)														# forward 1.
			return m.group(4)
		#
		m = re.match("^\[(["+Bar.FRETTING+"\\.]+)\](.*)$",df)					# is it [fffff] ?
		if m is not None:
			if len(m.group(1)) != 5:											# must be 5 frets
				raise MusicException("Fret setting must have 5 frets "+df)
			self.fretting = [x for x in m.group(1)]								# convert to list
			return m.group(2)
		#
		m = re.match("^\(([1-5\\.]+)\)(.*)$",df)								# is it (ssssssss) ?
		if m is not None:
			if len(m.group(1)) != self.noteCount:								# must be right no of notes
				raise MusicException("String setting must have {0} frets {1}".format(self.noteCount,df))
			self.strings = [x for x in m.group(1)]								# convert to list
			return m.group(2)
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

(32313231) xx4*xx4*xx5*xx7* | xx7*xx5*xx4*xx2* | xx0*xx0*xx2*xx4* | xx4*xxxx0*xx2*xxxx0*
(32313231) xx4*xx4*xx5*xx7* | xx7*xx5*xx4*xx2* | xx0*xx0*xx2*xx4* | xx2*xxxx0***xxxx0*


""".strip()
	h = open("__test.banjo","w")
	h.write(src)
	h.close()
	BluegrassTune("__test.banjo")







