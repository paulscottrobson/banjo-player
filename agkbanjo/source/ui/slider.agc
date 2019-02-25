// ***************************************************************************************************
// ***************************************************************************************************
//
//		Name:		slider.agc
//		Purpose:	slider class
//		Date:		6th February 2019
//		Author:		Paul Robson (paul@robsons.org.uk)
//
// ***************************************************************************************************
// ***************************************************************************************************

#constant SLIDER_START		0
#constant SLIDER_END 		1
#constant SLIDER_POSITION	2

type Slider
	pos as float[3]
	bar as integer
	spheres as integer[3]
	currentDrag as integer
	x as integer
	y as integer
	width as integer
endtype

function Slider_Initialise(this ref as slider,x1 as integer,x2 as integer,y as integer,size as integer)
	this.pos[SLIDER_START] = 0.0
	this.pos[SLIDER_POSITION] = 0.0
	this.pos[SLIDER_END] = 1.0
	this.currentDrag = -1
	this.x = x1+size/2
	this.y = y
	this.width = x2-x1-size
	img = LoadImage("sprites.png")
	this.bar = CreateSprite(LoadSubImage(img,"rectangle"))
	SetSpriteSize(this.bar,this.width,size/6)
	SetSpritePosition(this.bar,this.x,y-GetSpriteHeight(this.bar)/2)
	SetSpriteColor(this.bar,0,64,192,255)
	for i = 0 to 2
		col$ = "green":sz = size
		if i = SLIDER_END then col$ = "cyan"
		if i = SLIDER_POSITION 
			sz = sz * 0.8:col$ = "yellow"
		endif
		this.spheres[i] = CreateSprite(LoadSubImage(img,"sp"+col$))
		SetSpriteSize(this.spheres[i],sz,sz)
		SetSpriteOffset(this.spheres[i],sz/2,sz/2)
		SetSpritePosition(this.spheres[i],i*100+100,200)
	next i
endfunction

function Slider_Destroy(this ref as slider)
	DeleteSprite(this.bar)
	for i = 0 to 2:DeleteSprite(this.spheres[i]):next i
endfunction

function Slider_Get(this ref as slider,item as integer)
endfunction this.pos[item]

function Slider_SetPosition(this ref as slider,pos as float)
	this.pos[SLIDER_POSITION] = pos
endfunction

function Slider_Update(this ref as slider)
	hasChanged = 0
	if GetPointerPressed() <> 0 and this.currentDrag < 0
		for i = 0 to 2
			if GetSpriteHitTest(this.spheres[i],GetPointerX(),GetPointerY()) <> 0 then this.currentDrag = i
		next i
	endif
	if GetPointerReleased() <> 0 and this.currentDrag >= 0
		this.currentDrag = -1
		if this.pos[SLIDER_START] > this.pos[SLIDER_END]-0.025 then this.pos[SLIDER_START] = this.pos[SLIDER_END]-0.025
	endif
	if this.currentDrag >= 0
		this.pos[this.currentDrag] = (GetPointerX()-this.x)/(this.width+0.0)
		if this.pos[this.currentDrag] < 0.0 then this.pos[this.currentDrag] = 0.0
		if this.pos[this.currentDrag] > 1.0 then this.pos[this.currentDrag] = 1.0
		hasChanged = (this.currentDrag = SLIDER_POSITION)
	endif	
	for i = 0 to 2
		SetSpritePositionByOffset(this.spheres[i],this.pos[i]*this.width+this.x,this.y)
	next i
endfunction hasChanged

