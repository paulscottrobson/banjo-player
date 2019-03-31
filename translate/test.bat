@echo off
call buildall.bat
echo 0 >..\agkbanjo\media\showmenu.txt
..\agkbanjo\agkbanjo.exe
echo 1 >..\agkbanjo\media\showmenu.txt
