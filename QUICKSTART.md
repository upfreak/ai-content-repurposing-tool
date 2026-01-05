# Quick Start Guide

## 5-Minute Setup

### Prerequisites Check
- [ ] Python 3.9+ installed (`python --version`)
- [ ] Node.js 16+ installed (`node --version`)
- [ ] PostgreSQL 12+ installed and running
- [ ] Git installed

### Step 1: Clone/Prepare Project (1 min)

```bash
# Navigate to project directory
cd "c:\mysaasapps\AI Content Repurposing Tool"
```

### Step 2: Database Setup (1 min)

```bash
# Create database
createdb content_repurpose

# Verify connection
psql -U postgres -d content_repurpose -c "SELECT 1"
```

### Step 3: Backend Setup (2 min)

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file (copy from .env.example)
copy .env.example .env

# Edit .env if needed (should work with defaults)
```

### Step 4: Frontend Setup (1 min)

```bash
# Open new terminal in project root
cd frontend

# Install dependencies
npm install

# Create .env.local (optional, has good defaults)
copy .env.example .env.local
```

### Step 5: Run Both Servers

**Terminal 1 - Backend:**
```bash
cd backend
venv\Scripts\activate  # If not already activated
uvicorn main:app --reload
```

Expected output:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
Press CTRL+C to quit
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

Expected output:
```
VITE v5.0.7 ready in XXX ms
➜  Local:   http://localhost:3000/
```

### Step 6: Test It Out (Included in 5 min)

1. Open http://localhost:3000
2. Click "Create one" to register
3. Fill in email, username, password
4. Click "New Project"
5. Paste some content and select platforms
6. Click "Generate Content"
7. Watch the AI magic happen! ✨

## Common Issues & Fixes

### Backend Won't Start

**Error: "ModuleNotFoundError: No module named 'fastapi'"**
```bash
# Make sure virtual environment is activated
venv\Scripts\activate

# Reinstall dependencies
pip install -r requirements.txt
```

**Error: "Connection refused" (Database)**
```bash
# Check PostgreSQL is running
# Windows: Check Services app or run
pg_ctl -D "C:\Program Files\PostgreSQL\15\data" start

# Create database
createdb content_repurpose
```

### Frontend Won't Start

**Error: "npm: command not found"**
```bash
# Install Node.js from https://nodejs.org/
# Restart terminal after installation
```

**Error: "EACCES: permission denied"**
```bash
# Clear npm cache
npm cache clean --force

# Reinstall
npm install
```

### Port Already in Use

```bash
# Backend port 8000
# Windows: Find and kill process
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Frontend port 3000
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

### API Connection Error

**"Failed to login" or network errors**
- Check backend is running (Terminal 1)
- Verify http://localhost:8000/docs loads
- Check ALLOWED_ORIGINS in backend .env
- Clear browser cache (Ctrl+Shift+Del)

## Features Overview

### After Login:

1. **Dashboard** - Overview of your projects and statistics
2. **New Project** - Create new content repurposing jobs
3. **Content Library** - View and manage all uploaded content
4. **Settings** - Create custom brand voices

### Generation Platforms:

- **Twitter/X** - Tweet threads (5-8 tweets)
- **LinkedIn** - Professional posts
- **Instagram** - Captions with hashtags
- **Facebook** - Engaging posts
- **TikTok** - Video scripts
- **Email** - Newsletter templates
- **Summary** - TL;DR and executive summaries

## Next Steps

1. **Explore the API**: Visit http://localhost:8000/docs
2. **Read the docs**: Check README.md for detailed info
3. **Try different tones**: Professional, Casual, Educational, etc.
4. **Create brand voices**: In Settings, save your custom voice
5. **Test file uploads**: Upload .txt, .md, .pdf, or .docx files

## Deployment

Ready to go live? Check DEPLOYMENT.md for:
- Heroku deployment
- AWS ECS deployment
- DigitalOcean deployment
- Vercel/Netlify frontend deployment

## Support

- **Backend Errors**: Check terminal 1 output
- **Frontend Errors**: Open browser DevTools (F12)
- **API Issues**: Visit http://localhost:8000/docs
- **Database Issues**: Check PostgreSQL logs

## Tips & Tricks

1. **Better Content Generation**:
   - Use longer, more detailed source content
   - Try different tones for variety
   - Create multiple brand voices for different audiences

2. **Copy Generated Content**:
   - Click the copy button on each generated piece
   - Content is automatically formatted for each platform

3. **Regenerate Content**:
   - Want a different version? Click "Regenerate"
   - Change the tone for different results
   - Save your favorites to brand voices

4. **Keyboard Shortcuts**:
   - Tab through form fields
   - Enter to submit forms
   - Ctrl+C in terminal to stop servers

## Database Reset (Development Only)

If you need to reset everything:

```bash
# Drop database
dropdb content_repurpose

# Recreate it
createdb content_repurpose

# Backend will auto-create tables on first run
```

## Check Backend Health

```bash
# In browser or terminal
curl http://localhost:8000/health

# Expected response:
# {"status":"healthy","service":"AI Content Repurposing Tool","version":"1.0.0"}
```

## View API Documentation

- **Interactive Swagger UI**: http://localhost:8000/docs
- **Alternative ReDoc**: http://localhost:8000/redoc
- **Full API Docs**: Check API_DOCS.md file

---

## Production Checklist

When ready to deploy:

- [ ] Change SECRET_KEY in .env to a random value
- [ ] Set DEBUG=False in backend .env
- [ ] Configure proper database (RDS, Heroku Postgres, etc.)
- [ ] Set ALLOWED_ORIGINS to your domain
- [ ] Set GROQ_API_KEY (production key)
- [ ] Enable HTTPS
- [ ] Set up monitoring and logging
- [ ] Configure backups

See DEPLOYMENT.md for detailed steps.

---

Enjoy using AI Content Repurposing Tool! 🚀
