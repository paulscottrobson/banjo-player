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
#constant VERSION "0.13 (04-Mar-19)"

#include "source/bar.agc"
#include "source/bardisplay.agc"
#include "source/ui/button.agc"
#include "source/ui/rotator.agc"
#include "source/ui/slider.agc"
#include "source/ui/menu.agc"
#include "source/music.agc"
#include "source/player.agc"
#include "source/manager.agc"
#include "source/readfile.agc"
#include "source/renderers/fretrenderer.agc"
#include "source/program.agc"

// TODO: 	
//		TAB Display / scrolling tab ?
// 		Clawhammer Arrows option ?
