SetErrorMode(2)
#constant SCWIDTH 1440
#constant SCHEIGHT 960
#constant DPHEIGHT 840

#include "source/bar.agc"
#include "source/bardisplay.agc"
#include "source/music.agc"
#include "source/manager.agc"
#include "source/renderers/fretrenderer.agc"

global debug as string = "DBG:"

SetWindowTitle( "agkbanjo" )
SetWindowSize( SCWIDTH, SCHEIGHT, 0 )
SetWindowAllowResize( 1 ) // allow the user to resize the window
SetVirtualResolution( SCWIDTH, SCHEIGHT ) // doesn't have to match the window
SetOrientationAllowed( 1, 1, 1, 1 ) // allow both portrait and landscape on mobile devices
SetSyncRate( 30, 0 ) // 30fps instead of 60 to save battery
//SetScissor( 0,0,0,0 ) // use the maximum available screen space, no black borders
UseNewDefaultFonts( 1 ) // since version 2.0.22 we can use nicer default fonts

background = CreateSprite(LoadSubImage(LoadImage("sprites.png"),"background"))
SetSpritePosition(background,0,0)
SetSpriteSize(background,SCWIDTH,SCHEIGHT)
SetSpriteDepth(background,9999)

tune as Music
Music_Initialise(tune)
for i = 1 to 15
	Music_AddBar(tune)
next i

Manager_Initialise(tune)
Manager_SwitchRenderer(1)
//Manager_SwitchRenderer(0)

pos# = 0
while not GetRawKeyState(27)
	pos# = pos# + 0.006
    print(debug)
    print(pos#)
    Manager_MoveRenderTo(pos#)
    Sync()
endwhile
