# Git Workflow Guide

## ✅ Initial Setup Complete!

Your repository is initialized with:
- **92 files** committed
- **7,144 lines** of code
- **Initial commit**: `f53857d`

## 🔧 Configure Git Identity (Optional)

```bash
# Set your name and email
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Or just for this project
git config user.name "Your Name"
git config user.email "your.email@example.com"
```

## 📝 Daily Git Workflow

### Making Changes

```bash
# 1. Check what changed
git status

# 2. See the actual changes
git diff

# 3. Add files to staging
git add .                    # Add all changes
git add backend/apps/        # Add specific directory
git add file.py              # Add specific file

# 4. Commit with message
git commit -m "Add feature X"

# 5. View commit history
git log --oneline
git log --graph --oneline --all
```

### Commit Message Best Practices

```bash
# Good commit messages:
git commit -m "Add Jira webhook receiver"
git commit -m "Fix: Handle null values in sync task"
git commit -m "Refactor: Extract Jira client to separate class"
git commit -m "Docs: Update API reference with new endpoints"

# Use prefixes:
# feat: New feature
# fix: Bug fix
# refactor: Code refactoring
# docs: Documentation
# test: Tests
# chore: Maintenance
```

### Branching Strategy

```bash
# Create a new feature branch
git checkout -b feature/servicenow-integration

# Work on your feature, commit changes
git add .
git commit -m "feat: Add ServiceNow plugin"

# Switch back to main
git checkout main

# Merge feature branch
git merge feature/servicenow-integration

# Delete feature branch
git branch -d feature/servicenow-integration
```

## 🚀 Recommended Workflow for This Project

### Week-by-Week Development

```bash
# Week 1: Jira Enhancement
git checkout -b feature/jira-bidirectional-sync
# ... make changes ...
git commit -m "feat: Add bidirectional Jira sync"
git checkout main
git merge feature/jira-bidirectional-sync

# Week 2: Frontend
git checkout -b feature/frontend-ui
# ... make changes ...
git commit -m "feat: Add change request list view"
git checkout main
git merge feature/frontend-ui
```

### Daily Commits

```bash
# End of each coding session
git add .
git commit -m "WIP: Working on Jira webhook receiver"

# Or for completed features
git commit -m "feat: Complete Jira webhook receiver with tests"
```

## 📊 Useful Git Commands

### View History

```bash
# Simple log
git log --oneline

# Detailed log with graph
git log --graph --oneline --all --decorate

# See changes in last commit
git show

# See changes in specific commit
git show f53857d
```

### Undo Changes

```bash
# Discard changes in working directory
git checkout -- file.py

# Unstage file (keep changes)
git reset HEAD file.py

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Undo last commit (discard changes) - CAREFUL!
git reset --hard HEAD~1
```

### Stashing (Save work temporarily)

```bash
# Save current changes
git stash

# List stashes
git stash list

# Apply last stash
git stash pop

# Apply specific stash
git stash apply stash@{0}
```

## 🌐 Adding Remote Repository (Later)

When you're ready to add GitHub/GitLab:

```bash
# Add remote
git remote add origin https://github.com/yourusername/appsec-dashboard.git

# Push to remote
git push -u origin main

# Pull from remote
git pull origin main
```

## 📋 .gitignore Already Configured

Your `.gitignore` files already exclude:
- ✅ Virtual environments (`venv/`)
- ✅ Environment files (`.env`)
- ✅ Python cache (`__pycache__/`)
- ✅ Node modules (`node_modules/`)
- ✅ Build artifacts (`dist/`, `build/`)
- ✅ IDE files (`.vscode/`, `.idea/`)
- ✅ Logs (`*.log`)

## 🎯 Suggested Commit Points

### After Each Feature
```bash
git commit -m "feat: Add ServiceNow integration"
```

### After Bug Fixes
```bash
git commit -m "fix: Handle timeout in Jira sync"
```

### After Tests
```bash
git commit -m "test: Add unit tests for Jira plugin"
```

### End of Day
```bash
git commit -m "WIP: Progress on frontend dashboard"
```

## 💡 Pro Tips

1. **Commit Often**: Small, frequent commits are better than large ones
2. **Meaningful Messages**: Future you will thank you
3. **Branch for Features**: Keep main branch stable
4. **Review Before Commit**: Use `git diff` to review changes
5. **Don't Commit Secrets**: Never commit `.env` files or API keys

## 🔍 Current Repository Status

```bash
# Check current status
git status

# View commit history
git log --oneline

# See what branch you're on
git branch
```

## 📚 Quick Reference

```bash
# Status & Info
git status              # See what changed
git log --oneline       # View history
git branch             # List branches

# Making Changes
git add .              # Stage all changes
git commit -m "msg"    # Commit changes
git push               # Push to remote (when set up)

# Branching
git checkout -b name   # Create & switch to branch
git checkout main      # Switch to main
git merge branch-name  # Merge branch

# Undo
git checkout -- file   # Discard changes
git reset HEAD file    # Unstage file
git stash             # Save work temporarily
```

## 🎉 You're All Set!

Your project is now under version control. Every change you make can be:
- ✅ Tracked
- ✅ Reverted if needed
- ✅ Branched for experiments
- ✅ Shared with team (when you add remote)

**Next Steps:**
1. Make changes to your code
2. Commit regularly
3. When ready, add GitHub remote
4. Push to share with team

---

**Current Commit**: `f53857d` - Initial commit with full MVP
**Branch**: `main`
**Files Tracked**: 92 files, 7,144 lines of code
