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
    let body = '';
    for await (const chunk of req) body += chunk;
    const data = JSON.parse(body);
    const text = data.text || '';

    if (!text) return res.status(400).json({ error: 'No text' });

    console.log('[TTS] "' + text.substring(0, 60) + '"');

    const audio = await new Promise((resolve, reject) => {
      const payload = JSON.stringify({ text: text });
      const r = https.request({
        hostname: 'api.deepgram.com',
        path: '/v1/speak?model=aura-asteria-en',
        method: 'POST',
        headers: {
          'Authorization': 'Token ' + DG_KEY,
          'Content-Type': 'application/json',
          'Content-Length': Buffer.byteLength(payload)
        }
      }, resp => {
        const chunks = [];
        resp.on('data', c => chunks.push(c));
        resp.on('end', () => resolve(Buffer.concat(chunks)));
      });
      r.on('error', reject);
      r.write(payload);
      r.end();
    });

    console.log('[TTS] Got ' + audio.length + ' bytes');
    res.setHeader('Content-Type', 'audio/mpeg');
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Cache-Control', 'no-cache, no-store, must-revalidate');
    res.end(audio);
  } catch (e) {
    console.error('[TTS] Error:', e.message);
    res.status(500).json({ error: e.message });
  }
};
