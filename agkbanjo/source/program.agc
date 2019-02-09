// ***************************************************************************************************
// ***************************************************************************************************
//
//		Name:		program.agc
//		Purpose:	Main Program
//		Date:		5th February 2019
//		Author:		Paul Robson (paul@robsons.org.uk)
//
// ***************************************************************************************************
// ***************************************************************************************************

type ProgramGlobals
	tune as Music												// Tune being played
	background as Integer										// Background graphic
	info as Integer												// Copyright label
	pos# as Float												// Position in music
	beatsPerMinute# as Float									// Speed of playback BPM
	speedRotator as Rotator 									// Rotator for base speed
	speedupButton as Button 									// Toggle button for speed
	posCtrl as Slider 											// Slider for pos/repeat control
	bpmLabel as integer 										// BPM Display Sprite
	rendererID as integer 										// Current renderer
endtype

global prg as ProgramGlobals
global debug as string = "DBG:"

// ***************************************************************************************************
//									Initialise the display
// ***************************************************************************************************

function Program_SetupDisplay()
	SetWindowTitle( "Banjo Trainer" )
	SetWindowSize( SCWIDTH, SCHEIGHT, 0 )
	SetWindowAllowResize( 1 ) // allow the user to resize the window
	SetVirtualResolution( SCWIDTH, SCHEIGHT ) // doesn't have to match the window
	SetOrientationAllowed( 1, 1, 1, 1 ) // allow both portrait and landscape on mobile devices
	SetSyncRate( 60, 0 ) // 30fps instead of 60 to save battery
	//SetScissor( 0,0,0,0 ) // use the maximum available screen space, no black borders
	UseNewDefaultFonts( 1 ) // since version 2.0.22 we can use nicer default fonts

	prg.background = CreateSprite(LoadSubImage(LoadImage("sprites.png"),"background"))
	SetSpritePosition(prg.background,0,0)
	SetSpriteSize(prg.background,SCWIDTH,SCHEIGHT)
	SetSpriteDepth(prg.background,9999)
	
	prg.info = CreateText("Written by Paul Robson (paul@robsons.org.uk) 2019 v"+VERSION)
	SetTextFont(prg.info,LoadFont("rocko.ttf"))
	SetTextSize(prg.info,SCWIDTH/60)
	SetTextPosition(prg.info,SCWIDTH/2-GetTextTotalWidth(prg.info)/2,SCHEIGHT-GetTextTotalHeight(prg.info))
endfunction

// ***************************************************************************************************
//									Set up the display
// ***************************************************************************************************

function Program_CreateDisplay(musicFile as string)

	prg.pos# = 0.0
	prg.rendererID = 1
	Music_Initialise(prg.tune)
	Music_AddFile(prg.tune,musicFile)
	Manager_Initialise(prg.tune)
	Manager_SwitchRenderer(prg.rendererID)
	Player_Initialise(prg.tune)
		
	yc = (SCHEIGHT+DPHEIGHT)/2
	prg.bpmLabel = CreateText("000")
	sp = SCHEIGHT-DPHEIGHT
	sz = sp * 0.7
	SetTextSize(prg.bpmLabel,sp)
	SetTextFont(prg.bpmLabel,LoadFont("digital.ttf"))
	xc = SCWIDTH-GetTextTotalWidth(prg.bpmLabel)-10
	SetTextPosition(prg.bpmLabel,xc,yc-GetTextTotalHeight(prg.bpmLabel)/2)
	SetTextColor(prg.bpmLabel,255,51,51,255)
	SetTextPosition(prg.bpmLabel,xc,yc-GetTextTotalHeight(prg.bpmLabel)/2)
	Program_SetSpeed(80.0)
	Rotator_Initialise(prg.speedRotator,xc-sp/2,yc,sz,"Speed BPM","rotary")
	Button_Initialise(prg.speedupButton,xc-sp*3/2,yc,sz,"spgreen","Speed up",0)
	Slider_Initialise(prg.posCtrl,10,xc-sp*2,yc,sz*0.8)
endfunction

// ***************************************************************************************************
//											Update speed
// ***************************************************************************************************

