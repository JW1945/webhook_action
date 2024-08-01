#!/bin/bash

# Navigate to your project directory
cd /path/to/your/project

# Pull the latest changes
git pull origin main

# Install dependencies (if applicable)
npm install  # or pip install, etc.

# Build the project (if applicable)
npm run build

# Restart your application (adjust as needed)
pm2 restart your-app  # or systemctl restart your-service, etc.
