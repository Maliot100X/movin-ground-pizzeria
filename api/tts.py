"""Deepgram TTS - Vercel Serverless Function"""
import json
import urllib.request

DG_KEY = 'ffbf23cb49159c3d5699587c20f1debecb819fc5'
DG_TTS_URL = 'https://api.deepgram.com/v1/speak'

def handler(request):
    if request.method == 'OPTIONS':
        return Response(
            status=204,
            body='',
            headers={
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            }
        )

    if request.method != 'POST':
        return Response(status=405, body='Method not allowed')

    try:
        body_data = json.loads(request.body)
        text = body_data.get('text', '')
        if not text:
            return Response(
                status=400,
                body=json.dumps({'error': 'No text provided'}),
                headers={'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}
            )

        payload = json.dumps({'text': text}).encode('utf-8')
        req = urllib.request.Request(
            DG_TTS_URL,
            data=payload,
            headers={
                'Authorization': 'Token ' + DG_KEY,
                'Content-Type': 'application/json'
            }
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            audio_data = resp.read()
            content_type = resp.headers.get('Content-Type', 'audio/mpeg')

        return Response(
            status=200,
            body=audio_data,
            headers={
                'Content-Type': content_type,
                'Access-Control-Allow-Origin': '*',
                'Content-Length': str(len(audio_data))
            }
        )
    except Exception as e:
        return Response(
            status=500,
            body=json.dumps({'error': str(e)}),
            headers={'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}
        )


class Response:
    def __init__(self, status=200, body='', headers=None):
        self.status = status
        self.body = body if isinstance(body, str) else body
        self.headers = headers or {'Content-Type': 'application/json'}
        if 'Content-Length' not in self.headers:
            b = self.body if isinstance(self.body, bytes) else self.body.encode('utf-8')
            self.headers['Content-Length'] = str(len(b))
