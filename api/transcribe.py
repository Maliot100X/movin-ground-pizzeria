"""Deepgram STT - Vercel Serverless Function"""
from http.server import BaseHTTPRequestHandler
import json
import urllib.request
import os

DG_KEY = os.environ.get('DEEPGRAM_API_KEY', 'ffbf23cb49159c3d5699587c20f1debecb819fc5')
DG_URL = 'https://api.deepgram.com/v1/listen?model=nova-2&language=de&smart_format=true'

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_POST(self):
        try:
            length = int(self.headers.get('Content-Length', 0))
            audio = self.rfile.read(length)
            print(f'[STT] Got {length} bytes')
            if length < 100:
                self._json(400, {'error': 'No audio data'})
                return
            req = urllib.request.Request(DG_URL, data=audio,
                headers={'Authorization': 'Token ' + DG_KEY, 'Content-Type': 'audio/wav'})
            with urllib.request.urlopen(req, timeout=15) as resp:
                result = json.loads(resp.read())
            t = ''
            ch = result.get('results', {}).get('channels', [])
            if ch and ch[0].get('alternatives'):
                t = ch[0]['alternatives'][0].get('transcript', '')
            print(f'[STT] Result: "{t}"')
            self._json(200, {'transcript': t})
        except Exception as e:
            print(f'[STT] Error: {e}')
            self._json(500, {'error': str(e)})

    def _json(self, code, data):
        body = json.dumps(data).encode()
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        pass
