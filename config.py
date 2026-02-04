# AI Customer Support Assistant - Configuration

# API Configuration
# Replace with your actual API key when ready to use real AI
ANTHROPIC_API_KEY = "your-api-key-here"  # Get from: https://console.anthropic.com/

# Model Settings
AI_MODEL = "claude-sonnet-4-5-20250929"
MAX_TOKENS = 1000

# Safety Limits
MAX_INPUT_LENGTH = 2000
MAX_OUTPUT_LENGTH = 1000
RATE_LIMIT_PER_HOUR = 100  # Prevent cost spikes

# Business Defaults
DEFAULT_BUSINESS_NAME = "Support Team"
DEFAULT_TONE = "professional"
DEFAULT_INDUSTRY = "general business"

# Logging
ENABLE_LOGGING = True
LOG_DIRECTORY = "logs"

# Feature Flags
ENABLE_SIGNATURE = True
ENABLE_EDIT_TRACKING = True
ENABLE_ANALYTICS = True