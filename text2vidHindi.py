from moviepy.editor import TextClip, ImageClip, CompositeVideoClip
from gtts import gTTS
import os

text = "Hogsmeade Station"

text_en = "we will arrive in 2 minutes"
duration_en = 4

text_hi = "हम 2 मिनट में पहुंच जाएंगे"
duration_hi = 4

width, height = 1920, 1080
custom_position = (-250, 0)
image_path = "download.png"

txt_clip_en = TextClip(text, fontsize=70, color='black', stroke_color='black', stroke_width=1.5, size=(width, height))
txt_clip_en = txt_clip_en.set_duration(duration_en)
txt_clip_en = txt_clip_en.set_pos(custom_position)

txt_clip_hi = TextClip(text, fontsize=70, color='black', stroke_color='black', stroke_width=1.5, size=(width, height))
txt_clip_hi = txt_clip_hi.set_duration(duration_hi)
txt_clip_hi = txt_clip_hi.set_pos(custom_position)

image_clip = ImageClip(image_path, duration=duration_en)  # Duration is set to match the longer text duration
image_clip = image_clip.resize(height=height)
image_clip = image_clip.set_pos('center')

video_en = CompositeVideoClip([image_clip, txt_clip_en])
video_hi = CompositeVideoClip([image_clip, txt_clip_hi])

output_file_en = "text_video_en.mp4"
output_file_hi = "text_video_hi.mp4"

video_en.write_videofile(output_file_en, codec='libx264', fps=24)
video_hi.write_videofile(output_file_hi, codec='libx264', fps=24)

speech_texts = [text_en, text_hi]
speech_output_files = ["speech_en.mp3", "speech_hi.mp3"]
languages = ['en', 'hi']

for i, speech_text in enumerate(speech_texts):
    tts = gTTS(text=speech_text, lang=languages[i], slow=False)
    tts.save(speech_output_files[i])

combined_output_file_en = "combined_video_en.mp4"
combined_output_file_hi = "combined_video_hi.mp4"

os.system(f'ffmpeg -i {output_file_en} -i speech_en.mp3 -c:v copy -c:a aac -strict experimental {combined_output_file_en}')
os.system(f'ffmpeg -i {output_file_hi} -i speech_hi.mp3 -c:v copy -c:a aac -strict experimental {combined_output_file_hi}')

os.remove(output_file_en)
os.remove(output_file_hi)
os.remove("speech_en.mp3")
os.remove("speech_hi.mp3")

from moviepy.editor import concatenate_videoclips, VideoFileClip

video_en = VideoFileClip("combined_video_en.mp4")
video_hi = VideoFileClip("combined_video_hi.mp4")

final_video = concatenate_videoclips([video_en, video_hi])
output_file = "final_combined_video.mp4"
final_video.write_videofile(output_file, codec='libx264', fps=24)

# os.remove("combined_video_en.mp4")
# os.remove("combined_video_hi.mp4")
