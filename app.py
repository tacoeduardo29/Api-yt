from flask import Flask, request, Response
from flask_cors import CORS
import yt_dlp
import requests

app = Flask(__name__)
CORS(app)

@app.route('/descargar')
def descargar():
    url = request.args.get('url')
    if not url:
        return "Error: Pega un link de YouTube", 400
    
    # Configuramos yt-dlp para obtener el link de audio
    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            link_directo = info['url']
            titulo = info.get('title', 'musica_tacoeduardo').replace('"', '')

            # En lugar de redireccionar, nosotros descargamos y enviamos el flujo
            # Esto evita que el navegador bloquee la descarga
            response = requests.get(link_directo, stream=True)
            
            def generate():
                for chunk in response.iter_content(chunk_size=4096):
                    yield chunk

            return Response(
                generate(),
                content_type='audio/mpeg',
                headers={
                    "Content-Disposition": f"attachment; filename=\"{titulo}.mp3\"",
                    "Access-Control-Allow-Origin": "*"
                }
            )
    except Exception as e:
        return f"Error en el motor: {str(e)}", 500

if __name__ == "__main__":
    app.run()
