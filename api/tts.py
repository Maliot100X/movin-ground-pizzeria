"""Deepgram TTS - Vercel Serverless Function"""
from http.server import BaseHTTPRequestHandler
import json
import urllib.request
import os

DG_KEY = os.environ.get('DEEPGRAM_API_KEY', 'ffbf23cb49159c3d5699587c20f1debecb819fc5')
DG_TTS_URL = 'https://api.deepgram.com/v1/speak'

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
            body = json.loads(self.rfile.read(length))
            text = body.get('text', '')
            if not text:
                self._json(400, {'error': 'No text provided'})
                return
            print(f'[TTS] Synthesizing: "{text}"')
            payload = json.dumps({'text': text}).encode()
            req = urllib.request.Request(DG_TTS_URL, data=payload,
                headers={'Authorization': 'Token ' + DG_KEY, 'Content-Type': 'application/json'})
            with urllib.request.urlopen(req, timeout=30) as resp:
                audio = resp.read()
                ct = resp.headers.get('Content-Type', 'audio/mpeg')
            print(f'[TTS] Got {len(audio)} bytes')
            self.send_response(200)
            self.send_header('Content-Type', ct)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-Length', str(len(audio)))
            self.end_headers()
            self.wfile.write(audio)
        except Exception as e:
            print(f'[TTS] Error: {e}')
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
