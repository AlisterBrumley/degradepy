pyinstaller -w --clean --distpath ./dist-win -n qdd --add-data "./ffmpeg/*;./ffmpeg/" --noconfirm qddinst.py
rm -rf ./build