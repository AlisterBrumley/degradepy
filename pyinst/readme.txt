 ----- QUICK AND DIRTY DEGRADER -----
A simple tool for degrading digital audio.
This readme is for the release versions for Mac OS or Windows, or for creating your own exectuable
For more basic information, check the github @ AstaBrum/degradepy

CONTENTS
- Mac
- Windows
- Linux
- Rolling your own


 ----- INFO FOR MAC USERS -----
Simply unzip and move to your application folder. The .app bundle might not be signed correctly for your version of MacOS and the OS might complain if you simply double click on it the first time. Instead, right click on the .app and click open. Accept the warning, and it should open normally from now on.

The bundle is packaged with ffmpeg but if you want to update the version or if it's having issues, it lives in qdd.app/Contents/Resources/ffmpeg. I bundled my own build using the latest source at time of writing, but it should run with any build.

If the program runs into errors during ffmpeg related tasks, it prints very long error messages. Rather then shove them in a dialog box, they will get dumped in an error log in your user folder at `~/.QDD_FFMPEG_ERROR_LOG.txt`


 ----- INFO FOR WINDOWS USERS -----
Simply unzip and move to wherever you want it. There should be no issues with UAC, but perhaps some antivirus programs will false-flag it. This was packaged using pyinstaller, which is also often used by virus-makers, so you might need to whitelist it.

This application requires ffmpeg, and is packaged in the application folder. If you want to update it, or if it's having issues, you should be able to replace it with the newest version. I used my own build using the latest source at time of writing, but it should run with any build.

If the program runs into errors during ffmpeg related tasks, it prints very long error messages. Rather then shove them in a dialog box, they will get dumped in an error log in the application folder `FFMPEG_ERROR_LOG.txt`


 ----- INFO FOR LINUX USERS -----
I haven't released a linux version, as I can only produce an executable that isn't portable. It seems to have issues working on different distro's or with different versions of ffmpeg then the one present when it was built. This might be fixable, but as yet I haven't been able and can't provide a download

It does however work on the system it was built on, so you're welcome to create your own for use locally. The next section should cover that.

If you do bundle it, and the program runs into errors during ffmpeg related tasks, it prints very long error messages. Rather then shove them in a dialog box, they will get dumped in an error log in your user folder at `~/.QDD_FFMPEG_ERROR_LOG.txt`


 ----- IF YOU WANT TO MAKE YOUR OWN -----
To build your own executable, you will need all the dependencies, including ffmpeg, as well as pyinstaller. Move the `ffmpeg` and `ffprobe` to `/pyinst/ffmpeg`. Then, simply run `pyinst-xxxx.sh` where xxxx is your OS platform.