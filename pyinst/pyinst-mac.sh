pyinstaller -w --clean --distpath ./dist-mac -n qdd --add-data "./ffmpeg/*:./ffmpeg/" --noconfirm qddinst.py
rm -rf ./build
rm -rf ./dist-mac/qdd/