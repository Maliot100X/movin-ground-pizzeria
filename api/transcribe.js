const https = require('https');

module.exports = async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') return res.status(204).end();
  if (req.method !== 'POST') return res.status(405).json({error:'Method not allowed'});

  const DG_KEY = process.env.DEEPGRAM_API_KEY || 'ffbf23cb49159c3d5699587c20f1debecb819fc5';
  
  try {
    const chunks = [];
    for await (const chunk of req) chunks.push(chunk);
    const audio = Buffer.concat(chunks);
    
    if (audio.length < 100) {
      return res.status(400).json({error:'No audio data'});
    }

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
        resp.on('end', () => resolve(JSON.parse(d)));
      });
      r.on('error', reject);
      r.write(audio);
      r.end();
    });

    let t = '';
    const ch = result?.results?.channels;
    if (ch && ch[0]?.alternatives) t = ch[0].alternatives[0]?.transcript || '';
    
    res.setHeader('Content-Type', 'application/json');
    res.json({transcript: t});
  } catch(e) {
    res.status(500).json({error: e.message});
  }
};
