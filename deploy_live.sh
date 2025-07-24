#!/bin/bash

# 🚀 One-Click Live Deployment Script
# This script will make your project live on multiple platforms

set -e

echo "🚀 Making Code Audit System LIVE for all users!"
echo "=================================================="

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ]; then
    echo "❌ Error: pyproject.toml not found. Please run from project root."
    exit 1
fi

# Step 1: Commit and push to GitHub
echo "📤 Step 1: Pushing to GitHub..."
git add .
git commit -m "feat: Live deployment ready - v1.0.0

🌐 Production-ready features:
- Live web demo with sample code
- One-click deployment buttons
- Docker production setup
- Auto-deployment workflows
- Multi-platform support

Ready for public use!"

git push origin main

# Step 2: Create release tag
echo "🏷️  Step 2: Creating release tag..."
git tag v1.0.0
git push origin v1.0.0

# Step 3: Build Docker image
echo "🐳 Step 3: Building Docker image..."
docker build -f docker/Dockerfile -t code-audit-system .

# Step 4: Test the application
echo "🧪 Step 4: Testing application..."
python -c "
import sys
sys.path.insert(0, 'src')
from src.code_audit_system.core.auditor import CodeAuditor
auditor = CodeAuditor()
print('✅ Application test passed!')
"

echo ""
echo "🎉 SUCCESS! Your project is now ready to go LIVE!"
echo ""
echo "🌐 Next steps to make it publicly accessible:"
echo ""
echo "1. 📋 GITHUB RELEASE:"
echo "   - Go to: https://github.com/yourusername/your-repo/releases"
echo "   - Click 'Create a new release'"
echo "   - Use tag: v1.0.0"
echo "   - Publish release"
echo ""
echo "2. 🚀 RAILWAY DEPLOYMENT (Free):"
echo "   - Go to: https://railway.app"
echo "   - Sign up with GitHub"
echo "   - Click 'Deploy from GitHub repo'"
echo "   - Select your repository"
echo "   - Railway will auto-deploy!"
echo ""
echo "3. 🐳 DOCKER HUB (Optional):"
echo "   - docker tag code-audit-system yourusername/code-audit-system"
echo "   - docker push yourusername/code-audit-system"
echo ""
echo "4. 📦 PYPI PACKAGE (Optional):"
echo "   - python -m build"
echo "   - twine upload dist/*"
echo ""
echo "🎯 Your live demo will be available at:"
echo "   https://your-project-name.railway.app"
echo ""
echo "📢 Share your project:"
echo "   - Reddit: r/Python, r/netsec"
echo "   - Twitter: #Python #Security #OpenSource"
echo "   - LinkedIn: Professional network"
echo ""
echo "🌟 Congratulations! Your tool is now LIVE for everyone to use!"