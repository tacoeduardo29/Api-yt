from flask import Flask, request, Response
from flask_cors import CORS
import yt_dlp
import requests
import re

app = Flask(__name__)
CORS(app)

def limpiar_nombre(text):
    # Quita caracteres que no le gustan a Windows/Android en nombres de archivos
    return re.sub(r'[\\/*?:"<>|]', "", text)

@app.route('/descargar')
def descargar():
    url = request.args.get('url')
    if not url:
        return "Error: Falta URL", 400
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            link_directo = info['url']
            # Obtenemos el título real y lo limpiamos
            titulo_sucio = info.get('title', 'musica_tacoeduardo')
            titulo_final = limpiar_nombre(titulo_sucio)

            # Hacemos el tunel de datos (streaming)
            req = requests.get(link_directo, stream=True)
            
            # El secreto está en 'Content-Disposition'
            return Response(
                req.iter_content(chunk_size=1024*1024), # Procesamos por bloques de 1MB
                content_type='audio/mpeg',
                headers={
                    "Content-Disposition": f"attachment; filename=\"{titulo_final}.mp3\""
                }
            )
    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == "__main__":
    app.run()
