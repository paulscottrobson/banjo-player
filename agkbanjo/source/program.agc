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
	backButton as Button 										// Back button
	pauseButton as Button 										// Toggle button for pause
	posCtrl as Slider 											// Slider for pos/repeat control
	bpmLabel as integer 										// BPM Display Sprite
	rendererID as integer 										// Current renderer
endtype

global prg as ProgramGlobals
global debug as string = ""

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

	prg.info = CreateText("Written by Paul Robson (paul@robsons.org.uk) v"+VERSION)
	SetTextFont(prg.info,LoadFont("rocko.ttf"))
	SetTextSize(prg.info,SCWIDTH/70)
	SetTextPosition(prg.info,SCWIDTH/2-GetTextTotalWidth(prg.info)/2,SCHEIGHT-GetTextTotalHeight(prg.info))
endfunction

// ***************************************************************************************************
//									Set up the display
// ***************************************************************************************************

function Program_CreateDisplay()

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
	Rotator_Initialise(prg.speedRotator,xc-sp/2,yc,sz,"Tempo BPM","rotary",asc("T"))
	Button_Initialise(prg.speedupButton,xc-sp*3/2,yc,sz,"sporange","Speed up",0,asc("S"))
	Button_Initialise(prg.pauseButton,10+sp*3/2,yc,sz,"spred","Pause",0,asc("P"))
	Button_Initialise(prg.backButton,10+sp/2,yc,sz,"back","Select",1,asc("Q"))
	Slider_Initialise(prg.posCtrl,sp+10+sp,xc-sp*2,yc,sz*0.8)
endfunction

// ***************************************************************************************************
//								Initialise new tunr
// ***************************************************************************************************

function Program_OpenTune(musicFile as string)
	prg.pos# = 0.0
	prg.rendererID = 1
	Music_Initialise(prg.tune)
	Music_AddFile(prg.tune,musicFile)
	Manager_Initialise(prg.tune)
	Manager_SwitchRenderer(prg.rendererID)
	Player_Initialise(prg.tune)
	Program_SetSpeed(prg.tune.defaultBPM)
	Rotator_ResetRotation(prg.speedRotator)
endfunction

// ***************************************************************************************************
//									  Tidy up
// ***************************************************************************************************

function Program_CloseTune()
	Manager_SwitchRenderer(-2)
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
	exitPlay = 0
	while exitPlay = 0
		if GetRawKeyPressed(27) <> 0 then end					// Crashes out
		if debug <> "" then print("[DEBUG]"+debug)				// Output any debugging info
		elapsed = GetMilliseconds() - lastTime					// Track time between frames.
		lastTime = GetMilliseconds()

		if Button_GetState(prg.pauseButton) = 0
																// Convert to a time in bars
			elapsed# = elapsed / 1000.0 						// Actual elapsed time in seconds.
			beatsPerSec# = prg.beatsPerMinute# / 60.0 			// Beats per second
			beatsPerBar# = prg.tune.bars[trunc(prg.pos#)].beatsInBar // Beats per bar
			barsPerSec# = beatsPerSec# / beatsPerBar#			// Bars per second

			lastpos# = prg.pos#									// Last position
			prg.pos# = prg.pos# + barsPerSec# * elapsed# 		// New position
			if GetRawKeyPressed(32) <> 0 then prg.pos# = 0		// Space resets
			if GetRawKeyPressed(asc("Q")) <> 0 then exitPlay=1	// Q back to selector

			endPos# = prg.tune.barCount * Slider_Get(prg.posCtrl,SLIDER_END)
			if prg.pos# >= endPos# 								// Off right hand end ?
				prg.pos# = prg.tune.barCount * Slider_Get(prg.posCtrl,SLIDER_START)
				lastPos# = prg.pos#
				if Button_GetState(prg.speedupButton) <> 0
					Program_SetSpeed(prg.beatsPerMinute# + prg.tune.stepBPM)
				endif
			endif

			notes = prg.tune.bars[trunc(prg.pos#)].notesInBar 	// How many beats in bar
			qb1 = trunc(lastpos# * notes)						// Work out quarterbeat position
			qb2 = trunc(prg.pos# * notes)
			if qb1 <> qb2 or lastpos# = 0  						// Time for a note ?
				if mod(qb2,2) = 0 then Player_PlayMetronome()	// Play metronome
				Player_PlayNote(prg.tune.bars[trunc(prg.pos#)].notes[mod(qb2,notes)])
			endif
		endif
	    Manager_MoveRenderTo(prg.pos#)							// Update display position
		Slider_SetPosition(prg.posCtrl,prg.pos#/(0.0+prg.tune.barCount))
		if Slider_Update(prg.posCtrl) <> 0
			prg.pos# = prg.tune.barCount * Slider_Get(prg.posCtrl,SLIDER_POSITION)
		endif
		Button_Update(prg.speedupButton)						// Update UI objects
		Button_Update(prg.pauseButton)
		Button_Update(prg.backButton)
		if Button_GetState(prg.backButton) <> 0 then exitPlay = 1
		if Rotator_Update(prg.speedRotator)	<> 0
			newSpeed = prg.tune.defaultBPM+(Rotator_Get(prg.speedRotator)-0.5)*2*(prg.tune.defaultBPM*0.95)
			Program_SetSpeed(newSpeed)
		endif

		if GetPointerPressed() and GetPointerY() < DPHEIGHT		// Switch renderer
			//prg.rendererID = 1-prg.rendererID
			//Manager_SwitchRenderer(prg.rendererID)
		endif
		Sync()
	endwhile
	Sync()
endfunction

// ***************************************************************************************************
//											Select from menu
// ***************************************************************************************************

function Program_SelectFromMenu(menuDirectory as string,canReturn as integer)
	menu as Menu
	Menu_Initialise(menu)										// Set up menu, add 'return' if not top
	if canReturn <> 0 then Menu_Add(menu,"Previous Menu","<back>")
	Menu_Load(menu,menuDirectory+"index.txt")					// Load in menu data
	selected as string = ""
	while selected = ""											// Until something is selected
		selected = Menu_Select(menu)							// Pick menu option
		if right(selected,5) <> ".plux" and selected <> "<back>"// If not tune and not back
			subdir$ = menuDirectory+selected+"/"
			selected = Program_SelectFromMenu(subdir$,1)		// Do sub menu
		endif
		if right(selected,5) = ".plux"
			if FindString(selected,"/") = 0
				selected = menuDirectory+selected
			endif
		endif
	endwhile
	if selected = "<back>" then selected = ""					// Previous option, return "" to make caller loop
endfunction selected

Program_SetupDisplay()
Program_CreateDisplay()
OpenToRead(1,"showmenu.txt")
readTest$ = ReadLine(1)
CloseFile(1)
repeat
	file$ = "__test.plux"
//if left(readTest$,1) = "1" then file$ = Program_SelectFromMenu("",0)
	Program_OpenTune(file$)
	Program_MainLoop()
	Program_CloseTune()
until 0
	
