Overview
The system is designed to support businesses that want to automate customer support while maintaining a natural, human-like communication style. It offers:

Real-time response generation with Claude
Secure input cleaning and validation
Configurable tone and industry
Persistent logging for analytics and training
User feedback capture
A ready-to-use REST API


Features

AI-generated customer support replies using Claude (Sonnet model)
Demo mode when the Anthropic API key is not available
Input sanitization and basic security filtering
Customizable tone, industry, and signature settings
JSONL logging system for training and historical analysis
Feedback endpoint for storing edited AI responses
Analytics endpoint summarizing accuracy and usage metrics


Requirements

Python 3.9 or newer
Flask
flask-cors
anthropic Python SDK
Standard Python libraries (os, json, datetime, re)
