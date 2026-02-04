from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from datetime import datetime
import json
import os
import re

app = Flask(__name__)
CORS(app)

# Configuration
LOG_DIR = "logs"
API_KEY = os.environ.get('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')
os.makedirs(LOG_DIR, exist_ok=True)

class AIAssistant:
    """Core AI assistant with prompt engineering and safety controls"""
    
    def __init__(self):
        self.system_prompt = self._build_system_prompt()
        self.max_input_length = 2000
        self.max_output_length = 1000
    
    def _build_system_prompt(self, tone="professional", industry="general"):
        """The competitive advantage - your unique AI personality"""
        return f"""You are a skilled customer support assistant for {industry} business.

Core Principles:
- Tone: {tone}, friendly, and empathetic
- Goal: Solve the customer's problem quickly and effectively
- Style: Clear, concise, human (never robotic)
- Length: Keep responses short but complete (2-4 sentences ideal)

Rules:
1. Always acknowledge the customer's concern first
2. Provide a clear solution or next step
3. End with helpfulness, not just closing
4. Never use corporate jargon or templates
5. Sound like a real person who cares

If you cannot solve the issue, escalate politely and explain why.
Never make promises the business cannot keep."""

    def clean_input(self, message):
        """Sanitize and validate user input"""
        if not message:
            raise ValueError("Message cannot be empty")
        
        # Remove excessive whitespace
        cleaned = re.sub(r'\s+', ' ', message.strip())
        
        # Enforce length limits
        if len(cleaned) > self.max_input_length:
            cleaned = cleaned[:self.max_input_length] + "..."
        
        # Basic safety checks
        if self._contains_unsafe_content(cleaned):
            raise ValueError("Message contains inappropriate content")
        
        return cleaned
    
    def _contains_unsafe_content(self, text):
        """Simple content filter - expand based on your needs"""
        unsafe_patterns = [
            r'<script',
            r'javascript:',
            r'onerror=',
        ]
        return any(re.search(pattern, text, re.IGNORECASE) for pattern in unsafe_patterns)
    
    def generate_reply(self, customer_message, business_name="our team", settings=None):
        """Generate AI reply with full context"""
        settings = settings or {}
        
        # Clean input
        cleaned_message = self.clean_input(customer_message)
        
        # Build context
        tone = settings.get('tone', 'professional')
        industry = settings.get('industry', 'general business')
        add_signature = settings.get('add_signature', True)
        
        # Update system prompt based on settings
        system_prompt = self._build_system_prompt(tone, industry)
        
        # Simulate AI call (replace with actual API call)
        ai_response = self._call_ai_api(system_prompt, cleaned_message)
        
        # Format response
        formatted_response = self._format_response(
            ai_response, 
            business_name, 
            add_signature
        )
        
        return {
            'reply': formatted_response,
            'original_message': customer_message,
            'cleaned_message': cleaned_message,
            'settings_used': settings
        }
    
    def _call_ai_api(self, system_prompt, message):
        """
        AI API integration point
        Replace this with actual API call to Claude, GPT, etc.
        """

        return self._generate_demo_response(message)
    
    def _generate_demo_response(self, message):
        """Demo response generator - replace with real AI"""
        message_lower = message.lower()
        
        if 'refund' in message_lower or 'money back' in message_lower:
            return "I understand you're looking for a refund. I'd be happy to help you with that. Could you please provide your order number so I can process this right away?"
        
        elif 'shipping' in message_lower or 'delivery' in message_lower:
            return "Thanks for reaching out about your delivery. I've checked your order and it's currently on its way. You should receive it within 2-3 business days. I'll send you a tracking link right now."
        
        elif 'not working' in message_lower or 'broken' in message_lower or 'issue' in message_lower:
            return "I'm sorry to hear you're experiencing issues. Let's get this fixed for you right away. Can you tell me exactly what's happening when you try to use it? This will help me find the best solution."
        
        elif 'cancel' in message_lower:
            return "I can help you with that cancellation. Just to confirm, which subscription or order would you like to cancel? I'll process it immediately once you let me know."
        
        else:
            return "Thank you for contacting us! I'm here to help. Could you provide a bit more detail about what you need? That way, I can give you the most accurate assistance."
    
    def _format_response(self, ai_response, business_name, add_signature):
        """Polish the AI output"""
        # Ensure proper formatting
        formatted = ai_response.strip()
        
        # Add signature if requested
        if add_signature:
            formatted += f"\n\nBest regards,\n{business_name}"
        
        # Ensure it's not too long
        if len(formatted) > self.max_output_length:
            formatted = formatted[:self.max_output_length] + "..."
        
        return formatted

