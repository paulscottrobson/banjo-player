# ***************************************************************************************
# ***************************************************************************************
#
#		Name : 		makeatlas.py
#		Author :	Paul Robson (paul@robsons.org.uk)
#		Date : 		1st February 2019
#		Purpose :	Creates Image file and sub image.
#
# ***************************************************************************************
# ***************************************************************************************

import os,sys
from PIL import Image

# ***************************************************************************************
#							Represents a single graphic object
# ***************************************************************************************

class GraphicObject:
	def __init__(self,fname):
		self.fileName = fname
		self.image = Image.open(fname)

	def width(self):
		return self.image.size[0]

	def height(self):
		return self.image.size[1]

	def render(self,atlas,x,y):
		atlas.paste(self.image,(x,y))

	def getName(self):
		return os.path.basename(self.fileName)[:-4]

	def renderSubImageFile(self,f,x,y):
		f.write("{0}:{1}:{2}:{3}:{4}\n".format(self.getName(),x,y,self.width(),self.height()))

# ***************************************************************************************
#									Packer worker class
# ***************************************************************************************

class GraphicPacker:
	def __init__(self):
		self.imageWidth = 512 															# width of atlas sheet.
		self.imageList = []																# list of images.

	def append(self,graphicObject):
		self.imageList.append({ "object":graphicObject, 								# add a new object
							"area":graphicObject.width()*graphicObject.height() })
		while graphicObject.width() > self.imageWidth:									# make the atlas wide enogh
			self.imageWidth = self.imageWidth * 2

	def pack(self,packStep = 4):
		self.atlasHeight = 0
		iList = sorted(self.imageList,key=lambda k: k['area'],reverse = True)			# list sorted largest first.
		for i in range(0,len(iList)):													# for every element.
			x = 0																		# suggested position.
			y = 0	
			isOk = False 																# set true when done.
			while not isOk:																# keep going until found.
				iList[i]["left"] = x													# save position
				iList[i]["top"] = y
				iList[i]["right"] = x + iList[i]["object"].width() 
				iList[i]["bottom"] = y + iList[i]["object"].height() 
				isOk = self.canPlace(iList[i],iList,0,i-1)								# check if it can go there
				if not isOk:															# it can't.
					x = x + packStep															# try slightly to right.
					if x + iList[i]["object"].width() >= self.imageWidth: 				# if it can't fit on this line
						x = 0															# move down.
						y = y + packStep

			self.atlasHeight = max(self.atlasHeight,iList[i]["bottom"]+2)				# update the bottom size

	def render(self,baseName):
		baseName = baseName.lower()														# all file names l/c
		atlas = Image.new("RGBA",(self.imageWidth,self.atlasHeight),(0,0,0,0))			# blue background
		for image in self.imageList:													# render all images
			image["object"].render(atlas,image["left"],image["top"])	
		atlas.save(baseName+".png",optimize=True)										# save atlas image	

		subText = open(baseName+" subimages.txt","w")									# create text
		for image in self.imageList:
			image["object"].renderSubImageFile(subText,image["left"],image["top"])
		subText.close()

	def canPlace(self,item,iList,first,last):
		for i in range(first,last+1):													# work through all.
			if self.collides(iList[i],item):											# if collision found return False
				return False
		return True 																	# No collisions return true

	def collides(self,r1,r2):															# Check two items collide.
		separate = 	r1["right"] < r2["left"] or \
					r1["left"] > r2["right"] or \
					r1["top"] > r2["bottom"] or \
					r1["bottom"] < r2["top"]
		return not separate


count = 0
gpack = GraphicPacker()
for root,dirs,files in os.walk("source"):												# source contains graphics
	for f in files:																		# for each gfx file
		count = count + 1
		fName = root + os.sep + f
		gob = GraphicObject(fName)														# create it
		gpack.append(gob)																# append it
gpack.pack()																			# pack the objects in
gpack.render("sprites")																	# output them.
print("Grabbed {0} sprites".format(count))
