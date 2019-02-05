// ***************************************************************************************************
// ***************************************************************************************************
//
//		Name:		rotator.agc
//		Purpose:	rotator class
//		Date:		5th February 2019
//		Author:		Paul Robson (paul@robsons.org.uk)
//
// ***************************************************************************************************
// ***************************************************************************************************

type Rotator
	rotateSprite as integer 									// Sprite that is rotating
	label as integer 											// Text
	autoReturn as integer 										// Autoreturn rotator.
endtype

// ***************************************************************************************************
//										Initialise rotator
// ***************************************************************************************************

function Rotator_Initialise(this ref as Rotator,x as integer,y as integer,size as integer,label as string,sprite as string)
	img = LoadImage("sprites.png")
	this.rotateSprite = CreateSprite(LoadSubImage(img,sprite))
	SetSpriteSize(this.rotateSprite,size,size)
	SetSpriteOffset(this.rotateSprite,size/2,size/2)
	SetSpritePositionByOffset(this.rotateSprite,x,y)
	this.label = CreateText(label)
	SetTextSize(this.label,size/4)
	SetTextPosition(this.label,x-GetTextTotalWidth(this.label)/2,y+size/2)
endfunction

// ***************************************************************************************************
//										Destroy rotator
// ***************************************************************************************************

function Rotator_Destroy(this ref as Rotator)
	DeleteSprite(this.rotateSprite)
	DeleteText(this.label)
endfunction

// ***************************************************************************************************
//										Update rotator
// ***************************************************************************************************

function Rotator_Update(this ref as Rotator)
	isPressed = 0
	if GetSpriteHitTest(this.rotateSprite,GetPointerX(),GetPointerY()) <> 0
		if GetPointerState() <> 0 
			angle = GetSpriteAngle(this.rotateSprite)+GetFrameTime()*100
			while angle >= 360:angle = angle - 360:endwhile
			SetSpriteAngle(this.rotateSprite,angle)
			isPressed = 1
		endif
	endif
endfunction isPressed

// ***************************************************************************************************
//									Get rotator position
// ***************************************************************************************************

function Rotator_Get(this ref as Rotator)
	val# = (mod(GetSpriteAngle(this.rotateSprite)+180,360))/360.0
endfunction val#
