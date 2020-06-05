# Hogwarts House Pride
This is a bot that takes a bunch of videos and an audio as inputs and gives a self-esteem boosting Hogwarts House Pride video.

### How to use
1. Put all the input video files and clips in the "Input" directory.
2. Change the words in the `words.py` file according to the *qualities* of a particular house.
3. Run the `pride.py` using Python3.
4. Enter the duration of the video, the background musicfile name & the Hogwarts house name.
5. Finally you'll get an output file named "final-vdieo.mp4".

### Dependencies
1. moviepy 1.0.3
2. Also install the latest version of ImageMagick.\n
If you are on Windows, then to use ImageMagick you have to manually update the "default_config.py" file in moviepy.
    Just add the following line to the file.
    IMAGEMAGICK_BINARY = "<file\\path\\to\\magick.exe>"


