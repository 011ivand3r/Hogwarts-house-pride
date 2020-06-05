import os
from random import randint
from moviepy.editor import *
from moviepy.video.fx.all import fadein, fadeout
import itertools
from words import word_list


ABS_PATH = os.path.abspath(__file__)
BASE_DIR = os.path.dirname(ABS_PATH)
VID_DIR = os.path.join(BASE_DIR, "Input")
desired_duration = int(input("Edit duration in seconds: "))
music_file = input("Name of the background music file: ")
house_name = input("Name of the house: ")

final_audio_video_path = os.path.join(BASE_DIR, "final-video.mp4")

for (root, dirs, files) in os.walk(VID_DIR):
    print(files)

overlay_1 = VideoFileClip("overlay_1.mp4")
overlay_2 = VideoFileClip("overlay_2.mp4")
overlay_3 = VideoFileClip("overlay_3.mp4")

f_clips = []
total_duration = 0
for fname in itertools.cycle(files):
    source_path = os.path.join(VID_DIR, fname)
    clip_1 = VideoFileClip(source_path)
    r = randint(0, int(clip_1.duration - 13))
    subclip = clip_1.subclip(r, (r + 5 + (r % 8)))
    merged = CompositeVideoClip(
        [
            subclip,
            overlay_3.subclip(0, (5 + r % 8)).resize(subclip.size).set_opacity(0.30),
            overlay_2.subclip(0, (5 + r % 8)).resize(subclip.size).set_opacity(0.30),
        ]
    )
    if r % 2 == 1:  # adds a fade_in transition if r is odd.
        merged = fadein(merged, 3)
    f_clips.append(merged)
    total_duration += 5 + r % 8
    if total_duration < desired_duration:
        continue
    else:
        break

final_clip = concatenate_videoclips(f_clips)

print("Final clip duration = {} secs".format(final_clip.duration))
print("Length of word list = {}".format(len(word_list)))

w, h = final_clip.size
word_clips = []
for word in word_list:
    watermark_text = (
        TextClip(
            word,
            font="Bell-MT-Italic",
            fontsize=80,
            color="white",
            align="center",
            size=(w, 250),
            kerning=3,
        )
        .set_position("top")
        .fadein(0.5)
        .set_duration(final_clip.duration / len(word_list))
    )
    watermark_text = watermark_text.margin(top=680, opacity=0)
    word_clips.append(watermark_text)

word_merged = concatenate_videoclips(word_clips)
final_merged = CompositeVideoClip([final_clip, word_merged.set_opacity(0.45)])


### INTRO TEXT ###
intro_text = (
    TextClip(
        house_name,
        size=final_clip.size,
        fontsize=200,
        color="#fff",
        bg_color="#000",
        font="Rage-Italic",
        kerning=15,
    )
    .set_duration(3)
    .set_position("center")
    .fadein(0.5)
    .fadeout(0.5)
)


### ENDING IMAGE ###
image_clip = (
    ImageClip("ending-image.jpg")
    .resize(final_merged.size)
    .set_duration(3)
    .set_opacity(0.8)
)

final_intro_clip = concatenate_videoclips([intro_text, final_merged, image_clip])

final_overlay = CompositeVideoClip(
    [final_intro_clip, overlay_1.resize(final_intro_clip.size).set_opacity(0.20)]
)


### AUDIO ###
source_audio_path = os.path.join(BASE_DIR, music_file)
dur = final_overlay.duration
bg_audio = AudioFileClip(source_audio_path).subclip(0, dur)
final_av_clip = final_overlay.set_audio(bg_audio.set_start(6))
final_av_clip.write_videofile(final_audio_video_path, fps=60)
