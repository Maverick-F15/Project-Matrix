from moviepy.editor import TextClip, ImageClip, CompositeVideoClip
from gtts import gTTS
import os

# Define the text you want to display and speak
text = "Train will arrive at 2"

# Set the size of the video (width x height)
width, height = 1920, 1080  # Full HD resolution

# Set the duration of the video (in seconds)
duration = 10  # 10 seconds

# Create a TextClip with the specified text, fontsize, and color
txt_clip = TextClip(text, fontsize=70, color='black', stroke_color='black', stroke_width=1.5, size=(width, height))

# Set the duration of the text clip
txt_clip = txt_clip.set_duration(duration)

# Set the position of the text clip (centered)
txt_clip = txt_clip.set_pos('center')

# Load the GIF for the background
gif_path = "background.gif"
gif_clip = ImageClip(gif_path, duration=duration)

# Resize the GIF by specifying the width (height will be adjusted to maintain aspect ratio)
gif_clip = gif_clip.resize(width=width)

# Set the position of the resized GIF (centered)
gif_clip = gif_clip.set_pos('center')

# Composite the text clip on the resized GIF background
video = CompositeVideoClip([gif_clip, txt_clip])

# Set the output file name
output_file = "text_video_with_resized_gif_background.mp4"

# Write the video file
video.write_videofile(output_file, codec='libx264', fps=24)

# Convert text to speech using gTTS
speech_text = text
speech_output_file = "speech.mp3"
language = 'en'  # Language (English in this case)

tts = gTTS(text=speech_text, lang=language, slow=False)

# Save the speech to an MP3 file
tts.save(speech_output_file)

# Combine the video and speech using ffmpeg
combined_output_file = "combined_video.mp4"
os.system(f'ffmpeg -i {output_file} -i {speech_output_file} -c:v copy -c:a aac -strict experimental {combined_output_file}')

# Optionally, you can remove the individual video, speech, and temporary video with the GIF background files
os.remove(output_file)
os.remove(speech_output_file)
