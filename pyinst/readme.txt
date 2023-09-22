 ----- QUICK AND DIRTY DEGRADER -----
A simple tool for degrading digital audio.
Compatible with Windows 10 or newer, Mac OS 10.13 or newer, and Linux with kernel 4.19 or newer

This readme is for the release versions for Mac OS, Windows and Linux, but includes instructions creating your own exectuable.
For more basic information, check the github @ AstaBrum/degradepy


CONTENTS
- Mac
- Windows
- Linux
- Rolling your own


 ----- INFO FOR MAC USERS -----
Simply unzip and move to your application folder. The .app bundle might not be signed correctly for your version of MacOS, and it might complain if you simply double click on it the first time launching it. Instead, right click on the .app and click open. Accept the warning, and it should open normally from now on.

The bundle is packaged with ffmpeg but if you want to update the version or if it's having issues, it's located at qdd.app/Contents/Resources/ffmpeg/, and you should be able to replace it with the newest version provided on the ffmpeg website. It's packaged with a minimal build of ffmpeg 6.0, but it should run with any build that has the correct codecs/muxers. If the program runs into errors during ffmpeg related tasks, it prints very long error messages. Rather then shove them in a dialog box, they will get dumped in an error log in your user folder at `~/.qdd/FFMPEG_ERROR_LOG.txt`


 ----- INFO FOR WINDOWS USERS -----
Simply unzip and move to wherever you want it. Some antivirus programs might false-flag it, and the built in windows defender might possibly delete it, or it's files. This was packaged using pyinstaller, which is also often used by virus-makers, so you might need to whitelist it.

This application requires ffmpeg, and it is packaged in the application folder. If you want to update it, or if it's having issues, you should be able to replace it with the newest version provided on the ffmpeg website. It's packaged with a minimal build of ffmpeg 6.0, but it should run with any build that has the correct codecs/muxers. If the program runs into errors during ffmpeg related tasks, it prints very long error messages. Rather then shove them in a dialog box, they will get dumped in an error log in the application folder `FFMPEG_ERROR_LOG.txt`

 ----- INFO FOR LINUX USERS -----
Simply unzip and move to wherever you want it. The bundle is packaged with a minimal build of ffmpeg 6.0. It can only recgonise it's built in ffmpeg version, and to my knowledge, it can't be updated/replaced. If the program runs into errors during ffmpeg related tasks, it prints very long error messages. Rather then shove them in a dialog box, they will get dumped in an error log in your user folder at `~/.qdd/FFMPEG_ERROR_LOG.txt`.

 ----- IF YOU WANT TO MAKE YOUR OWN -----
To build your own executable, you will need all the dependencies, including ffmpeg, as well as pyinstaller. Download the source, and move `deghelpers.py` and 'guihelpers.py` to `/pyinst` Move the `ffmpeg` and `ffprobe` to `/pyinst/ffmpeg". Then, simply run `pyinst-xxxx.sh` where xxxx is your OS platform.
