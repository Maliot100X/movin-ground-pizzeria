const https = require('https');

module.exports = async function handler(req, res) {
  if (req.method === 'OPTIONS') {
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
    return res.status(204).end();
  }

  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  const DG_KEY = process.env.DEEPGRAM_API_KEY || 'ffbf23cb49159c3d5699587c20f1debecb819fc5';

  try {
    const chunks = [];
    for await (const chunk of req) chunks.push(chunk);
    const audio = Buffer.concat(chunks);

    if (audio.length < 100) {
      return res.status(400).json({ error: 'No audio data' });
    }

    console.log('[STT] Received ' + audio.length + ' bytes');

    const result = await new Promise((resolve, reject) => {
      const r = https.request({
        hostname: 'api.deepgram.com',
        path: '/v1/listen?model=nova-2&language=de&smart_format=true',
        method: 'POST',
        headers: {
          'Authorization': 'Token ' + DG_KEY,
          'Content-Type': 'audio/wav',
          'Content-Length': audio.length
        }
      }, resp => {
        let d = '';
        resp.on('data', c => d += c);
        resp.on('end', () => {
          try { resolve(JSON.parse(d)); }
          catch(e) { reject(new Error('Parse error')); }
        });
      });
      r.on('error', reject);
      r.write(audio);
      r.end();
    });

    let t = '';
    const ch = result && result.results && result.results.channels;
    if (ch && ch[0] && ch[0].alternatives && ch[0].alternatives[0]) {
      t = ch[0].alternatives[0].transcript || '';
    }

    console.log('[STT] Result: "' + t + '"');
    res.setHeader('Content-Type', 'application/json');
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.json({ transcript: t });
  } catch (e) {
    console.error('[STT] Error:', e.message);
    res.status(500).json({ error: e.message });
  }
};
