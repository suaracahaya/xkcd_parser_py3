xkcd_parser_py3
===============

xkcd comic parser for Python 3.x

This is a modified version from Ana Balica's script (https://gist.github.com/ana-balica/5454270) to work in Python 3.
The script will download random comic from xkcd.com and display the title and caption on your screen.

2014/06/11 16:20
- First time on GitHub!
- Modified the regex script (Line 82) which can't work on Python 3 due to string and byte-array type difference.
- The script can run well, but the downloaded image doesn't have a file type (I have to manually adding .jpg extension to the file).
- The comic info (comic no., title, caption) is only displayed on screen.

Next plan:
- Add script to name the image with .jpg
- Add script to save (append) comic info into a txt file
