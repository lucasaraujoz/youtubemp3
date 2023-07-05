from flask import Flask, render_template, request, send_file
import yt_dlp
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        url = request.form['url']
        try:
            URLS = [url]
            ydl_opts = {
                'format': 'm4a/bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'm4a',
                }],
                'o': '/output/%(title)s.%(ext)s'  # Define o padrão de nomeação e o diretório de destino

            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
                return send_file(filename, as_attachment=True)
        except Exception as e:
            message = f'Ocorreu um erro ao processar o vídeo. Detalhes: {str(e)}'
            return render_template('index.html', message=message)
    return render_template('index.html')
@app.route('/hello', methods=['POST'])
def say_hello():
    os.system('shutdown now')
    print('Olá!')
    return render_template('index.html')
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
