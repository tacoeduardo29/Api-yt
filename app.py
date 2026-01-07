from flask import Flask, request, redirect
from flask_cors import CORS # IMPORTANTE
import yt_dlp

app = Flask(__name__)
CORS(app) # ESTO DA EL PERMISO


@app.route('/descargar')
def descargar():
    url = request.args.get('url')
    if not url:
        return "Error: Pega un link de YouTube", 400
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            # Obtenemos el link directo de los servidores de Google/YouTube
            link_directo = info['url']
            return redirect(link_directo)
    except Exception as e:
        return f"Error en el motor: {str(e)}", 500

if __name__ == "__main__":
    app.run()