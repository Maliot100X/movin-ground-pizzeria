"""Deepgram STT - Vercel Python Function"""
import json
import urllib.request
import os

DG_KEY = os.environ.get('DEEPGRAM_API_KEY', 'ffbf23cb49159c3d5699587c20f1debecb819fc5')
DG_URL = 'https://api.deepgram.com/v1/listen?model=nova-2&language=de&smart_format=true'

def handler(request):
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
    }

    if request.method == 'OPTIONS':
        return {'statusCode': 204, 'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type'
        }}

    if request.method != 'POST':
        return {'statusCode': 405, 'headers': headers, 'body': json.dumps({'error': 'Method not allowed'})}

    try:
        body = request.body
        if isinstance(body, str):
            body = body.encode()
        if not body or len(body) < 100:
            return {'statusCode': 400, 'headers': headers, 'body': json.dumps({'error': 'No audio data'})}

        req = urllib.request.Request(DG_URL, data=body,
            headers={'Authorization': 'Token ' + DG_KEY, 'Content-Type': 'audio/wav'})
        with urllib.request.urlopen(req, timeout=15) as resp:
            result = json.loads(resp.read())

        t = ''
        ch = result.get('results', {}).get('channels', [])
        if ch and ch[0].get('alternatives'):
            t = ch[0]['alternatives'][0].get('transcript', '')

        return {'statusCode': 200, 'headers': headers, 'body': json.dumps({'transcript': t})}
    except Exception as e:
        return {'statusCode': 500, 'headers': headers, 'body': json.dumps({'error': str(e)})}
