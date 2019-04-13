#		Builds resources where required and copies them into applications media directory.
#
#
cp resources/fonts/*.ttf agkbanjo/media
cp resources/notes/sounds/*.ogg agkbanjo/media/sounds
cd resources/graphics
python makeatlas.py
cd ../..
cp resources/graphics/sprites* agkbanjo/media
echo "Built resources"
