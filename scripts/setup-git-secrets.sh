#!/bin/bash

# Install git-secrets if not already installed
if ! command -v git-secrets &> /dev/null; then
    echo "Installing git-secrets..."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        brew install git-secrets
    elif [[ -f /etc/redhat-release ]]; then
        # RHEL/CentOS
        sudo yum install -y git-secrets
    elif [[ -f /etc/debian_version ]]; then
        # Debian/Ubuntu
        sudo apt-get update
        sudo apt-get install -y git-secrets
    else
        echo "Unsupported OS. Please install git-secrets manually."
        exit 1
    fi
fi

# Initialize git-secrets
echo "Initializing git-secrets..."
git secrets --install --force

# Clear any existing patterns
git config --remove-section secrets.patterns 2>/dev/null || true

# Disable AWS patterns to avoid conflicts
git config --remove-section secrets.providers 2>/dev/null || true

# Add simple patterns one by one
echo "Adding common sensitive patterns..."

# AWS Access Key ID (simplified pattern)
git secrets --add --literal 'AKIA'

# Common secret patterns
git secrets --add --literal 'AWS_ACCESS_KEY='
git secrets --add --literal 'AWS_SECRET_KEY='
git secrets --add --literal 'SECRET_KEY='

# More specific patterns for common secrets
git secrets --add 'SECRET_KEY=[0-9a-zA-Z]+'  # Matches SECRET_KEY= followed by alphanumeric chars
git secrets --add 'PASSWORD=[0-9a-zA-Z]+'  # Matches PASSWORD= followed by alphanumeric chars

# Common API keys and tokens (simplified patterns)
git secrets --add --literal 'xoxb-'  # Slack tokens
git secrets --add --literal 'ghp_'   # GitHub tokens

# Private key patterns (as literals)
git secrets --add --literal 'BEGIN RSA PRIVATE KEY'
git secrets --add --literal 'BEGIN DSA PRIVATE KEY'
git secrets --add --literal 'BEGIN EC PRIVATE KEY'
git secrets --add --literal 'BEGIN OPENSSH PRIVATE KEY'

# Add allowed patterns (false positives)
echo "Configuring allowed patterns..."
git secrets --add -a 'password=*'  # Allow 'password=' in general
git secrets --add -a 'example.com'  # Allow example domains

echo "Git-secrets setup complete!"
echo "To test the setup, run: git secrets --scan"
