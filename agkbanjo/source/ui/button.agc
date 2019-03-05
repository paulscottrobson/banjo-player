// ***************************************************************************************************
// ***************************************************************************************************
//
//		Name:		button.agc
//		Purpose:	Button class
//		Date:		5th February 2019
//		Author:		Paul Robson (paul@robsons.org.uk)
//
// ***************************************************************************************************
// ***************************************************************************************************

type Button
	lightSprite as integer 										// Inner sprite
	frameSprite as integer 										// Outer sprite
	state as integer 											// True if on.
	label as integer 											// Text
	autoReturn as integer 										// Autoreturn button.
	returnTime as integer 										// Time of return.
	rawKey as integer 											// Raw key control
endtype

// ***************************************************************************************************
//											Create button
// ***************************************************************************************************

function Button_Initialise(this ref as Button,x as integer,y as integer,size as integer,
										colour as string,label as string,autoReturn as integer,rawkey as integer)
	this.autoReturn = autoReturn
	img = LoadImage("sprites.png")
	this.frameSprite = CreateSprite(LoadSubImage(img,"rotary"))
	SetSpriteSize(this.frameSprite,size,size)
	SetSpriteOffset(this.frameSprite,size/2,size/2)
	SetSpritePositionByOffset(this.frameSprite,x,y)
	this.lightSprite = CreateSprite(LoadSubImage(img,colour))
	s2 = size * 8 / 10
	SetSpriteSize(this.lightSprite,s2,s2)
	SetSpriteOffset(this.lightSprite,s2/2,s2/2)
	SetSpritePositionByOffset(this.lightSprite,x,y)
	Button_SetState(this,0)
	this.label = CreateText(label)
	SetTextSize(this.label,size/4)
	SetTextPosition(this.label,x-GetTextTotalWidth(this.label)/2,y+size/2)
	this.rawKey = rawkey
endfunction

// ***************************************************************************************************
//											Set button state
// ***************************************************************************************************

function Button_SetState(this ref as Button,isOn as integer)
	this.state = isOn
	if this.autoReturn <> 0 then isOn = isOn = 0
	if isOn = 0
		SetSpriteColor(this.lightSprite,64,64,64,255)
	else
		SetSpriteColor(this.lightSprite,255,255,255,255)
	endif
endfunction

// ***************************************************************************************************
//											Destroy button
// ***************************************************************************************************

function Button_Destroy(this ref as Button)
	DeleteSprite(this.frameSprite)
	DeleteSprite(this.lightSprite)
	DeleteText(this.label)
endfunction

// ***************************************************************************************************
//											Update button
// ***************************************************************************************************

function Button_Update(this ref as Button)
	hasPressed = 0
	if this.autoReturn <>0 and GetMilliseconds() > this.returnTime and this.state <> 0
		Button_SetState(this,0)
	endif
	if (GetPointerReleased() <> 0 and GetSpriteHitTest(this.frameSprite,GetPointerX(),GetPointerY()) <> 0) or GetRawKeyPressed(this.rawKey) <> 0 
		Button_SetState(this,1-this.state)
		this.returnTime = GetMilliseconds() + 250
		hasPressed = 1
	endif
endfunction hasPressed

// ***************************************************************************************************
//										Get button current state
// ***************************************************************************************************

function Button_GetState(this ref as Button)
endfunction this.state
