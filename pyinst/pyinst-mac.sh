#! /bin/sh

# adds ffmpeg into executable and names it qdd
pyinstaller -w --clean --distpath ./dist-Mac -n qdd --add-data "./ffmpeg/*:./ffmpeg/" --noconfirm qddinst.py

# deletes unneeded build file
rm -rf ./build
rm -rf ./dist-Mac/qdd/