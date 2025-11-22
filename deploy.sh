#!/bin/bash

# Tourism Guide - Quick Deployment Script
# This script helps you deploy to GitHub quickly

echo "🚀 Tourism Guide - Quick Deploy to GitHub"
echo "=========================================="
echo ""

# Check if git is initialized
if [ ! -d .git ]; then
    echo "📦 Initializing Git repository..."
    git init
    git branch -M main
fi

# Check if remote exists
if ! git remote | grep -q origin; then
    echo ""
    echo "🔗 Enter your GitHub repository URL:"
    echo "   (e.g., https://github.com/username/tourism-guide.git)"
    read -p "URL: " repo_url
    
    if [ -z "$repo_url" ]; then
        echo "❌ No URL provided. Exiting."
        exit 1
    fi
    
    git remote add origin "$repo_url"
    echo "✅ Remote added: $repo_url"
fi

# Add all files
echo ""
echo "📝 Adding files to git..."
git add .

# Commit
echo ""
read -p "Commit message (or press Enter for default): " commit_msg
if [ -z "$commit_msg" ]; then
    commit_msg="Ready for deployment"
fi

git commit -m "$commit_msg"

# Push
echo ""
echo "📤 Pushing to GitHub..."
git push -u origin main

echo ""
echo "✅ Successfully pushed to GitHub!"
echo ""
echo "📋 Next Steps:"
echo "   1. Go to https://render.com"
echo "   2. Sign in with GitHub"
echo "   3. New Web Service → Select your repository"
echo "   4. Follow DEPLOYMENT_GUIDE.md for configuration"
echo ""
echo "🎉 Your code is ready to deploy!"
