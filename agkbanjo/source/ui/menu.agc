// ***************************************************************************************************
// ***************************************************************************************************
//
//		Name:		menu.agc
//		Purpose:	menu class
//		Date:		7th February 2019
//		Author:		Paul Robson (paul@robsons.org.uk)
//
// ***************************************************************************************************
// ***************************************************************************************************

type _MenuEntry 
	label as String
	value as String
	background as Integer
	text as Integer
endtype

type Menu
	count as Integer
	entries as _MenuEntry[1]
endtype

// ***************************************************************************************************
//										Initialise a menu
// ***************************************************************************************************

function Menu_Initialise(this ref as Menu)
	this.count = 0
	this.entries.length = 5
endfunction

// ***************************************************************************************************
//									Add a label/value pair
// ***************************************************************************************************

function Menu_Add(this ref as Menu,label as String,value as String)
	if this.count = this.entries.length then this.entries.length = this.entries.length + 5
	this.entries[this.count].label = label
	this.entries[this.count].value = value
	this.entries[this.count].background = -1
	this.entries[this.count].text = -1	
	inc this.count
endfunction

// ***************************************************************************************************
//								Load in a menu from an index file
// ***************************************************************************************************

function Menu_Load(this ref as Menu,indexfile as String)
	elements$ = File_Read(indexFile)
	for i = 1 to CountStringTokens(elements$,"~")-1 step 2
		Menu_Add(this,GetStringToken(elements$,"~",i+1),GetStringToken(elements$,"~",i))
	next i
endfunction

// ***************************************************************************************************
//										Select a menu option
// ***************************************************************************************************

function Menu_Select(this ref as Menu)
	c = this.count + 2.0:if c < 7 then c = 7
	menuHeight = SCHEIGHT / c
	frame = LoadSubImage(LoadImage("sprites.png"),"menurectangle")
	for e = 0 to this.count - 1
		y = SCHEIGHT / 2 - menuHeight * (this.count-1) / 2 + e * menuHeight
		id = CreateSprite(frame):this.entries[e].background = id
		SetSpriteSize(id,SCWIDTH * 0.75,menuHeight * 0.9)
		SetSpriteOffset(id,GetSpriteWidth(id)/2,GetSpriteHeight(id)/2)
		SetSpritePositionByOffset(id,SCWIDTH/2,y)
		//SetSpriteColor(id,0,0,255,255)
		id = CreateText(chr(e+65)+". "+this.entries[e].label):this.entries[e].text = id
		SetTextFont(id,LoadFont("rocko.ttf"))
		SetTextSize(id,menuHeight * 0.4)
		SetTextColor(id,255,255,0,255)
		SetTextPosition(id,SCWIDTH/2-GetTextTotalWidth(id)/2,y-GetTextTotalHeight(id)/2)
	next e
	selected = -1
	while selected < 0
		if GetRawKeyState(27) then end
		for i = 0 to this.count-1
			if GetRawKeyReleased(i+65) then selected = i
			if GetPointerPressed() <> 0 and GetSpriteHitTest(this.entries[i].background,GetPointerX(),GetPointerY()) <> 0 then selected = i
		next i
		sync()
	endwhile
	for e = 0 to this.count-1
		DeleteSprite(this.entries[e].background)
		DeleteText(this.entries[e].text)
	next e
endfunction this.entries[selected].value