function Program_SetSpeed(newSpeed as Float)
	prg.beatsPerMinute# = newSpeed
	SetTextString(prg.bpmLabel,right("000"+str(trunc(newSpeed)),3))
endfunction

// ***************************************************************************************************
//										Main loop code
// ***************************************************************************************************

function Program_MainLoop()
	lastTime = GetMilliseconds()
	while not GetRawKeyState(27)
		elapsed = GetMilliseconds() - lastTime					// Track time between frames.
		lastTime = GetMilliseconds()
																// Convert to a time in bars.
		elapsed# = elapsed / 1000.0 							// Actual elapsed time in seconds.
		beatsPerSec# = prg.beatsPerMinute# / 60.0 				// Beats per second
		beatsPerBar# = prg.tune.bars[trunc(prg.pos#)].beats 	// Beats per bar
		barsPerSec# = beatsPerSec# / beatsPerBar#				// Bars per second
		
		lastpos# = prg.pos#										// Last position
		prg.pos# = prg.pos# + barsPerSec# * elapsed#  * 2.0		// New position, allowing banjo BPM Scalar
		endPos# = prg.tune.barCount * Slider_Get(prg.posCtrl,SLIDER_END)
		if prg.pos# >= endPos# 									// Off right hand end ?
			prg.pos# = prg.tune.barCount * Slider_Get(prg.posCtrl,SLIDER_START)
			lastPos# = prg.pos#
			if Button_GetState(prg.speedupButton) <> 0 
				Program_SetSpeed(prg.beatsPerMinute# + 2)
			endif
		endif
		
		beats = prg.tune.bars[trunc(prg.pos#)].beats 			// How many beats in bar
		hb1 = trunc(lastpos# * beats * 2)						// Work out halfbeat position
		hb2 = trunc(prg.pos# * beats * 2)
		if hb1 <> hb2 or lastpos# = 0  							// Time for a note ?
			if mod(hb2,2) = 0 then Player_PlayMetronome()		// Play metronome
			Player_PlayNote(prg.tune.bars[trunc(prg.pos#)].notes[mod(hb2,beats*2)])
		endif
	    Manager_MoveRenderTo(prg.pos#)							// Update display position
		Slider_SetPosition(prg.posCtrl,prg.pos#/(0.0+prg.tune.barCount))
		if Slider_Update(prg.posCtrl) <> 0
			prg.pos# = prg.tune.barCount * Slider_Get(prg.posCtrl,SLIDER_POSITION)
		endif
		Button_Update(prg.speedupButton)						// Update UI objects
		if Rotator_Update(prg.speedRotator)	<> 0
			newSpeed = 80+(Rotator_Get(prg.speedRotator)-0.5)*2*60
			Program_SetSpeed(newSpeed)
		endif
		
		if GetPointerPressed() and GetPointerY() < DPHEIGHT		// Switch renderer
			//prg.rendererID = 1-prg.rendererID
			//Manager_SwitchRenderer(prg.rendererID)
		endif
		
	    print(debug)
	    print(prg.pos#)
	    print(Rotator_Get(prg.speedRotator))
	    Sync()
	endwhile
endfunction

// ***************************************************************************************************
//											Select from menu
// ***************************************************************************************************

function Program_SelectFromMenu(menuFile as string,canReturn as integer)
	menu as Menu
	Menu_Initialise(menu)										// Set up menu, add 'return' if not top
	if canReturn <> 0 then Menu_Add(menu,"Previous Menu","<back>")
	Menu_Load(menu,menuFile)									// Load in menu data
	selected as string = ""
	while selected = ""											// Until something is selected
		selected = Menu_Select(menu)							// Pick menu option
		if right(selected,5) <> ".plux" and selected <> "<back>"// If not tune and not back
			selected = Program_SelectFromMenu(selected,1)		// Do sub menu
		endif
	endwhile
	if selected = "<back>" then selected = ""					// Previous option, return "" to make caller loop
endfunction selected

Program_SetupDisplay()
file$ = "__test.plux"
file$ = "lessons/strum.plux"
//file$ = Program_SelectFromMenu("home.index",0)
Program_CreateDisplay(file$)
Program_MainLoop()
