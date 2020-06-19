import os
from random import randint
from moviepy.editor import *
from moviepy.video.fx.all import fadein, fadeout
import itertools
from words import word_list


desired_duration = int(input("Desired edit duration in seconds : "))
music_file = input("Background-music file name : ")
vid_directory = input("video-clips folder name : ")


ABS_PATH = os.path.abspath(__file__)
BASE_DIR = os.path.dirname(ABS_PATH)
VID_DIR = os.path.join(BASE_DIR, vid_directory)
final_audio_video_path = os.path.join(BASE_DIR, "final-video.mp4")


overlay_1 = VideoFileClip("overlay_1.mp4")
overlay_2 = VideoFileClip("overlay_2.mp4")
overlay_3 = VideoFileClip("overlay_3.mp4")


class Potions_pot:
    def __init__(self, music, video_folder):
        super().__init__()
        self.total_duration = 0
        self.f_clips = []
        self.final_clip = None
        self.final_video = None
        self.final_overlay = None


    def generate(self):
        self.add_clips(desired_duration)
        self.word_overlay()
        self.add_music()

        
    def add_clips(self, desired_duration):
        for (root, dirs, files) in os.walk(VID_DIR):
            print(files)
        
        for fname in itertools.cycle(files):
            source_path = os.path.join(VID_DIR, fname)
            clip_1 = VideoFileClip(source_path)
            r = randint(0, int(clip_1.duration - 10))
            subclip = clip_1.subclip(r, (r + 4 + (r % 3) + (r % 3)))
            merged = CompositeVideoClip(
                [
                    subclip.resize( (1920,1080) ),
                    overlay_3.subclip(0, (4 + (r % 3) + (r % 3))).resize( (1920,1080) ).set_opacity(0.25),
                    overlay_2.subclip(0, (4 + (r % 3) + (r % 3))).resize( (1920,1080) ).set_opacity(0.25)
                ]
            )
            merged = merged.set_position(("center", "top"))
            if r % 2 == 1:  # adds a fade_in transition if r is odd.
                merged = fadein(merged, 1.5)
            self.f_clips.append(merged)
            self.total_duration += 4 + (r % 3) + (r % 3)
            if self.total_duration < desired_duration:
                continue
            else:
                break
            
        self.final_clip = concatenate_videoclips(self.f_clips)
        print('Final clip duration = {} secs'.format(self.final_clip.duration))
        print('Length of word list = ', (len(word_list)))

        
    def word_overlay(self):
        w, h = self.final_clip.size
        word_clips = []
        for word in word_list:
            watermark_text = (
                TextClip(
                    word, font="Bell-MT-Italic", fontsize=60, color="white", align="center", size=(w, 250) 
                )
                .fadein(0.5)
                .set_duration(self.final_clip.duration / len(word_list))
            )
            watermark_text = watermark_text.set_position(("center", "top"))
            watermark_text = watermark_text.margin(top=480, opacity=0)
            word_clips.append(watermark_text)
        word_merged = concatenate_videoclips(word_clips)
        final_merged = CompositeVideoClip([self.final_clip, word_merged.set_opacity(0.45)])

        ### INTRO TEXT ###
        intro_text = (
            TextClip(
                "Gryffindor",
                size=self.final_clip.size,
                fontsize=120,
                color="#ffc500",
                bg_color="#7f0909",
                font="Rage-Italic"
            )
            .set_duration(2)
            .set_position("center")
            .fadein(0.5)
            .fadeout(0.5)
        )
        
        self.final_video = concatenate_videoclips([intro_text, final_merged]) 
        self.final_overlay = CompositeVideoClip([self.final_video, overlay_1.resize(self.final_video.size).set_opacity(0.25).set_duration(self.final_video.duration)])

        
    def add_music(self):
        source_audio_path = os.path.join(BASE_DIR, music_file)  
        dur = self.final_overlay.duration
        bg_audio = AudioFileClip(source_audio_path).subclip(0, dur)
        final_av_clip = self.final_overlay.set_audio(bg_audio)
        final_av_clip.write_videofile(final_audio_video_path, fps=60)


g = Potions_pot(music = music_file, video_folder = vid_directory)
g.generate()