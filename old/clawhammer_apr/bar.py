# ***************************************************************************************************
# ***************************************************************************************************
#
#		Name:		bar.py
#		Purpose:	Bar class
#		Date:		24th April 2019
#		Author:		Paul Robson (paul@robsons.org.uk)
#
# ***************************************************************************************************
# ***************************************************************************************************

import re

from musicex import *

# ***************************************************************************************************
#
#					A pluck is a single fretted note played on a single string
#
# ***************************************************************************************************

class Pluck(object):
	def __init__(self,fret,string):
		self.fret = fret
		self.string = string 
		self.isModified = False
	#
	def getFretting(self):
		return self.endFret if self.isModified else self.fret
	def getString(self):
		return self.string
	#
	def setModify(self,isSlide,endFret):
		self.isModified = True
		self.isSlide = isSlide
		self.endFret = endFret
	#
	def render(self):
		base = str(self.string)+chr(self.fret+97)
		if self.isModified:
			c = "/" if self.isSlide else ("v" if self.endFret > self.fret else "^")
			base = base + c * abs(self.endFret-self.fret)
		return base
	#
	def toString(self):
		s = str(self.fret)
		if self.isModified:
			s = s + ("/" if self.isSlide else "-")+str(self.endFret)
		return s + "."+str(self.string)

# ***************************************************************************************************
#
#											Bar class
#
# ***************************************************************************************************

