@set PATH=%USERPROFILE%\scoop\apps\python\current\Scripts;%USERPROFILE%\scoop\apps\python\current;%USERPROFILE%\scoop\shims;%PATH%
@call "C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvarsall.bat" %*

@set VENV_ACTIVATE=%WORKSPACE_FOLDER%\.venv\Scripts\activate.bat
if exist %VENV_ACTIVATE% (
    @echo Activating .venv ...
    @call %VENV_ACTIVATE%
) else (
    @echo %VENV_ACTIVATE not found.
)

"C:\Program Files\Git\bin\sh.exe" --login -i
