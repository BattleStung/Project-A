Write-Host "🚀 AI Customer Support Assistant Launcher" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Set API key
$env:ANTHROPIC_API_KEY = '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'

# Activate virtual environment
Write-Host "🔧 Activating virtual environment..." -ForegroundColor Yellow
.\.venv\Scripts\Activate.ps1

# Check if API key is set
if ($env:ANTHROPIC_API_KEY) {
    Write-Host "✅ API key detected - using production mode" -ForegroundColor Green
    Write-Host ""
    Write-Host "🎯 Starting production server..." -ForegroundColor Cyan
    python app_production.py
} else {
    Write-Host "⚠️  Running in DEMO MODE (no API key detected)" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "🎯 Starting demo server..." -ForegroundColor Cyan
    python app.py
}