class Bar(Exception):
	#
	def __init__(self,barNumber,descriptor,keys = {},notes = 4):
		self.descriptor = descriptor										# Save standards
		self.barNumber = barNumber
		self.notes = notes
		self.keys = keys
		self.alternateDescriptor = None 									# Alternate description
		self.generate([0,0,0,0,0])											# Create it.
	#
	#		Create a bar array.
	#
	def generate(self,startFretting):
		MusicException.Number = self.barNumber 								# set up for errors
		self.pos = 0 														# current beat position.
		self.pluckCount = [ 0 ] * (self.notes * 2)							# Plucks in each half note
		self.chords = [ None ] * (self.notes * 2)							# Chords here.
		self.plucks = []													# Actual plucks each half note
		self.startFretting = [x for x in startFretting]						# initial fretting.		
		for i in range(0,self.notes*2):
			self.plucks.append([None,None,None,None,None])					# strings 1-5 offset by 1
		definition = self.descriptor 										# get the descriptor.
		if self.alternateDescriptor is not None:
			definition = self.alternateDescriptor
		definition = definition.replace("\t"," ").strip().lower()			# preprocess.
		while definition != "":												# process everything.
			definition = self.processDefinition(definition).strip()			# until done
	#
	#		Process one element
	#
	def processDefinition(self,d):
		# 
		if d.startswith("&"):												# & rest
			self.pos += 2
			return d[1:]
		#
		if d.startswith("."):												# . pluck
			if self.pos == 0 or self.pos > self.notes*2:
				raise MusicException("Cannot put pluck here")
			self.plucks[self.pos-1][4] = Pluck(0,5)
			return d[1:]
		#
		if d.startswith("!"):												# ! pling.
			self.createBrush()
			self.pos += 2
			return d[1:]
		#
		m = re.match("^\\((.*?)\\)(.*)$",d)									# (chord)
		if m is not None:
			if self.pos >= self.notes*2:
				raise MusicException("Cannot put chord here")
			if "chord_"+m.group(1) not in self.keys:
				raise MusicException("Unknown chord '{0}'".format(m.group(1)))
			self.chords[self.pos] = m.group(1)
			return m.group(2)
		#
		m = re.match("^(x*)(["+Bar.FRETTING+"]+)(.*)$",d)					# xxxfff fretting.
		if m is not None:
			self.writePlucks(1+len(m.group(1)),m.group(2))					# output it.
			self.pos += 2 													# advance.
			return m.group(3)
		#
		m = re.match("^([hp\\/])(["+Bar.FRETTING+"])(.*)$",d)				# [HP/][Fret]
		if m is not None:
			self.modifyLastFret(m.group(1) == "/",Bar.FRETTING.find(m.group(2)))
			return m.group(3)
		#
		raise MusicException("Do not understand '{0}'".format(d))
	#
	#		Write Notes
	#
	def writePlucks(self,string,frets):
		if self.pos >= self.notes * 2:										# no space
			raise MusicException("Bar overflow")
		for f in frets:														# for each fretting
			if string < 1 or string > 5:									# validate string
				raise MusicException("Does not fit on string")
			fretID = Bar.FRETTING.find(f)									# convert and check
			if fretID < 0:
				raise MusicException("Bad fretting '{0}'".format(frets))				
			self.plucks[self.pos][string-1] = Pluck(fretID,string)			# add to music.
			self.pluckCount[self.pos] += 1
			string += 1
	#
	#		Modify the last fret
	#
	def  modifyLastFret(self,isSlide,endPosition):
		print(self.pos,self.pluckCount)
		if self.pos == 0 or self.pluckCount[self.pos-2] != 1:				# must be one note.
			raise MusicException("Previous note must be one pluck only")
		for s in range(0,5):												# find the one to slide
			if self.plucks[self.pos-2][s] is not None:
				self.plucks[self.pos-2][s].setModify(isSlide,endPosition)
	#
	#		Create a brush here.
	#
	def createBrush(self):
		brushFretting = self.getCurrentEndFretting()						# fretting here
		self.plucks[self.pos] = [ None,None,None,None,None ]				# erase anything here.
		for s in range(0,3):												# copy plucks in.
			self.plucks[self.pos][s] = Pluck(brushFretting[s],s+1)
	#
	#		Get the fretting at the current end point.
	#
	def getCurrentEndFretting(self):
		fretting = [x for x in self.startFretting]							# start with this.
		for i in range(0,self.notes * 2):									# check all including this (for chord)
			if self.pluckCount[i] != 0:										# only if something here.
				overwrite = False
				for s in range(0,4):										# check for overwriting
					if self.plucks[i][s] is not None:						# some pluck here.
						newNote = self.plucks[i][s].getFretting()			# changed to ...
						if newNote != fretting[s]:							# if changed overwrite all
							overwrite = True
				if overwrite:												# if overwritten do everything
					fretting = [self.plucks[i][s].getFretting() if self.plucks[i][s] is not None else 0 for s in range(0,5)]
			if self.chords[i] is not None:									# chord.
				chord = self.keys["chord_"+self.chords[i]]+"0"				# get chord and check it
				if len(chord) != 5 or re.match("^["+Bar.FRETTING+"]+$",chord) is None:		
					raise MusicException("Bad chord definition "+self.chords[i])					
				fretting = [Bar.FRETTING.find(c) for c in chord] 			# update current					
		return fretting
	#
	#		Render
	#
	def render(self):
		return ".".join([self.__render(x) for x in range(0,self.notes*2)])
	def __render(self,p):
		return "".join([x.render() if x is not None else "" for x in self.plucks[p]])
	#
	#		Convert to string
	#
	def toString(self):
		return "\n".join([str(x+1)+self.__toString(x) for x in range(-1,5)])
	def __toString(self,s):
		return "|"+"".join([self.__toString2(hb,s) for hb in range(0,self.notes*2)])+"|"
	def __toString2(self,pos,s):
		if s < 0:
			s = "" if self.chords[pos] is None else self.chords[pos][0].upper()+self.chords[pos][1:].lower()
			pad = " "
		else:
			pluck = self.plucks[pos][s]
			s = "." if pluck is None else pluck.toString()
			pad = "-"
		while len(s) < 9:
			s = pad+s+pad
		return s[:9]

Bar.FRETTING = "0123456789nlwtufsv"											# Fret representations

if __name__ == "__main__":
	b = Bar(1,"5 & x2P0 xx3.")
	print(b.toString())
	print(b.render())
	print("==================================")
	b = Bar(1,"123 !. x1/5 !.")
	print(b.toString())
	print(b.render())
	print("==================================")
	b = Bar(1,"123 !. & (C)!.",{"chord_c":"2000" })
	print(b.toString())
	print(b.render())
