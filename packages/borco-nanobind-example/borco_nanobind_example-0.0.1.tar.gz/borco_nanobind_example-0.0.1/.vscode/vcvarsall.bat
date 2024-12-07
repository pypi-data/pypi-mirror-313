@set PATH=%USERPROFILE%\scoop\apps\python\current\Scripts;%USERPROFILE%\scoop\apps\python\current;%USERPROFILE%\scoop\shims;%PATH%
@call "C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvarsall.bat" %*
"C:\Program Files\Git\bin\sh.exe" --login -i
