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
	sineHeight as integer 										// Height of sine curve
endtype

global frg as FretRendererGlobals
global frg_colours as integer[8] = [0xFFFF00,0x00FF00,0x00FFFF,0xFF00FF,0xC0C0C0,0x808000,0xFF8000,0x008080]
global frg_stringScale as float[4] = [0.7,0.8,0.9,1.0,0.5]


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
			FretRenderer_MoveBarGraphics(bar,diBar,x,params.pos)
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
	frg.barWidth = SCWIDTH / 3.0
	frg.ballX = SCWIDTH * 14 / 100
	frg.sineHeight = DPHEIGHT * 1.5 / 10
																// Border to fretboard
	CreateSprite(CMD_ID,LoadSubImage(frg.spriteImage,"rectangle"))
	SetSpritePosition(CMD_ID,0,frg.fretY)
	SetSpriteSize(CMD_ID,SCWIDTH,frg.fretHeight)
	SetSpriteDepth(CMD_ID,9998)
	SetSpriteColor(CMD_ID,102,51,0,255)
																// Fretboard
	CreateSprite(CMD_ID+1,LoadSubImage(frg.spriteImage,"rectangle"))
	SetSpritePosition(CMD_ID+1,0,frg.stringAreaY)
	SetSpriteSize(CMD_ID+1,SCWIDTH,frg.stringAreaHeight)
	SetSpriteDepth(CMD_ID+1,9997)
	SetSpriteColor(CMD_ID+1,160,82,45,255)
	for s = 1 to 5:												// Strings
		id = CMD_ID+10+s
		CreateSprite(id,LoadSubImage(frg.spriteImage,"string"))
		SetSpriteSize(id,SCWIDTH,DPHEIGHT/150*frg_stringScale[s-1]+1)
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
	
	CreateSprite(CMD_ID+3,LoadSubImage(frg.spriteImage,"bar"))
	SetSpriteSize(CMD_ID+3,sz/8,frg.stringAreaHeight)
	SetSpritePosition(CMD_ID+3,frg.ballX,frg.stringAreaY)
	SetSpriteDepth(CMD_ID+3,1)
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
	DeleteSprite(CMD_ID+3)
	for s = 1 to 5
		DeleteSprite(CMD_ID+10+s)
	next s
endfunction

// ***************************************************************************************************
//								Create all the bar graphics
// ***************************************************************************************************

function FretRenderer_CreateBarGraphics(bar ref as Bar,diBar ref as BarDisplayInfo)
	diBar.x = -99999 											// Forces a redraw on movebargraphics
	//debug = debug + " C:"+str(bar.barNumber)
	for i = 0 to 1
		id = diBar.baseID+198+i
		CreateSprite(id,LoadSubImage(frg.spriteImage,"rectangle"))
		SetSpriteSize(id,frg.barWidth/150+1,frg.stringAreaHeight)
		SetSpriteOffset(id,GetSpriteWidth(id)/2.0,0)
		SetSpriteColor(id,0,0,0,255)
		SetSpriteDepth(id,9995)
	next i
	for b = 0 to bar.beats*2-1
		if mod(b,2) = 0
			id = diBar.baseID + b * 20
			CreateSprite(id,LoadSubImage(frg.spriteImage,"sinecurve"))
			SetSpriteSize(id,frg.barWidth/bar.beats,frg.sineHeight)
			SetSpriteOffset(id,GetSpriteWidth(id)/4,GetSpriteHeight(id))
		endif
		for s = 1 to 5
			id = diBar.baseID + b * 20 + s
			fretting = bar.notes[b].fretting[s]
			if fretting <> BAR_DONTPLAY
				CreateText(id,str(fretting))
				SetTextFont(id,frg.font)
				SetTextSize(id,frg.stringAreaHeight/5.0*0.75)
				SetTextColor(id,0,0,0,255)
				CreateSprite(id,LoadSubImage(frg.spriteImage,"notebutton"))
				SetSpriteSize(id,frg.barWidth/2/bar.beats,frg.stringAreaHeight/5.0)
				SetSpriteOffset(id,GetSpriteHeight(id)*0.5,GetSpriteWidth(id)*0.45)
				SetSpriteDepth(id,99)
				col = frg_colours[mod(fretting,frg_colours.length)]
				SetSpriteColor(id,col/65536,mod(col/256,256),mod(col,256),255)
			endif
		next
	next b
endfunction

// ***************************************************************************************************
//								 Delete all the bar graphics
// ***************************************************************************************************

function FretRenderer_DestroyBarGraphics(bar ref as Bar,diBar ref as BarDisplayInfo)
	//debug = debug + " D:"+str(bar.barNumber)
	DeleteSprite(diBar.baseID+198)
	DeleteSprite(diBar.baseID+199)
	for b = 0 to bar.beats*2-1
		if mod(b,2) = 0 then DeleteSprite(diBar.baseID + b * 20)
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

function FretRenderer_MoveBarGraphics(bar ref as Bar,diBar ref as BarDisplayInfo,x as integer,pos as Float)
	if diBar.x = x then exitfunction 
	diBar.x = x
	//debug = debug + " M:"+str(bar.barNumber)+">"+str(x)
	SetSpritePositionByOffset(diBar.baseID+198,x+frg.barWidth,frg.stringAreaY)
	SetSpritePositionByOffset(diBar.baseID+199,x,frg.stringAreaY)
	for b = 0 to bar.beats*2-1
		x1 = round((b+0.5)/8.0*frg.barWidth+x+0.5)
		alpha = 255
		if x1 < frg.ballX then alpha = 255 - (frg.ballX-x1)*3/2
		if alpha < 0 then alpha = 0
		if mod(b,2) = 0 then SetSpritePositionByOffset(diBar.baseID+b*20,x1,frg.fretY)
		for s = 1 to 5
			id = diBar.baseID + b * 20 + s
			fretting = bar.notes[b].fretting[s]
			if fretting <> BAR_DONTPLAY
				SetTextPosition(id,x1-GetTextTotalWidth(id)/2.0,FretRenderer_StringY(s)-GetTextTotalHeight(id)/2)
				SetSpritePositionByOffset(id,x1,FretRenderer_StringY(s))
				SetTextColorAlpha(id,alpha)
				SetSpriteColorAlpha(id,alpha)
			endif
		next
	next b
	pos = mod((pos - Trunc(pos)) * 4 * 180,180)
	SetSpritePositionByOffset(CMD_ID+2,frg.ballX,frg.fretY-sin(pos)*frg.sineHeight)
endfunction
