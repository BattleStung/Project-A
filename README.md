# AI Customer Support Automation API

## Overview

This system enables businesses to automate customer support while maintaining natural, human-like communication.

It generates real-time AI responses using Claude, performs secure input validation, supports configurable tone and industry settings, logs interactions for analytics, and captures user feedback. The system is exposed through a REST API for easy integration.

## Features

- AI-generated customer support replies using the Claude Sonnet model
- Automatic demo mode when the Anthropic API key is not configured
- Input sanitization and basic security filtering
- Customizable tone, industry, and signature settings
- JSONL logging for analytics and model improvement
- Feedback endpoint for storing edited AI responses
- Analytics endpoint summarizing usage and accuracy metrics
- REST API ready for integration

## Requirements

- Python 3.9 or newer
- Flask
- flask-cors
- anthropic (Python SDK)

### Standard Python Libraries

- os
- json
- datetime
- re
