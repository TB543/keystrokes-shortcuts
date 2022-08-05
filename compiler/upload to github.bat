@echo off
for /F %%a in ('echo prompt $E ^| cmd') do (
  set "ESC=%%a"
)
SETLOCAL EnableDelayedExpansion
set /p comment="enter a comment to add to this upload (do not add any characters other than letters and numbers or errors may occur): "
echo:
cd ..
echo:
git init
echo:
git add .
echo:
git status
echo:
git commit -m "%comment%"
echo:
echo !ESC![92mRepository Created/Updated!ESC![0m
echo:
git remote add origin https://github.com/TB543/keystrokes-shortcuts
echo:
git branch -M main
echo:
git push --force -u origin main
echo:
echo !ESC![92mDone!ESC![0m
echo:
pause