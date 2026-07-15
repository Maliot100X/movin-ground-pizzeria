const https = require('https');

module.exports = async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') return res.status(204).end();
  if (req.method !== 'POST') return res.status(405).json({error:'Method not allowed'});

  const DG_KEY = process.env.DEEPGRAM_API_KEY || 'ffbf23cb49159c3d5699587c20f1debecb819fc5';

  try {
    const {text} = req.body;
    if (!text) return res.status(400).json({error:'No text'});

    const audio = await new Promise((resolve, reject) => {
      const r = https.request({
        hostname: 'api.deepgram.com',
        path: '/v1/speak',
        method: 'POST',
        headers: {
          'Authorization': 'Token ' + DG_KEY,
          'Content-Type': 'application/json'
        }
      }, resp => {
        const chunks = [];
        resp.on('data', c => chunks.push(c));
        resp.on('end', () => resolve(Buffer.concat(chunks)));
      });
      r.on('error', reject);
      r.write(JSON.stringify({text}));
      r.end();
    });

    res.setHeader('Content-Type', 'audio/mpeg');
    res.setHeader('Cache-Control', 'no-cache');
    res.send(audio);
  } catch(e) {
    res.status(500).json({error: e.message});
  }
};
