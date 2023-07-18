from flask import Flask, render_template, request
import yt_dlp
import ffmpeg
import pathlib
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        url = request.form['url']
        format = request.form['format']
        try:
            filename = download_video(url, format)
            fp = open(filename, "rb")
            def stream():
                yield from fp
                fp.close()
                os.remove(filename)
            return app.response_class(
                stream(), 
                headers={'Content-Disposition': f'attachment; filename={pathlib.Path(filename).name}'},
                mimetype=f"audio/{format}"
            )
        except Exception as e:
            return render_template('index.html', message=str(e))

    return render_template('index.html')

def download_video(url, format):
    if format not in ["3gp","aac","flv","m4a","mp3","mp4","ogg","wav","webm"]:
        raise "Formato indisponível, escolha uma das opções: [3gp, aac, flv, m4a, mp3, mp4, ogg, wav, webm]."
    
    ydl_opts = {
        'format': "bestaudio",
        'o': '/output/%(title)s.%(ext)s'  # Define o padrão de nomeação e o diretório de destino
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)

    ext = pathlib.Path(filename).suffix
    if format != ext:
        new_filename = filename.replace(ext, "."+format)
        downloaded = ffmpeg.input(filename)
        converted = ffmpeg.output(downloaded, new_filename)
        ffmpeg.run(converted, overwrite_output=True)
        os.remove(filename)
        return new_filename
    
    return filename

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
