// ***************************************************************************************************
// ***************************************************************************************************
//
//		Name:		main.agc
//		Purpose:	Main Program
//		Date:		5th February 2019
//		Author:		Paul Robson (paul@robsons.org.uk)
//
// ***************************************************************************************************
// ***************************************************************************************************

SetErrorMode(2)

#constant SCWIDTH 1440
#constant SCHEIGHT 960
#constant DPHEIGHT 840
#constant VERSION "0.1"

#include "source/bar.agc"
#include "source/bardisplay.agc"
#include "source/music.agc"
#include "source/player.agc"
#include "source/manager.agc"
#include "source/readfile.agc"
#include "source/renderers/fretrenderer.agc"
#include "source/program.agc"

// TODO: 	
//		Beats per minute display
//		Lit Button UI class (step up on/off off end)
//		RotatorButton UI class (current speed/writeable)
//		Scrollbar UI class
//			Make it follow and update
//			On loop back speed up (lit button)
