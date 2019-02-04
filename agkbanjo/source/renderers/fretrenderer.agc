// ***************************************************************************************************
// ***************************************************************************************************
//
//		Name:		fretrenderer.agc
//		Purpose:	Renderer for scrolling fretboard display.
//		Date:		4th February 2019
//		Author:		Paul Robson (paul@robsons.org.uk)
//
// ***************************************************************************************************
// ***************************************************************************************************

type FretRendererGlobals
	spriteImage as integer										// Sprite image
	fretHeight as integer										// pos/height of whole fretboard
	fretY as integer
	stringAreaHeight as integer									// pos/height of inner area where strings are
	stringAreaY as integer
	barWidth as integer											// width of one bar
	ballX as integer											// ball horizontal position.
endtype

global frg as FretRendererGlobals

// ***************************************************************************************************
//							Scrolling Fret Renderer - Command Dispatcher
// ***************************************************************************************************

function FretRenderer_Command(cmd as integer,bar ref as Bar,diBar as BarDisplayInfo,params as BarParameters)
	retval = 0
	select cmd
		case CMD_INITIALISE:
			frg.spriteImage = LoadImage("sprites.png")
		endcase
		case CMD_CREATE:
			FretRenderer_Create()
		endcase
		case CMD_DESTROY:
			FretRenderer_Destroy()
		endcase
		case CMD_VISIBLE:
		endcase
		case CMD_SHOW:
		endcase
		case CMD_HIDE:
		endcase
	endselect
endfunction retval

// ***************************************************************************************************
//										Create Background Objects
// ***************************************************************************************************

function FretRenderer_Create()
	frg.fretHeight = DPHEIGHT * 4 / 10							// Calculate positions, sizes etc.
	frg.fretY = DPHEIGHT - frg.fretHeight
	frg.stringAreaHeight = frg.fretHeight * 9 / 10
	frg.stringAreaY = frg.fretY + frg.fretHeight/2 - frg.stringAreaHeight/2
	frg.barWidth = SCWIDTH / 4
	frg.ballX = SCWIDTH * 10 / 100
																// Border to fretboard
	CreateSprite(CMD_ID,LoadSubImage(frg.spriteImage,"rectangle"))
	SetSpritePosition(CMD_ID,0,frg.fretY)
	SetSpriteSize(CMD_ID,SCWIDTH,frg.fretHeight)
	SetSpriteDepth(CMD_ID,9998)
	SetSpriteColor(CMD_ID,255,215,0,255)
																// Fretboard
	CreateSprite(CMD_ID+1,LoadSubImage(frg.spriteImage,"rectangle"))
	SetSpritePosition(CMD_ID+1,0,frg.stringAreaY)
	SetSpriteSize(CMD_ID+1,SCWIDTH,frg.stringAreaHeight)
	SetSpriteDepth(CMD_ID+1,9997)
	SetSpriteColor(CMD_ID+1,160,82,45,255)
	for s = 1 to 5:												// Strings
		id = CMD_ID+10+s
		CreateSprite(id,LoadSubImage(frg.spriteImage,"string"))
		SetSpriteDepth(id,9996)
		SetSpriteSize(id,SCWIDTH,DPHEIGHT/100+1)
		SetSpriteOffset(id,0,GetSpriteHeight(id)/2)
		SetSpritePositionByOffset(id,0,FretRenderer_StringY(s))
	next s
																// Bouncy ball
	CreateSprite(CMD_ID+2,LoadSubImage(frg.spriteImage,"spred"))
	sz = frg.stringAreaHeight/5
	SetSpriteSize(CMD_ID+2,sz,sz)
	SetSpriteOffset(CMD_ID+2,sz/2,sz)
	SetSpritePositionByOffset(CMD_ID+2,frg.ballX,frg.fretY)
	SetSpriteDepth(id,1)
endfunction

// ***************************************************************************************************
//								  Get Vertical String Position
// ***************************************************************************************************

function FretRenderer_StringY(s)
	s = (s-3) * frg.stringAreaHeight/5.0+frg.stringAreaY+frg.stringAreaHeight/2
endfunction s

// ***************************************************************************************************
//									Delete background objects
// ***************************************************************************************************

function FretRenderer_Destroy()
	DeleteSprite(CMD_ID)
	DeleteSprite(CMD_ID+1)
	DeleteSprite(CMD_ID+2)
	for s = 1 to 5
		DeleteSprite(CMD_ID+10+s)
	next s
endfunction
