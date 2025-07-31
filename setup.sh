#!/bin/bash

# Setup script for ISTE App deployment

echo "Setting up ISTE App for deployment..."

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Install Playwright browsers
echo "Installing Playwright browsers..."
playwright install

# Set environment variables for production
export FLASK_ENV=production
export FLASK_DEBUG=0

echo "Setup completed successfully!"
echo "To run the application: gunicorn app:app" 