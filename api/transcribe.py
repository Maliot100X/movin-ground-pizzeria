"""Deepgram STT - Vercel Serverless Function"""
import json
import urllib.request

DG_KEY = 'ffbf23cb49159c3d5699587c20f1debecb819fc5'
DG_URL = 'https://api.deepgram.com/v1/listen?model=nova-2&language=de&smart_format=true'

def handler(request):
    if request.method != 'POST':
        return Response(status=405, body='Method not allowed')

    try:
        body = request.body
        if not body or len(body) < 100:
            return Response(
                status=400,
                body=json.dumps({'error': 'No audio data'}),
                headers={'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}
            )

        req = urllib.request.Request(
            DG_URL,
            data=body,
            headers={
                'Authorization': 'Token ' + DG_KEY,
                'Content-Type': 'audio/wav'
            }
        )
        with urllib.request.urlopen(req, timeout=15) as resp:
            result = json.loads(resp.read())

        t = ''
        ch = result.get('results', {}).get('channels', [])
        if ch and ch[0].get('alternatives'):
            t = ch[0]['alternatives'][0].get('transcript', '')

        return Response(
            status=200,
            body=json.dumps({'transcript': t}),
            headers={'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}
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
        self.body = body if isinstance(body, str) else json.dumps(body)
        self.headers = headers or {'Content-Type': 'application/json'}
        if 'Content-Length' not in self.headers:
            self.headers['Content-Length'] = str(len(self.body.encode('utf-8') if isinstance(self.body, str) else self.body))
