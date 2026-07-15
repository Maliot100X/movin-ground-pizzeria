"""Deepgram TTS - Vercel Python Function"""
import json
import base64
import urllib.request
import os

DG_KEY = os.environ.get('DEEPGRAM_API_KEY', 'ffbf23cb49159c3d5699587c20f1debecb819fc5')
DG_TTS_URL = 'https://api.deepgram.com/v1/speak'

def handler(request):
    if request.method == 'OPTIONS':
        return {'statusCode': 204, 'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type'
        }}

    if request.method != 'POST':
        return {'statusCode': 405, 'headers': {'Content-Type': 'application/json'}, 'body': json.dumps({'error': 'Method not allowed'})}

    try:
        body = request.body
        if isinstance(body, bytes):
            body = body.decode()
        data = json.loads(body)
        text = data.get('text', '')
        if not text:
            return {'statusCode': 400, 'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}, 'body': json.dumps({'error': 'No text'})}

        payload = json.dumps({'text': text}).encode()
        req = urllib.request.Request(DG_TTS_URL, data=payload,
            headers={'Authorization': 'Token ' + DG_KEY, 'Content-Type': 'application/json'})
        with urllib.request.urlopen(req, timeout=30) as resp:
            audio = resp.read()
            ct = resp.headers.get('Content-Type', 'audio/mpeg')

        encoded = base64.b64encode(audio).decode()
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': ct,
                'Access-Control-Allow-Origin': '*',
                'Content-Length': str(len(audio))
            },
            'isBase64Encoded': True,
            'body': encoded
        }
    except Exception as e:
        return {'statusCode': 500, 'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}, 'body': json.dumps({'error': str(e)})}
