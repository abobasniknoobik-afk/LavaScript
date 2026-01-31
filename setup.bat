@echo off
assoc .ls=LavaScriptFile
ftype LavaScriptFile=python.exe "%1" %*
echo LavaScript (.ls) registered for Windows.
pause
