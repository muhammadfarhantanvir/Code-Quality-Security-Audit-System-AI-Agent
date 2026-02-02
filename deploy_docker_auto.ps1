# PowerShell script for Docker deployment of Code Quality & Security Audit System

Write-Host "🚀 Starting automated Docker deployment..." -ForegroundColor Green

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

# Check prerequisites
Write-Status "Checking prerequisites..."

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

Write-Status "Prerequisites check passed!"

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
    Write-Status "✅ Services are running successfully!"
    Write-Host ""
    Write-Status "Application is available at: http://localhost:8501"
    if ($deploymentType -eq "production") {
        Write-Status "Nginx is available at: http://localhost"
    }
    Write-Host ""
    Write-Status "To view logs: $composeCmd -f $composeFile logs -f"
    Write-Status "To stop services: $composeCmd -f $composeFile down"
} else {
    Write-ErrorMsg "❌ Services failed to start properly."
    Write-Status "Check logs with: $composeCmd -f $composeFile logs"
    exit 1
}

Write-Status "🎉 Docker deployment completed successfully!"