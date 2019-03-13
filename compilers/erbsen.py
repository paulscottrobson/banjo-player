# ***************************************************************************************************
# ***************************************************************************************************
#
#		Name:		erbsen.py
#		Purpose:	Generates variants for Wayne Erbsen's Clawhammer book
#		Date:		13th March 2019
#		Author:		Paul Robson (paul@robsons.org.uk)
#
# ***************************************************************************************************
# ***************************************************************************************************

import os,sys,re

class Bar(object):
	def __init__(self,defn):
		self.definition = defn
		self.notes = [ None ] * 4 																# notes in definition
		self.chords = [ None ] * 4 																# chords
		self.output = []																		# what is actually output
		for i in range(0,8):
			self.output.append([None,None,None,None,None,None])
		self.fretting = [ None ] * 8															# fret at this position on melody note
		self.string = [ None ] * 8 																# string at this position on melody
		self.decode(defn)																		# convert into notes
	#
	def decode(self,defn):
		self.isAll234 = True 																	# is it all string 2-4
		defn = [x for x in defn.split(" ") if x != ""]											# split up
		pos = 0 																				# current position.
		for d in defn:																			# for each note
			if d.startswith("("):																# rip any chords
				m = re.match("^\((.*?)\)(.*)$",d)
				assert m is not None,"Bad chord note "+d
				self.chords[pos] = m.group(1).lower()
				d = m.group(2)
			m = re.match("^(x*)([0-9])(-?)$",d)													# decode it
			assert m is not None,"Bad note "+d
			self.notes[pos] = [int(m.group(2)),len(m.group(1))+1] 								# set up note played
			for n in range(pos*2,8):															# update fretting
				self.fretting[n] = self.notes[pos][0]
				self.string[n] = self.notes[pos][1]
			if self.notes[pos][1] < 2 or self.notes[pos][1] > 4:								# check notes
				self.isAll234 = False
			pos = pos + (2 if m.group(3) == "" else 1) 											# advance 1 or 2
		self.is1Half = self.notes[1] is not None												# check for half beats
		self.is2Half = self.notes[3] is not None
		if self.fretting[4] > 0:
			self.fretting[3] = self.fretting[4] 												# fix for rolls on 3.
			self.string[3] = self.string[4]
	#
	def applyModifier(self,modifier,useDefault):
		doIt = not useDefault
		if modifier == "melody":																# melody.
			for i in range(0,4):
				if self.notes[i] is not None:
					self.output[i*2][self.notes[i][1]] = self.notes[i][0]
		elif modifier == "pinch":																# pinch
			if doIt or not self.is1Half:
				self.output[2][1] = 0
				self.output[2][5] = 0
			if doIt or not self.is2Half:
				self.output[6][1] = 0
				self.output[6][5] = 0
		elif modifier == "drone":																# drone
			if doIt or self.is1Half:
				self.output[1][1] = 0
				self.output[3][1] = 0
			if doIt or self.is2Half:
				self.output[5][1] = 0
				self.output[7][1] = 0
		elif modifier == "twofinger":															# two finger roll
			self.generateRoll("x151x151",useDefault,useDefault)
		elif modifier == "pegleg":																# pegleg roll
			self.generateRoll("x_51x_51",useDefault,useDefault)
		elif modifier == "forward":																# forward roll
			self.generateRoll("x15x15x1",useDefault,useDefault)
		elif modifier == "reverse":																# reverse roll
			self.generateRoll("x21512x1",useDefault,useDefault)
		elif modifier == "foggy":																# foggy mountain roll
			self.generateRoll("x1x15x15",useDefault,useDefault)
		elif modifier == "clear":
			for i in range(0,8):
				self.output[i] = [ None,None,None,None,None,None ]
		elif modifier == "chord":
			for i in range(0,4):
				if self.chords[i] is not None:
					self.loadChord(i*2,self.chords[i])
		else:
			assert False,"Unknown modifier "+modifier
		#print(self.definition,self.notes,self.fretting,self.render())
	#
	def generateRoll(self,pattern,useDefault,requires234):
		if useDefault and (self.is1Half or self.is2Half):										# default is only if 2 single beat notes
			return
		if requires234 and (not self.isAll234):													# must require 2/3/4
			return
		for i in range(0,8):																	# each note
			self.output[i] = [ None,None,None,None,None,None ]									# erase
			if pattern[i] != "_":																# put pattern in
				if pattern[i] == "x":				
					self.output[i][self.string[i]] = self.fretting[i]							# melody note
				else:
					self.output[i][int(pattern[i])] = 0											# roll note
	#
	def loadChord(self,pos,chord):
		assert chord in Bar.chords,"Unknown chord "+chord
		for i in range(1,5+1):
			self.output[pos][i] = int(Bar.chords[chord][i-1])
		self.output[pos][5] = None
	#
	def render(self):
		return ".".join([self.renderNote(n) for n in range(0,8)])
	#
	def renderNote(self,note):
		render = ""
		for i in range(1,5+1):
			if self.output[note][i] is not None:
				render += str(i)+chr(self.output[note][i]+97)
		return render

Bar.chords = { "g":"00000","c":"21010","d7":"01200","d":"43240","f":"31230" }

class ErbsenProcessor(object):
	def __init__(self,srcFile,objDirectory):
		src = [x.strip() for x in open(srcFile).readlines()]									# read file
		src = [x if x.find("#") < 0 else x[:x.find("#")].strip() for x in src]					# remove comments
		models = [x[1:].strip().replace(" ","").lower() for x in src if x.startswith("@")]		# extract variants
		src = [x.lower() for x in src if x != "" and (not x.startswith("@"))]					# get just bar data
		self.barSource = [x.strip() for x in "|".join(src).split("|") if x.strip() != ""]		# convert to bar list
		self.barCount = len(self.barSource)
		self.name = srcFile.split(os.sep)[-1][:-7].lower()										# name of tune from file
		for m in models:																		# for each variant
			parts = [x.strip() for x in m.split(":=") if x.strip() != ""]						# split into name,parts
			assert len(parts) == 2 and parts[0] != "" and parts[1] != ""						# check it
			name = self.name+"_("+parts[0]+")"
			objName = objDirectory+os.sep+name+".plux"											# target file name
			self.generate(name,objName,parts[1].split(":"))										# create it.
	#
	def generate(self,songName,targetFile,modifiers):
		print("\t\t \""+targetFile.split(os.sep)[-1]+"\".")		
		self.bars = [Bar(x) for x in self.barSource]											# create all bars
		for m in [x for x in modifiers if x != ""]:

			overrideList = None
			modifierType = m
			#print("**** "+modifierType+" ****")
			for bar in range(0,self.barCount):
				if overrideList is None:
					self.bars[bar].applyModifier(m,True)
				elif overrideList[bar+1]:
					self.bars[bar].applyModifier(m,False)

		equates = { "format":"1","beats":"2","fretting":"0123456789","notes":"8","tempo":"60" }
		equates["name"] = songName
		h = open(targetFile,"w")
		for k in equates.keys():
			h.write(".{0}:={1}\n".format(k,equates[k]))
		for b in self.bars:
			h.write("|"+b.render()+"\n")
		h.close()

if __name__ == "__main__":
	ErbsenProcessor("downtheroad.erbsen",".")
