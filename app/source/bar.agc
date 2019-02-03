// ******************************************************************************************************
//
//		Name: 		bar.agc
//		Date: 		3rd February 2019
//		Author:		Paul Robson (paul@robsons.org.uk)
//		Purpose:	Bar storage and rendering class
//
// ******************************************************************************************************

type Note
	finger as String 							// T M I or space (no note)
	fretting as integer[5]						// Fretting position, -1 = don't play.
endtype

type Bar
	x as integer								// Position of bar
	y as integer
	width as integer							// Size
	height as integer 
	baseID as integer 							// First used ID
	nextFreeID as integer 						// Next available ID
	beats as integer 							// Beats in bar
	notes as Note[1]							// Notes in bar
endtype

global Bar_typeID as integer = 10000 			// next free bar ID
global Bar_rectID as integer = 0 				// Rectangle ID
global Bar_fontID as integer 					// Font ID

function Bar_Initialise(this ref as Bar,x as integer,y as integer,width as integer,height as integer)
	if Bar_rectID = 0 							// Load required graphic
		Bar_rectID = LoadImage("rectangle.png")
		Bar_fontID = LoadImage("font.png")
	endif
	this.x = x 									// Set everything up.
	this.y = y
	this.width = width
	this.height = height
	this.baseID = Bar_typeID
	this.nextFreeID = this.baseID
	this.beats = 4								// 4 notes in each bar
	this.notes.length = this.beats * 2 - 1		// Set up the notes array.
	for i = 0 to this.notes.length				// Set all notes to 'don't play'
		this.notes[i].finger = chr(i+65)
		for s = 1 to 5							
			this.notes[i].fretting[s] = -1
		next s
	next i
	Bar_typeID = Bar_typeID + 100 				// Allocate a group of 100 IDs for the bar
endfunction

function Bar_Draw(this ref as Bar)
	if DEBUG <> 0 								// Allows us to check boundary
		id = CreateSprite(Bar_rectID)
		SetSpritePosition(id,this.x,this.y)
		SetSpriteSize(id,this.width,this.height)
		SetSpriteColor(id,64,64,64,64)
	endif
	thickness = 1+this.height/200				// Draw the bar and staves
	for i = 1 to 5								// Vertical lines
		y = Bar_YPosition(this,i)
		id = Bar_CreateRectID(this)
		SetSpritePosition(id,this.x,y)
		SetSpriteSize(id,this.width,thickness)
	next i
	y1 = Bar_YPosition(this,1)					// Bar ends
	y2 = Bar_YPosition(this,5)
	for i = 0 to 1
		id = Bar_CreateRectID(this)
		SetSpritePosition(id,this.x+(this.width-thickness)*i,y1)
		SetSpriteSize(id,thickness,y2-y1+thickness)
	next i
	for note = 0 to this.notes.length 			// Draw the notes
		if this.notes[note].finger <> " "		// If note exist
			Bar_DrawNote(this,note)				// Draw it
			if mod(note,2) = 0 					// If first half of pair and second half exists
				if this.notes[note+1].finger <> " "
					hbar = Bar_CreateRectID(this) // Draw a connecting bar
					width = this.height / 30+1
					SetSpritePosition(hbar,Bar_XPosition(this,note),Bar_YPosition(this,6)-width)			
					SetSpriteSize(hbar,Bar_XPosition(this,note+1)-Bar_XPosition(this,note),width)
				endif
			endif
		endif
	next note
endfunction

function Bar_DrawNote(this ref as Bar,note as integer)
	lowest = 1										// Figure out the lowest one that is being played.
	for s = 1 to 5
		if this.notes[note].fretting[s] >= 0 then lowest = s
	next s
	x = Bar_XPosition(this,note)					// Horizontal position
	y1 = Bar_YPosition(this,lowest+0.5)
	vline = Bar_CreateRectID(this)					// Create vertical line
	w = 1+this.width/150
	SetSpritePosition(vline,x-w/2,y1)
	SetSpriteSize(vline,w,Bar_YPosition(this,6)-y1)
	CreateText(vline,this.notes[note].finger)		// Put TMI on the bottom
	SetTextFontImage(vline,Bar_fontID)
	SetTextColor(vline,0,0,0,255)
	SetTextSize(vline,this.width/20)
	SetTextPosition(vline,x-GetTextTotalWidth(vline)/2,Bar_YPosition(this,6.1))
endfunction

function Bar_XPosition(this ref as Bar,note as integer)
endfunction this.x + (note+0.5) * this.width / (this.beats * 2.0)

function Bar_YPosition(this ref as Bar,pos as float)
endfunction this.y + this.height * (pos-0.5) / 6.5

function Bar_CreateRectID(this ref as Bar)
	id = this.nextFreeID
	inc this.nextFreeID
	CreateSprite(id,Bar_rectID)
	SetSpriteColor(id,0,0,0,255)
endfunction id






