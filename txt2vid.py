from moviepy.editor import TextClip, VideoFileClip, concatenate_videoclips, CompositeVideoClip
from gtts import gTTS
import os

from transformers import MarianMTModel, MarianTokenizer

def translate_english_to_hindi(text):
    model_name = "Helsinki-NLP/opus-mt-en-hi"
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model = MarianMTModel.from_pretrained(model_name)

    inputs = tokenizer.encode(">>en<<" + text, return_tensors="pt")
    outputs = model.generate(inputs, max_length=200, num_return_sequences=1, no_repeat_ngram_size=2)

    translated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return translated_text

width, height = 1920, 1080
duration = 3
custom_position = (-200, 0)

def floating_text_animation(text_clip, start_pos, end_pos, start_time, end_time, speed=2.0):
    def move_position(t):
        progress = ((t - start_time) * speed) / (end_time - start_time)
        x = start_pos[0] + progress * (end_pos[0] - start_pos[0])
        y = start_pos[1] + progress * (end_pos[1] - start_pos[1])
        return x, y
    return text_clip.set_position(move_position)

# Sample Use Case for Train Station: Using Gif
# Similarly PNG / JPG / MP4 formmats can be used with any text
background_type = "gif"  
background_path = "bus.gif"  
station = "Okhla Bird Sanctuary"

text_en = f"Welcome to {station}"
txt_clip_en = TextClip(text_en, fontsize=70, color='black', stroke_color='black', stroke_width=1.5, size=(width, height))
txt_clip_en = txt_clip_en.set_duration(duration)
txt_clip_en = floating_text_animation(txt_clip_en, start_pos=custom_position, end_pos=(250, 0), start_time=0, end_time=duration, speed=6)

translated_text = translate_english_to_hindi(text_en)
print("Translated text in Hindi:", translated_text)
text_hi = translated_text
txt_clip_hi = TextClip(text_hi, fontsize=70, color='black', stroke_color='black', stroke_width=1.5, size=(width, height))
txt_clip_hi = txt_clip_hi.set_duration(duration)
txt_clip_hi = floating_text_animation(txt_clip_hi, start_pos=custom_position, end_pos=(250, 0), start_time=0, end_time=duration, speed=3)


if background_type == "image":
    background_clip = ImageClip(background_path, duration=duration)
elif background_type == "video":
    background_clip = VideoFileClip(background_path)
    background_clip = background_clip.subclip(0, duration)  
else:  
    gif_clip = VideoFileClip(background_path)

    num_repeats = int(duration / gif_clip.duration) + 1

    background_clip = concatenate_videoclips([gif_clip] * num_repeats)
    background_clip = background_clip.subclip(0, duration)  

background_clip = background_clip.resize(height=height)

video_en = CompositeVideoClip([background_clip, txt_clip_en])
video_hi = CompositeVideoClip([background_clip, txt_clip_en])

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

video_en = VideoFileClip(combined_output_file_en)
video_hi = VideoFileClip(combined_output_file_hi)
final_video = concatenate_videoclips([video_en, video_hi])

output_file_combined = "final_combined_video.mp4"

final_video.write_videofile(output_file_combined, codec='libx264', fps=24)

os.remove(output_file_en)
os.remove(output_file_hi)
os.remove(combined_output_file_en)
os.remove(combined_output_file_hi)
os.remove("speech_en.mp3")
os.remove("speech_hi.mp3")
