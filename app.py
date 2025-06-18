from flask import Flask, request, send_file
import tempfile
from moviepy.editor import ImageClip, AudioFileClip

app = Flask(__name__)

@app.route('/generate-video', methods=['POST'])
def generate_video():
    image_data = request.files.get('image')
    audio_data = request.files.get('audio')

    if not image_data or not audio_data:
        return "Image or Audio not provided", 400

    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as img_file, \
         tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as audio_file:

        img_file.write(image_data.read())
        audio_file.write(audio_data.read())
        img_path = img_file.name
        audio_path = audio_file.name

    output_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4").name

    clip = ImageClip(img_path).set_duration(AudioFileClip(audio_path).duration)
    clip = clip.set_audio(AudioFileClip(audio_path))
    clip.write_videofile(output_path, codec="libx264", fps=24)

    return send_file(output_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
