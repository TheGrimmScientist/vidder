# Vidder

Provide interface on top of already-written [ffmpeg](https://ffmpeg.org/ffmpeg.html) libraries to automate my common 
processing steps for training videos.

# Selection of ffmpeg library.
Two candidates exist, from what I've seen.
* [python-ffmpeg](https://github.com/jonghwanhyeon/python-ffmpeg)
  * example: https://github.com/jonghwanhyeon/python-ffmpeg/blob/main/examples/transcoding.py
* [ffmpeg-python](https://kkroening.github.io/ffmpeg-python/)

The latter explicitly supports [concat](https://kkroening.github.io/ffmpeg-python/#ffmpeg.concat), as well
as other features I'll likely soon use.  So we are running with this as our core library.

