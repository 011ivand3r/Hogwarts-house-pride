# Hogwarts House Pride
This is a bot that takes a bunch of videos and an audio as inputs and gives a self-esteem boosting Hogwarts House Pride video.

### How to use
1. Put all the clips you want to mash up in a folder, and put it in the same directory as `pride.py`.
2. Change the words in the `words.py` file according to the *qualities* of a particular Hogwarts house.
3. Run `pride.py` using Python3.
4. Enter the following.
    - Duration of the video
    - The background musicfile name 
    - The video-clips folder name
5. Finally you'll get an output file named "final-video.mp4".

### Dependencies
- moviepy 1.0.3
- Also install the latest version of [ImageMagick](https://imagemagick.org/script/download.php).
- If you are on Windows, then to use ImageMagick you will have to manually update the "default_config.py" file in moviepy.\
Just add the following line to the file.\
```IMAGEMAGICK_BINARY = "<file\\path\\to\\magick.exe>"```


