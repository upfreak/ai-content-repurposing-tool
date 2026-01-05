# Deployment Guide

## Pre-Deployment Checklist

- [ ] All tests passing
- [ ] Environment variables configured
- [ ] Database migrations complete
- [ ] API documentation reviewed
- [ ] Frontend build tested
- [ ] Security audit completed
- [ ] Rate limiting enabled
- [ ] Error logging configured
- [ ] Monitoring set up

## Backend Deployment

### Option 1: Heroku Deployment

1. **Install Heroku CLI**
```bash
# Windows
choco install heroku-cli

# macOS
brew tap heroku/brew && brew install heroku
```

2. **Create Procfile**
```
web: gunicorn main:app --worker-class uvicorn.workers.UvicornWorker --workers 4
```

3. **Create runtime.txt**
```
python-3.11.7
```

4. **Deploy**
```bash
heroku login
heroku create your-app-name
heroku addons:create heroku-postgresql:standard-0
heroku config:set SECRET_KEY=your-secret-key
heroku config:set GROQ_API_KEY=your-groq-key
git push heroku main
```

### Option 2: AWS Elastic Beanstalk

1. **Install EB CLI**
```bash
pip install awsebcli
```

2. **Initialize**
```bash
eb init -p python-3.11 content-repurposing
```

3. **Create environment**
```bash
eb create production
```

4. **Deploy**
```bash
eb deploy
eb setenv SECRET_KEY=your-secret-key GROQ_API_KEY=your-groq-key
```

### Option 3: Docker & AWS ECS

1. **Create Dockerfile**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

2. **Build and push to ECR**
```bash
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com

docker build -t content-repurposing .

docker tag content-repurposing:latest $AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/content-repurposing:latest

docker push $AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/content-repurposing:latest
```

3. **Deploy with ECS**
- Create ECS task definition
- Create ECS service
- Configure load balancer

### Option 4: DigitalOcean App Platform

1. **Connect GitHub repository**
2. **Create app.yaml**
```yaml
name: content-repurposing
services:
- name: backend
  github:
    repo: your-repo
    branch: main
  build_command: pip install -r requirements.txt
  run_command: uvicorn main:app --host 0.0.0.0 --port 8080
  envs:
  - key: DATABASE_URL
    scope: RUN_AND_BUILD_TIME
    value: ${db.connection_string}
  - key: SECRET_KEY
    scope: RUN_TIME
    value: ${SECRET_KEY}
databases:
- name: db
  engine: PG
  version: "13"
```

3. **Deploy**
```bash
doctl apps create --spec app.yaml
```

## Frontend Deployment

### Option 1: Vercel (Recommended)

1. **Install Vercel CLI**
```bash
npm i -g vercel
```

2. **Deploy**
```bash
cd frontend
vercel --prod
```

3. **Configure environment variables**
```bash
vercel env add VITE_API_URL
# Enter your backend API URL
```

### Option 2: Netlify

1. **Install Netlify CLI**
```bash
npm install -g netlify-cli
```

2. **Create netlify.toml**
```toml
[build]
  command = "npm run build"
  publish = "dist"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200

[env]
  VITE_API_URL = "https://your-api-domain.com/api"
```

3. **Deploy**
```bash
cd frontend
netlify deploy --prod
```

### Option 3: AWS S3 + CloudFront

1. **Build frontend**
```bash
npm run build
```

2. **Create S3 bucket**
```bash
aws s3 mb s3://content-repurposing-frontend
aws s3 sync dist/ s3://content-repurposing-frontend --delete
```

3. **Create CloudFront distribution**
- Origin: S3 bucket
- Default root object: index.html
- Error pages: Route to index.html

4. **Configure domain**
- Add CNAME to CloudFront distribution

## Database Migrations (Production)

### Using Alembic (Optional)

1. **Install Alembic**
```bash
pip install alembic
```

2. **Initialize**
```bash
alembic init alembic
```

3. **Create migration**
```bash
alembic revision --autogenerate -m "Initial schema"
```

4. **Run migration**
```bash
alembic upgrade head
```

## SSL/TLS Configuration

### Using Let's Encrypt (Free)

1. **Install Certbot**
```bash
pip install certbot certbot-nginx
```

2. **Generate certificate**
```bash
certbot certonly --standalone -d yourdomain.com -d www.yourdomain.com
```

3. **Configure in your web server** (Nginx example)
```nginx
server {
    listen 443 ssl http2;
    server_name yourdomain.com;
    
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    
    location / {
        proxy_pass http://localhost:8000;
    }
}
```

## Monitoring & Logging

### Application Monitoring

```python
# Add to main.py
from pythonjsonlogger import jsonlogger
import logging

# Setup JSON logging
logHandler = logging.FileHandler('app.log')
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)

logging.getLogger().addHandler(logHandler)
```

### Error Tracking (Optional)

```python
# Using Sentry
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration

sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[FastApiIntegration()],
    traces_sample_rate=1.0
)
```

### Performance Monitoring

```python
# Add NewRelic or DataDog
# Check official documentation for setup
```

## Scaling Strategies

### Horizontal Scaling

1. **Load Balancing**
   - Nginx (recommended for development)
   - AWS ALB (production)
   - HAProxy

2. **Database Replication**
   - Primary-replica setup
   - Read replicas for reporting

3. **Caching Layer**
   - Redis for session and API response caching
   - CloudFront CDN for static assets

### Vertical Scaling

1. Increase server resources (CPU, RAM)
2. Optimize database queries
3. Implement connection pooling

## Backup & Recovery

### Database Backups

```bash
# PostgreSQL backup
pg_dump content_repurpose > backup.sql

# Restore
psql content_repurpose < backup.sql

# AWS RDS automated backups
# Enabled by default, retention: 7 days
```

### Application Files Backup

```bash
# Backup uploads directory
tar -czf uploads_backup.tar.gz uploads/

# Backup application code
git push origin main  # Version control is best backup
```

## Post-Deployment

1. **Test endpoints**
```bash
curl https://your-api-domain.com/health
```

2. **Verify environment variables**
3. **Monitor application logs**
4. **Check database connectivity**
5. **Test user registration/login flow**
6. **Verify Groq API integration**
7. **Test file uploads**
8. **Check CORS configuration**

## Troubleshooting Deployment

### Port Issues
```bash
# Check if port is in use
netstat -an | grep :8000
# Change port in deployment config
```

### Database Connection
```bash
# Check PostgreSQL is accessible
psql -h prod-db.example.com -U username -d dbname
```

### Memory Issues
```bash
# Increase worker count carefully
# For 4GB RAM: 2-3 workers
# gunicorn main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker
```

### CORS Errors
- Verify ALLOWED_ORIGINS includes frontend domain
- Check that credentials are being sent
- Verify SSL certificates if using HTTPS

## Rollback Procedures

1. **Revert to previous Git commit**
```bash
git revert <commit-hash>
git push origin main
```

2. **Restore database from backup**
```bash
psql content_repurpose < backup.sql
```

3. **Redeploy application**
```bash
# Heroku
git push heroku main

# DigitalOcean
doctl apps update <app-id> --spec app.yaml
```
