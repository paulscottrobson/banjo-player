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
endfunction

// ***************************************************************************************************
//									Set up the display
// ***************************************************************************************************

function Program_CreateDisplay(musicFile as string)
	prg.background = CreateSprite(LoadSubImage(LoadImage("sprites.png"),"background"))
	SetSpritePosition(prg.background,0,0)
	SetSpriteSize(prg.background,SCWIDTH,SCHEIGHT)
	SetSpriteDepth(prg.background,9999)
	
	prg.info = CreateText("Written by Paul Robson (paul@robsons.org.uk) 2019 v"+VERSION)
	SetTextFont(prg.info,LoadFont("rocko.ttf"))
	SetTextSize(prg.info,SCWIDTH/60)
	SetTextPosition(prg.info,SCWIDTH/2-GetTextTotalWidth(prg.info)/2,SCHEIGHT-GetTextTotalHeight(prg.info))

	prg.beatsPerMinute# = 60.0
	prg.pos# = 0.0

	Music_Initialise(prg.tune)
	Music_AddFile(prg.tune,musicFile)
	Manager_Initialise(prg.tune)
	Manager_SwitchRenderer(1)
	Player_Initialise(prg.tune)
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
		prg.pos# = prg.pos# + barsPerSec# * elapsed#			// New position
		if prg.pos# >= prg.tune.barCount 						// Off right hand end ?
			prg.pos# = 0:lastpos# = 0							// Reset to start
		endif
		
		beats = prg.tune.bars[trunc(prg.pos#)].beats 			// How many beats in bar
		hb1 = trunc(lastpos# * beats * 2)						// Work out halfbeat position
		hb2 = trunc(prg.pos# * beats * 2)
		if hb1 <> hb2 or lastpos# = 0  							// Time for a note ?
			if mod(hb2,2) = 0 then Player_PlayMetronome()		// Play metronome
			Player_PlayNote(prg.tune.bars[trunc(prg.pos#)].notes[mod(hb2,beats*2)])
		endif
	    Manager_MoveRenderTo(prg.pos#)							// Update display position
	
	    print(debug)
	    print(prg.pos#)
	    Sync()
	endwhile
endfunction

Program_SetupDisplay()
Program_CreateDisplay("cripple.plux")
Program_MainLoop()
