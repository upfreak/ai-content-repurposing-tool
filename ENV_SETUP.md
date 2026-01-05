# Environment Variables Configuration

## Backend (.env)

Copy this template to `backend/.env` and fill in your values:

```bash
# Database Configuration
DATABASE_URL=postgresql://postgres:password@localhost:5432/content_repurpose

# JWT Secret Key (MUST be at least 32 characters)
# Generate with: python -c "import secrets; print(secrets.token_urlsafe(32))"
SECRET_KEY=change-this-to-a-secure-random-key-with-32-chars-min

# Groq API Key (Get from https://console.groq.com)
GROQ_API_KEY=YOUR_GROQ_API_KEY_HERE

# Groq Model (recommended: llama-3.3-70b-versatile)
GROQ_MODEL=llama-3.3-70b-versatile

# CORS Configuration (Frontend URL)
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001,http://127.0.0.1:3000

# File Upload Configuration
UPLOAD_DIR=uploads
MAX_UPLOAD_SIZE=52428800

# Debug Mode
DEBUG=True

# Authentication Token Expiration
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

## Frontend (.env.local)

Copy this template to `frontend/.env.local`:

```bash
# API Configuration
VITE_API_URL=http://localhost:8000/api

# Optional: Analytics
# VITE_GA_ID=your-google-analytics-id
```

## Database Setup

### PostgreSQL Installation

**Windows:**
```bash
# Using chocolatey
choco install postgresql

# Or download from: https://www.postgresql.org/download/windows/
```

**macOS:**
```bash
# Using Homebrew
brew install postgresql
brew services start postgresql
```

**Linux (Ubuntu):**
```bash
sudo apt-get install postgresql postgresql-contrib
sudo systemctl start postgresql
```

### Create Database and User

```bash
# Connect to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE content_repurpose;

# Create user (optional, use 'postgres' by default)
CREATE USER repurpose_user WITH PASSWORD 'secure_password';

# Grant privileges
GRANT ALL PRIVILEGES ON DATABASE content_repurpose TO repurpose_user;

# Exit
\q
```

### Verify Connection

```bash
# Test connection
psql -U repurpose_user -d content_repurpose -h localhost
```

## Generate Secure Secret Key

```bash
# Python method
python -c "import secrets; print(secrets.token_urlsafe(32))"

# PowerShell method
[System.Convert]::ToBase64String((1..32 | ForEach-Object {Get-Random -Maximum 256})) | Select-Object -First 43
```

## Groq API Setup

1. Visit https://console.groq.com
2. Sign up for a free account
3. Create an API key
4. Copy the key to `GROQ_API_KEY` in `.env`

## Development vs Production

### Development (.env)
```
DEBUG=True
DATABASE_URL=postgresql://postgres:password@localhost:5432/content_repurpose
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001
```

### Production (.env)
```
DEBUG=False
DATABASE_URL=postgresql://prod_user:prod_pass@prod_host:5432/content_repurpose_prod
ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
SECRET_KEY=<very-secure-random-key>
GROQ_API_KEY=<your-groq-key>
```

## Security Best Practices

1. **Never commit .env files** - They're in .gitignore
2. **Use environment-specific configurations**
3. **Rotate secrets regularly**
4. **Use strong, random SECRET_KEY** (minimum 32 characters)
5. **Enable HTTPS in production**
6. **Restrict ALLOWED_ORIGINS to your domain**
7. **Keep API keys secure and rotate regularly**

## Troubleshooting

### Database Connection Issues
```bash
# Check PostgreSQL is running
pg_isready -h localhost -p 5432

# Test with psql
psql -U postgres -h localhost -d content_repurpose

# Check DATABASE_URL format
# postgresql://username:password@host:port/database
```

### Groq API Issues
```bash
# Verify API key format
echo $GROQ_API_KEY

# Test API connection (from backend)
python -c "from groq import Groq; client = Groq(); print('API OK')"
```

### Port Already in Use
```bash
# Backend (8000)
lsof -i :8000
kill -9 <PID>

# Frontend (3000)
lsof -i :3000
kill -9 <PID>
```
