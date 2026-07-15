# Pizzeria & Bistro Movin Ground

Voice-enabled pizzeria website with Deepgram STT/TTS integration.

## Features
- 24 menu items (13 pizza, 4 fast food, 2 pasta, 5 salads)
- Real food photography
- Dark theme with orange accents
- Voice assistant (German)
  - Speech-to-Text via Deepgram
  - Text-to-Speech via Deepgram
  - Voice commands: search, prices, cart, categories
- Shopping cart with localStorage
- Responsive design
- TTS preview samples (German + English)

## Tech Stack
- Vanilla HTML/CSS/JS (no framework)
- Deepgram API (STT + TTS)
- Vercel (hosting + serverless functions)

## Deployment
```bash
vercel deploy
```

## API Endpoints
- `POST /api/transcribe` - Speech-to-Text (Deepgram nova-2, German)
- `POST /api/tts` - Text-to-Speech (Deepgram, German)

## Voice Commands (German)
- "Zeig mir die Pizzas" - Show pizza category
- "Was kostet die Margarita?" - Get price
- "Füge Pizza Salami hinzu" - Add to cart
- "Entferne Pommes" - Remove from cart
- "Hilfe" - List commands