class Logger:
    """Logging system for continuous improvement"""
    
    @staticmethod
    def log_interaction(customer_message, ai_reply, settings, user_edit=None):
        """Save interaction for analysis and training"""
        timestamp = datetime.now().isoformat()
        
        log_entry = {
            'timestamp': timestamp,
            'customer_message': customer_message,
            'ai_reply': ai_reply,
            'settings': settings,
            'user_edit': user_edit,
            'edited': user_edit is not None
        }
        
        # Save to daily log file
        date_str = datetime.now().strftime('%Y-%m-%d')
        log_file = os.path.join(LOG_DIR, f'interactions_{date_str}.jsonl')
        
        with open(log_file, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
        
        return log_entry

# Initialize AI assistant
assistant = AIAssistant()

# API Routes

@app.route('/')
def index():
    """Serve the main UI"""
    return render_template('index.html')

@app.route('/api/generate-reply', methods=['POST'])
def generate_reply():
    """Main endpoint for generating customer support replies"""
    try:
        data = request.json
        
        # Extract parameters
        customer_message = data.get('message', '')
        business_name = data.get('business_name', 'Our Support Team')
        settings = {
            'tone': data.get('tone', 'professional'),
            'industry': data.get('industry', 'general business'),
            'add_signature': data.get('add_signature', True)
        }
        
        # Generate reply
        result = assistant.generate_reply(customer_message, business_name, settings)
        
        # Log the interaction
        Logger.log_interaction(
            customer_message=customer_message,
            ai_reply=result['reply'],
            settings=settings
        )
        
        return jsonify({
            'success': True,
            'reply': result['reply'],
            'metadata': {
                'cleaned_message': result['cleaned_message'],
                'settings_used': result['settings_used']
            }
        })
    
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'An unexpected error occurred'
        }), 500

@app.route('/api/feedback', methods=['POST'])
def submit_feedback():
    """Endpoint for user edits - critical for improvement loop"""
    try:
        data = request.json
        
        original_reply = data.get('original_reply', '')
        edited_reply = data.get('edited_reply', '')
        customer_message = data.get('customer_message', '')
        
        # Log the edit for training data
        Logger.log_interaction(
            customer_message=customer_message,
            ai_reply=original_reply,
            settings={},
            user_edit=edited_reply
        )
        
        return jsonify({
            'success': True,
            'message': 'Feedback recorded'
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Analytics endpoint - track usage and quality"""
    try:
        total_interactions = 0
        total_edited = 0
        
        # Read all log files
        for filename in os.listdir(LOG_DIR):
            if filename.startswith('interactions_') and filename.endswith('.jsonl'):
                filepath = os.path.join(LOG_DIR, filename)
                with open(filepath, 'r') as f:
                    for line in f:
                        entry = json.loads(line)
                        total_interactions += 1
                        if entry.get('edited'):
                            total_edited += 1
        
        accuracy_rate = 0
        if total_interactions > 0:
            accuracy_rate = ((total_interactions - total_edited) / total_interactions) * 100
        
        return jsonify({
            'success': True,
            'stats': {
                'total_interactions': total_interactions,
                'total_edited': total_edited,
                'accuracy_rate': round(accuracy_rate, 2)
            }
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    print("🚀 AI Customer Support Assistant Starting...")
    print("📍 Server running at http://localhost:5000")
    print("📊 Logs directory: ./logs")
    app.run(debug=True, host='0.0.0.0', port=5000)