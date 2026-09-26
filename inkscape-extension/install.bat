@echo off
echo Kromacut Launcher - Manager
echo ========================================

set SRC=%~dp0..\inkscape-extension
set TARGET=%APPDATA%\Inkscape\extensions

echo Inkscape extensions folder: %TARGET%
echo.

if not exist "%TARGET%" (
    mkdir "%TARGET%"
)

copy /Y "%SRC%\send_to_kromacut.inx" "%TARGET%\" >nul
copy /Y "%SRC%\send_to_kromacut.py" "%TARGET%\" >nul

if errorlevel 1 (
    echo.
    echo Something went wrong copying the extension files.
) else (
    echo.
    echo Inkscape extension installed to:
    echo   %TARGET%
)

echo.
echo ----------------------------------------
echo Kromacut install
echo ----------------------------------------
set /p INSTALL_KROMACUT="Download and install Kromacut too? [Y/n]: "
if /i "%INSTALL_KROMACUT%"=="n" goto SKIP_KROMACUT

echo Looking up the latest Kromacut release...
powershell -NoProfile -Command ^
  "$rel = Invoke-RestMethod -Uri 'https://api.github.com/repos/vycdev/Kromacut/releases/latest';" ^
  "$asset = $rel.assets | Where-Object { $_.name -like '*setup.exe' -and $_.name -notlike '*offline*' } | Select-Object -First 1;" ^
  "if (-not $asset) { Write-Host 'Could not find a Windows installer in the latest release.'; exit 1 };" ^
  "$out = Join-Path $env:TEMP $asset.name;" ^
  "Write-Host ('Downloading ' + $asset.name + ' ...');" ^
  "Invoke-WebRequest -Uri $asset.browser_download_url -OutFile $out;" ^
  "Write-Host ('Running installer: ' + $out);" ^
  "Start-Process -FilePath $out -Wait"

if errorlevel 1 (
    echo.
    echo Kromacut download/install failed. You can grab it manually from:
    echo   https://github.com/vycdev/Kromacut/releases/latest
) else (
    echo.
    echo Kromacut installed.
)

:SKIP_KROMACUT
echo.
echo Restart Inkscape - "Send to Kromacut" should show up under Extensions.
echo.
pause

