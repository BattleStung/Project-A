AI Customer Support Assistant (Flask + Claude API)
This project is a production‑ready backend service for generating automated customer‑support replies using Anthropic Claude (or a built‑in demo fallback). It includes message cleaning, safety filtering, logging, analytics, and a frontend ready to plug into your UI.

Features
AI‑generated customer support replies using Claude (Sonnet)
Demo mode when API key is not available
Input sanitization & basic security filtering
Configurable tone, industry, and signature
Logging system (.jsonl) for training & analysis
User feedback loop (logs edited responses)
Analytics endpoint to measure accuracy and usage

Requirements
Python 3.9+
Flask
flask-cors
anthropic
openai-safe regexes, standard libs
