# PowerShell script for comprehensive deployment of Code Quality & Security Audit System
# Deploys to both Docker and Vercel

Write-Host "🚀 Starting comprehensive deployment for Code Quality & Security Audit System..." -ForegroundColor Green

# Function to write colored output
function Write-Status {
    param([string]$Message)
    Write-Host "[INFO] $Message" -ForegroundColor Green
}

function Write-WarningMsg {
    param([string]$Message)
    Write-Host "[WARNING] $Message" -ForegroundColor Yellow
}

function Write-ErrorMsg {
    param([string]$Message)
    Write-Host "[ERROR] $Message" -ForegroundColor Red
}

function Write-Header {
    param([string]$Message)
    Write-Host "[HEADER] $Message" -ForegroundColor Blue
}

# Check prerequisites for Docker
Write-Header "Checking Docker prerequisites..."

# Check if Docker is installed and running
try {
    $dockerVersion = docker --version 2>$null
    if (-not $dockerVersion) {
        Write-ErrorMsg "Docker is not installed. Please install Docker Desktop first."
        exit 1
    }
    Write-Status "Docker is installed: $dockerVersion"
} catch {
    Write-ErrorMsg "Docker is not accessible. Please ensure Docker Desktop is running."
    exit 1
}

# Check if docker-compose is available
$composeCmd = "docker-compose"
$composeAvailable = $false

try {
    $composeVersion = docker-compose --version 2>$null
    if ($composeVersion) {
        $composeAvailable = $true
        Write-Status "Docker Compose is available: $composeVersion"
    }
} catch {
    # Try 'docker compose' (newer Docker versions)
    try {
        $composeVersion = docker compose version 2>$null
        if ($composeVersion) {
            $composeCmd = "docker compose"
            $composeAvailable = $true
            Write-Status "Docker Compose is available: $composeVersion"
        }
    } catch {
        Write-ErrorMsg "Neither 'docker-compose' nor 'docker compose' is available."
        exit 1
    }
}

Write-Status "Docker prerequisites check passed!"

# Check prerequisites for Vercel
Write-Header "Checking Vercel prerequisites..."

# Check if Vercel CLI is installed
if (!(Get-Command vercel -ErrorAction SilentlyContinue)) {
    Write-ErrorMsg "Vercel CLI is not installed. Please install with: npm install -g vercel"
    exit 1
}

Write-Status "Vercel CLI is available."

# Check if user is logged in to Vercel
try {
    $vercelUser = vercel whoami 2>$null
    if (-not $vercelUser) {
        Write-WarningMsg "Not logged in to Vercel. Initiating login..."
        vercel login
    } else {
        Write-Status "Already logged in to Vercel as: $vercelUser"
    }
} catch {
    Write-WarningMsg "Not logged in to Vercel. Initiating login..."
    vercel login
}

# Verify vercel.json exists
if (-not (Test-Path "vercel.json")) {
    Write-WarningMsg "vercel.json not found. Creating default configuration..."
    $vercelConfig = @{
        version = 2
        builds = @(
            @{
                src = "app.py"
                use = "@vercel/python"
                config = @{ runtime = "python3.11" }
            }
        )
        routes = @(
            @{
                src = "/(.*)"
                dest = "app.py"
            }
        )
        env = @{
            STREAMLIT_SERVER_PORT = "3000"
            STREAMLIT_SERVER_ADDRESS = "0.0.0.0"
            PYTHONPATH = "."
        }
    } | ConvertTo-Json -Depth 10
    
    Set-Content -Path "vercel.json" -Value $vercelConfig
    Write-Status "Created default vercel.json configuration."
}

# Determine deployment type and compose file
$deploymentType = "development"
$composeFile = "docker-compose.yml"

if (Test-Path "Dockerfile.prod") {
    $deploymentType = "production"
    $composeFile = "docker-compose.prod.yml"
    Write-Status "Using production configuration"
} else {
    Write-Status "Using development configuration"
}

# Build the Docker image
Write-Status "Building Docker image for $deploymentType deployment..."
& $composeCmd -f $composeFile build

# Start the services
Write-Status "Starting $deploymentType services..."
& $composeCmd -f $composeFile up -d

# Wait for services to be ready
Write-Status "Waiting for services to start..."
Start-Sleep -Seconds 15

# Check if the main service is running
$psOutput = & $composeCmd -f $composeFile ps
if ($psOutput -match "Up") {
    Write-Status "✅ Docker services are running successfully!"
    Write-Host ""
    Write-Status "Docker Application is available at: http://localhost:8501"
    if ($deploymentType -eq "production") {
        Write-Status "Nginx is available at: http://localhost"
    }
    Write-Host ""
    Write-Status "To view Docker logs: $composeCmd -f $composeFile logs -f"
    Write-Status "To stop Docker services: $composeCmd -f $composeFile down"
} else {
    Write-ErrorMsg "❌ Docker services failed to start properly."
    Write-Status "Check Docker logs with: $composeCmd -f $composeFile logs"
    exit 1
}

Write-Status "🎉 Docker deployment completed successfully!"
Write-Host ""

# Deploy to Vercel
Write-Status "Deploying to Vercel..."
vercel --prod

Write-Status "🎉 Vercel deployment completed successfully!"
Write-Status "Your application is now live on Vercel!"
Write-Host ""

Write-Header "🎉 Comprehensive deployment completed successfully!"
Write-Status "Docker: http://localhost:8501"
Write-Status "Vercel: Check your Vercel dashboard for the deployment URL"