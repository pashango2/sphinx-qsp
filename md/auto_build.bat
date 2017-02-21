@ECHO OFF

pushd %~dp0

REM Command file for Sphinx auto build

set SOURCEDIR=.
set BUILDDIR=_build

sphinx-autobuild -b html -r "___jb_.*?___$$" -r "^~.*" -r ".*?\.(bak|BAK)$$" %SOURCEDIR% %BUILDDIR%/html
goto end

:end
popd