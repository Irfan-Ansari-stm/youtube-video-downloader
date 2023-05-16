from flask import Flask, render_template, request,session
from pytube import YouTube

app = Flask(__name__)

app.config.update(
    TESTING=True,
    SECRET_KEY='192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf'
)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        session['link'] = request.form.get('url')
        try:
            url = YouTube(session['link'])
            url.check_availability()
            resolutions = get_available_resolutions(url)
            audio_info = get_audio_info(url)
                      
        except:
            return render_template('error.html') 

        return render_template('download.html',url=url,resolutions=resolutions,audio_info=audio_info)
    
    return render_template('index.html')

def get_available_resolutions(youtube):
    resolutions = []
    for stream in youtube.streams:
        if stream.resolution and stream.resolution not in resolutions:
            size_in_bytes = stream.filesize
            size_in_mb = size_in_bytes / (1024 * 1024)
            resolutions.append((stream.resolution, size_in_mb))
    return resolutions


def get_audio_info(video_url):
    youtube = YouTube(video_url)
    audio_info = []

    for stream in youtube.streams.filter(only_audio=True):
        format_info = stream.mime_type.split('/')[1]
        size_info = get_formatted_size(stream.filesize)
        audio_info.append({'format': format_info, 'size': size_info})

    return audio_info

def get_formatted_size(size_in_bytes):
    size_in_mb = size_in_bytes / (1024 * 1024)
    return f"{size_in_mb:.2f} MB"

if __name__ == '__main__':
    app.run(debug='True') 
