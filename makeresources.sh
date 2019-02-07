#
#		Builds resources where required and copies them into applications media directory.
#
cp fonts/*.ttf agkbanjo/media
cp notes/sounds/*.ogg agkbanjo/media
cd graphics
python makeatlas.py
cd ..
cp graphics/sprites* agkbanjo/media
echo "Built resources"
