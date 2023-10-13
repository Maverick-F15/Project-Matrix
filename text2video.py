from moviepy.editor import TextClip, ImageClip, CompositeVideoClip
from gtts import gTTS
import os

width, height = 1920, 1080
duration = 5

text = "Hogsmeade Station"
txt_clip = TextClip(text, fontsize=70, color='black',
                    stroke_color='black', stroke_width=1.5, size=(width, height))
txt_clip = txt_clip.set_duration(duration)
custom_position = (-250, 0)
txt_clip = txt_clip.set_pos(custom_position)

image_path = "download.png"
image_clip = ImageClip(image_path, duration=duration)
image_clip = image_clip.resize(height=height)
image_clip = image_clip.set_pos('center')

video = CompositeVideoClip([image_clip, txt_clip])
output_file = "text_video_with_image_background.mp4"
video.write_videofile(output_file, codec='libx264', fps=24)

speech_text = f"We will arrive {text}, in 2 minutes"
speech_output_file = "speech.mp3"
language = 'en'

tts = gTTS(text=speech_text, lang=language, slow=False)
tts.save(speech_output_file)

combined_output_file = "combined_video.mp4"
os.system(f'ffmpeg -i {output_file} -i {speech_output_file} -c:v copy -c:a aac -strict experimental {combined_output_file}')

os.remove(output_file)
os.remove(speech_output_file)
