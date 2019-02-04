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
	font as integer 											// TTF font
	fretHeight as integer										// pos/height of whole fretboard
	fretY as integer
	stringAreaHeight as integer									// pos/height of inner area where strings are
	stringAreaY as integer
	barWidth as integer											// width of one bar
	ballX as integer											// ball horizontal position.
endtype

global frg as FretRendererGlobals
global colours as integer[8] = [0xFFFF00,0x00FF00,0x00FFFF,0xFF00FF,0xC0C0C0,0x808000,0xFF8000,0x008080]

// ***************************************************************************************************
//							Scrolling Fret Renderer - Command Dispatcher
// ***************************************************************************************************

function FretRenderer_Command(cmd as integer,bar ref as Bar,diBar ref as BarDisplayInfo,params ref as BarParameters)
	retval = 0
	x as integer 
	x = round((bar.barNumber-params.pos) * frg.barWidth + frg.ballX)
	select cmd
		case CMD_INITIALISE:
			frg.spriteImage = LoadImage("sprites.png")
			frg.font = LoadFont("rocko.ttf")
		endcase
		case CMD_CREATE:
			FretRenderer_Create()
		endcase
		case CMD_DESTROY:
			FretRenderer_Destroy()
		endcase
		case CMD_VISIBLE:
			retval = (x >= -frg.barWidth) and (x < SCWIDTH)
		endcase
		case CMD_SHOW:
			if diBar.isDrawn = 0 then FretRenderer_CreateBarGraphics(bar,diBar)
			diBar.isDrawn = 1
			FretRenderer_MoveBarGraphics(bar,diBar,x)
		endcase
		case CMD_HIDE:
			if diBar.isDrawn <> 0 then FretRenderer_DestroyBarGraphics(bar,diBar)
			diBar.isDrawn = 0
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
	frg.barWidth = SCWIDTH / 2.3
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
		SetSpriteSize(id,SCWIDTH,DPHEIGHT/150+1)
		SetSpriteOffset(id,0,GetSpriteHeight(id)/2)
		SetSpritePositionByOffset(id,0,FretRenderer_StringY(s))
		SetSpriteDepth(id,9996)
	next s
																// Bouncy ball
	CreateSprite(CMD_ID+2,LoadSubImage(frg.spriteImage,"spred"))
	sz = frg.stringAreaHeight/5
	SetSpriteSize(CMD_ID+2,sz,sz)
	SetSpriteOffset(CMD_ID+2,sz/2,sz)
	SetSpritePositionByOffset(CMD_ID+2,frg.ballX,frg.fretY)
	SetSpriteDepth(CMD_ID+2,1)
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

// ***************************************************************************************************
//								Create all the bar graphics
// ***************************************************************************************************

function FretRenderer_CreateBarGraphics(bar ref as Bar,diBar ref as BarDisplayInfo)
	diBar.x = -99999 											// Forces a redraw on movebargraphics
	debug = debug + " C:"+str(bar.barNumber)
	id = diBar.baseID+199
	CreateSprite(id,LoadSubImage(frg.spriteImage,"bar"))
	SetSpriteSize(id,frg.barWidth/40,frg.stringAreaHeight)
	SetSpriteOffset(id,GetSpriteWidth(id)/2.0,0)
	SetSpriteDepth(id,9995)
	for b = 0 to bar.beats*2-1
		for s = 1 to 5
			id = diBar.baseID + b * 20 + s
			fretting = bar.notes[b].fretting[s]
			if fretting <> BAR_DONTPLAY
				s1 = frg.barWidth/2/bar.beats:s2 = frg.stringAreaHeight/5:if s2<s1 then s1=s2
				CreateText(id,str(fretting))
				SetTextFont(id,frg.font)
				SetTextSize(id,s1*0.75)
				SetTextColor(id,0,0,0,255)
				CreateSprite(id,LoadSubImage(frg.spriteImage,"notebutton"))
				SetSpriteSize(id,s1,s1)
				SetSpriteOffset(id,s1*0.5,s1*0.45)
				SetSpriteDepth(id,99)
				col = colours[mod(fretting,colours.length)]
				SetSpriteColor(id,col/65536,mod(col/256,256),mod(col,256),255)
			endif
		next
	next b
endfunction

// ***************************************************************************************************
//								 Delete all the bar graphics
// ***************************************************************************************************

function FretRenderer_DestroyBarGraphics(bar ref as Bar,diBar ref as BarDisplayInfo)
	debug = debug + " D:"+str(bar.barNumber)
	DeleteSprite(diBar.baseID+199)
	for b = 0 to bar.beats*2-1
		for s = 1 to 5
			id = diBar.baseID + b * 20 + s
			fretting = bar.notes[b].fretting[s]
			if fretting <> BAR_DONTPLAY
				DeleteText(id)
				DeleteSprite(id)
			endif
		next
	next b	
endfunction

// ***************************************************************************************************
// 				Reposition and make position relevant adjustments to the graphics
// ***************************************************************************************************

function FretRenderer_MoveBarGraphics(bar ref as Bar,diBar ref as BarDisplayInfo,x as integer)
	if diBar.x = x then return 
	diBar.x = x
	//debug = debug + " M:"+str(bar.barNumber)+">"+str(x)
	SetSpritePositionByOffset(diBar.baseID+199,x,frg.stringAreaY)
	for b = 0 to bar.beats*2-1
		x1 = round((b+0.5)/8.0*frg.barWidth+x+0.5)
		for s = 1 to 5
			id = diBar.baseID + b * 20 + s
			fretting = bar.notes[b].fretting[s]
			if fretting <> BAR_DONTPLAY
				SetTextPosition(id,x1-GetTextTotalWidth(id)/2.0,FretRenderer_StringY(s)-GetTextTotalHeight(id)/2)
				SetSpritePositionByOffset(id,x1,FretRenderer_StringY(s))
			endif
		next
	next b
endfunction
