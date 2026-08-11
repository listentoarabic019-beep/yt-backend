from flask import Flask, request, send_file
from flask_cors import CORS
import subprocess
import os
import time

app = Flask(__name__)
CORS(app)

@app.route('/cut')
def cut():
    try:
        url = request.args.get('url')
        start = request.args.get('start', '0')
        end = request.args.get('end', '10')
        uid = str(int(time.time()))
        out = f'/tmp/{uid}.mp4'
        
        cmd = ['yt-dlp', '-f', 'best[ext=mp4]', '--download-sections', f'*{start}-{end}', '-o', out, url]
        subprocess.run(cmd, timeout=120)
        
        if not os.path.exists(out):
            return {'error': 'Failed'}, 500
        
        return send_file(out, as_attachment=True, download_name=f'cut-{uid}.mp4')
    except Exception as e:
        return {'error': str(e)}, 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
