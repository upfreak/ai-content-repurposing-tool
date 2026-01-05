<p align="center">
  <img src="https://img.shields.io/badge/AI-Powered-blueviolet?style=for-the-badge" alt="AI Powered"/>
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI"/>
  <img src="https://img.shields.io/badge/React-61DAFB?style=for-the-badge&logo=react&logoColor=black" alt="React"/>
  <img src="https://img.shields.io/badge/PostgreSQL-336791?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL"/>
  <img src="https://img.shields.io/badge/Groq-FF6B6B?style=for-the-badge" alt="Groq"/>
</p>

<h1 align="center">🚀 AI Content Repurposing Tool</h1>

<p align="center">
  <strong>Transform your long-form content into engaging, platform-optimized social media posts with AI</strong>
</p>

<p align="center">
  A production-ready SaaS platform that leverages advanced AI to automatically convert blog posts, articles, and video transcripts into optimized content for Twitter, LinkedIn, Instagram, Facebook, TikTok, Email Newsletters, and Executive Summaries.
</p>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [Architecture](#-functional-architecture)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
- [Environment Variables](#-environment-variables)
- [API Reference](#-api-reference)
- [Database Schema](#-database-schema)
- [Platform-Specific Generation](#-platform-specific-generation)
- [Security](#-security)
- [Deployment](#-deployment)
- [Troubleshooting](#-troubleshooting)
- [Future Roadmap](#-future-roadmap)
- [License](#-license)

---

## 🎯 Overview

The **AI Content Repurposing Tool** is a comprehensive SaaS solution designed for content creators, marketers, and businesses who need to maximize their content's reach across multiple platforms. Instead of manually adapting content for each social network, this tool uses AI to intelligently transform your original content while maintaining your brand voice and optimizing for each platform's unique requirements.

### Why Use This Tool?

| Challenge | Solution |
|-----------|----------|
| Time-consuming manual adaptation | Automated AI-powered generation in seconds |
| Platform-specific formatting | Built-in character limits & best practices |
| Inconsistent brand voice | Custom brand voice templates |
| Managing multiple outputs | Centralized content library & history |
| Engagement optimization | Platform-specific prompts for maximum reach |

---

## ✨ Key Features

### 🔄 Content Input
- **Multi-format Support**: Text, URLs, and file uploads (.txt, .md, .pdf, .docx)
- **Smart Parsing**: Automatic content extraction and word count calculation
- **Drag & Drop**: Intuitive file upload interface

### 🤖 AI-Powered Generation
- **Groq Integration**: Ultra-fast inference with LLaMA 3.3 70B Versatile
- **7 Platform Targets**: Twitter, LinkedIn, Instagram, Facebook, TikTok, Email, Summary
- **5 Tone Options**: Professional, Casual, Enthusiastic, Educational, Humorous

### 🎨 Brand Customization
- **Brand Voice Templates**: Save custom instructions for consistent messaging
- **Default Templates**: Set preferred brand voice as default
- **Tone Flexibility**: Mix brand voice with different tones

### 📊 Content Management
- **Content Library**: Store and organize all original content
- **Generation History**: Track all AI-generated outputs
- **CRUD Operations**: Full control over content lifecycle

### 👤 User Experience
- **Secure Authentication**: JWT-based with auto-refresh
- **Responsive Dashboard**: Real-time statistics and quick actions
- **One-Click Copy**: Easy clipboard integration for generated content

---

## 🏗️ Functional Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                                   CLIENT LAYER                                       │
│  ┌──────────────────────────────────────────────────────────────────────────────┐   │
│  │                        React 18 + Vite Frontend                               │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │   │
│  │  │    Auth     │  │   Content   │  │ Generation  │  │      Settings       │  │   │
│  │  │   Pages     │  │   Upload    │  │    Form     │  │       Page          │  │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────────────┘  │   │
│  │         │                │                │                    │              │   │
│  │         └────────────────┴────────────────┴────────────────────┘              │   │
│  │                                    │                                           │   │
│  │                          ┌─────────┴─────────┐                                │   │
│  │                          │   Zustand Store   │                                │   │
│  │                          │  (State Manager)  │                                │   │
│  │                          └─────────┬─────────┘                                │   │
│  │                                    │                                           │   │
│  │                          ┌─────────┴─────────┐                                │   │
│  │                          │   Axios Client    │                                │   │
│  │                          │  (API Service)    │                                │   │
│  │                          └─────────┬─────────┘                                │   │
│  └────────────────────────────────────┼──────────────────────────────────────────┘   │
└───────────────────────────────────────┼─────────────────────────────────────────────┘
                                        │ HTTP/REST
                                        ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                                   API LAYER                                          │
│  ┌──────────────────────────────────────────────────────────────────────────────┐   │
│  │                         FastAPI Application                                   │   │
│  │                                                                               │   │
│  │   ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐    │   │
│  │   │  /api/auth  │  │/api/content │  │/api/generate│  │   /api/user     │    │   │
│  │   ├─────────────┤  ├─────────────┤  ├─────────────┤  ├─────────────────┤    │   │
│  │   │ • register  │  │ • upload    │  │ • repurpose │  │ • profile       │    │   │
│  │   │ • login     │  │ • upload-   │  │ • regenerate│  │ • brand-voice   │    │   │
│  │   │ • refresh   │  │   file      │  │ • history   │  │ • brand-voices  │    │   │
│  │   │             │  │ • list/CRUD │  │ • get/delete│  │ • CRUD ops      │    │   │
│  │   └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  └────────┬────────┘    │   │
│  │          │                │                │                   │             │   │
│  │          └────────────────┴────────────────┴───────────────────┘             │   │
│  │                                    │                                          │   │
│  │                          ┌─────────┴─────────┐                               │   │
│  │                          │  JWT Middleware   │                               │   │
│  │                          │  (Authentication) │                               │   │
│  │                          └─────────┬─────────┘                               │   │
│  └────────────────────────────────────┼──────────────────────────────────────────┘   │
└───────────────────────────────────────┼─────────────────────────────────────────────┘
                                        │
                                        ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                                 SERVICE LAYER                                        │
│  ┌──────────────────┐  ┌───────────────────┐  ┌────────────────────────────────┐   │
│  │   Auth Service   │  │  Content Service  │  │         AI Service             │   │
│  ├──────────────────┤  ├───────────────────┤  ├────────────────────────────────┤   │
│  │ • Password hash  │  │ • File parsing    │  │ • Groq API integration         │   │
│  │ • JWT creation   │  │ • URL extraction  │  │ • Platform-specific prompts    │   │
│  │ • Token verify   │  │ • Word counting   │  │ • Response parsing             │   │
│  │ • Refresh logic  │  │ • Content CRUD    │  │ • Mock fallback (development)  │   │
│  └────────┬─────────┘  └─────────┬─────────┘  └─────────────┬──────────────────┘   │
│           │                      │                          │                       │
│           │                      │                          │ ┌───────────────────┐ │
│           │                      │                          │ │  Groq Cloud API   │ │
│           │                      │                          └─│ (LLaMA 3.3 70B)   │ │
│           │                      │                            └───────────────────┘ │
│           └──────────────────────┴─────────────────────────────┐                    │
└──────────────────────────────────────────────────────────────────────────────────────┘
                                                                 │
                                                                 ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                                  DATA LAYER                                          │
│  ┌──────────────────────────────────────────────────────────────────────────────┐   │
│  │                          SQLAlchemy ORM                                       │   │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────────────────┐  │   │
│  │  │   Users    │  │  Content   │  │Generations │  │     Brand Voices       │  │   │
│  │  ├────────────┤  ├────────────┤  ├────────────┤  ├────────────────────────┤  │   │
│  │  │ id         │  │ id         │  │ id         │  │ id                     │  │   │
│  │  │ email      │  │ user_id    │  │ content_id │  │ user_id                │  │   │
│  │  │ password   │  │ title      │  │ user_id    │  │ name                   │  │   │
│  │  │ username   │  │ content    │  │ platform   │  │ instructions           │  │   │
│  │  │ plan       │  │ type       │  │ text       │  │ is_default             │  │   │
│  │  │ is_active  │  │ word_count │  │ tone       │  │ created_at             │  │   │
│  │  └─────┬──────┘  └─────┬──────┘  └─────┬──────┘  └────────────┬───────────┘  │   │
│  │        │               │               │                      │              │   │
│  │        └───────────────┴───────────────┴──────────────────────┘              │   │
│  │                                        │                                      │   │
│  │                              ┌─────────┴─────────┐                           │   │
│  │                              │    PostgreSQL     │                           │   │
│  │                              │     Database      │                           │   │
│  │                              └───────────────────┘                           │   │
│  └──────────────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

### Data Flow

```
┌─────────┐    ┌──────────┐    ┌──────────┐    ┌─────────┐    ┌──────────┐
│  User   │───▶│  Upload  │───▶│  Parse   │───▶│  Store  │───▶│ Generate │
│ Content │    │  (React) │    │ Content  │    │  in DB  │    │ AI Call  │
└─────────┘    └──────────┘    └──────────┘    └─────────┘    └─────┬────┘
                                                                     │
┌─────────┐    ┌──────────┐    ┌──────────┐    ┌─────────┐          │
│   Copy  │◀───│  Display │◀───│  Parse   │◀───│  Groq   │◀─────────┘
│ to Clip │    │  Results │    │ Response │    │   API   │
└─────────┘    └──────────┘    └──────────┘    └─────────┘
```

---

## 🛠️ Tech Stack

### Backend
| Technology | Purpose | Version |
|------------|---------|---------|
| **FastAPI** | Web framework | 0.104+ |
| **PostgreSQL** | Database | 12+ |
| **SQLAlchemy** | ORM | 2.0+ |
| **Pydantic** | Data validation | 2.0+ |
| **JWT** | Authentication | - |
| **bcrypt** | Password hashing | - |
| **Groq SDK** | AI integration | Latest |

### Frontend
| Technology | Purpose | Version |
|------------|---------|---------|
| **React** | UI framework | 18.2+ |
| **Vite** | Build tool | 5.0+ |
| **Tailwind CSS** | Styling | 3.3+ |
| **Zustand** | State management | 4.4+ |
| **Axios** | HTTP client | 1.6+ |
| **Lucide React** | Icons | Latest |
| **React Hot Toast** | Notifications | 2.4+ |

---

## 📁 Project Structure

```
ai-content-repurposing-tool/
├── 📂 backend/
│   ├── 📄 main.py                  # FastAPI app entry & CORS
│   ├── 📄 config.py                # Settings & environment vars
│   ├── 📄 database.py              # Database connection
│   ├── 📄 models.py                # SQLAlchemy ORM models
│   ├── 📄 schemas.py               # Pydantic request/response schemas
│   ├── 📄 prompts.py               # AI prompt templates
│   ├── 📄 utils.py                 # Utility functions
│   ├── 📂 api/
│   │   ├── 📄 auth.py              # Auth endpoints (register, login)
│   │   ├── 📄 content.py           # Content CRUD endpoints
│   │   ├── 📄 generate.py          # AI generation endpoints
│   │   └── 📄 user.py              # User & brand voice endpoints
│   ├── 📂 services/
│   │   ├── 📄 ai_service.py        # Groq API integration
│   │   ├── 📄 auth_service.py      # JWT & password utilities
│   │   └── 📄 content_service.py   # File parsing & content logic
│   ├── 📂 uploads/                 # Uploaded files storage
│   └── 📄 requirements.txt
│
├── 📂 frontend/
│   ├── 📄 index.html
│   ├── 📄 vite.config.js
│   ├── 📄 tailwind.config.js
│   ├── 📄 package.json
│   └── 📂 src/
│       ├── 📄 App.jsx              # Main app with routing
│       ├── 📄 main.jsx             # React entry point
│       ├── 📄 store.js             # Zustand state store
│       ├── 📄 index.css            # Global styles
│       ├── 📂 components/
│       │   ├── 📄 Navbar.jsx
│       │   ├── 📄 ProtectedRoute.jsx
│       │   ├── 📂 auth/
│       │   │   ├── 📄 LoginForm.jsx
│       │   │   └── 📄 RegisterForm.jsx
│       │   ├── 📂 content/
│       │   │   ├── 📄 ContentUpload.jsx
│       │   │   └── 📄 ContentList.jsx
│       │   └── 📂 generation/
│       │       └── 📄 GenerationForm.jsx
│       ├── 📂 pages/
│       │   ├── 📄 LoginPage.jsx
│       │   ├── 📄 RegisterPage.jsx
│       │   ├── 📄 DashboardPage.jsx
│       │   ├── 📄 NewProjectPage.jsx
│       │   ├── 📄 ContentLibraryPage.jsx
│       │   └── 📄 SettingsPage.jsx
│       ├── 📂 services/
│       │   ├── 📄 api.js           # Axios instance
│       │   ├── 📄 authService.js   # Auth API calls
│       │   └── 📄 contentService.js # Content API calls
│       └── 📂 hooks/
│           └── 📄 useAuth.js       # Auth hook
│
└── 📄 README.md
```

---

## 🚀 Getting Started

### Prerequisites

- **Python** 3.9 or higher
- **Node.js** 16 or higher
- **PostgreSQL** 12 or higher
- **Git**
- **Groq API Key** ([Get one here](https://console.groq.com/))

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd ai-content-repurposing-tool
```

### Step 2: Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env
```

### Step 3: Configure Backend Environment

Edit `.env` file:

```env
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/content_repurpose
SECRET_KEY=your-super-secret-key-at-least-32-characters-long
GROQ_API_KEY=YOUR_GROQ_API_KEY_HERE
ALLOWED_ORIGINS=http://localhost:3000
DEBUG=True
```

### Step 4: Initialize Database

```bash
# Create PostgreSQL database
createdb content_repurpose

# Or via psql:
psql -U postgres -c "CREATE DATABASE content_repurpose;"

# Run the app (tables created automatically on startup)
uvicorn main:app --reload
```

The backend API will be available at: `http://localhost:8000`

- **Interactive API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

### Step 5: Frontend Setup

```bash
# Navigate to frontend (from project root)
cd frontend

# Install dependencies
npm install

# Create environment file
echo "VITE_API_URL=http://localhost:8000/api" > .env.local

# Start development server
npm run dev
```

The frontend will be available at: `http://localhost:3000`

---

## 🔐 Environment Variables

### Backend (`.env`)

| Variable | Description | Required | Example |
|----------|-------------|----------|---------|
| `DATABASE_URL` | PostgreSQL connection string | ✅ | `postgresql://user:pass@localhost:5432/dbname` |
| `SECRET_KEY` | JWT signing key (min 32 chars) | ✅ | `your-super-secret-key-...` |
| `GROQ_API_KEY` | Groq API key for AI | ✅ | `YOUR_GROQ_API_KEY` |
| `GROQ_MODEL` | AI model name | ❌ | `llama-3.3-70b-versatile` (default) |
| `ALLOWED_ORIGINS` | CORS allowed origins | ❌ | `http://localhost:3000` |
| `DEBUG` | Enable debug mode | ❌ | `True` |

### Frontend (`.env.local`)

| Variable | Description | Required | Example |
|----------|-------------|----------|---------|
| `VITE_API_URL` | Backend API base URL | ✅ | `http://localhost:8000/api` |

---

## 📚 API Reference

### Authentication

| Endpoint | Method | Description | Auth Required |
|----------|--------|-------------|---------------|
| `/api/auth/register` | POST | Register new user | ❌ |
| `/api/auth/login` | POST | Login and get tokens | ❌ |
| `/api/auth/refresh` | POST | Refresh access token | ✅ |

### Content Management

| Endpoint | Method | Description | Auth Required |
|----------|--------|-------------|---------------|
| `/api/content/upload` | POST | Upload text/URL content | ✅ |
| `/api/content/upload-file` | POST | Upload file (.txt, .md, .pdf, .docx) | ✅ |
| `/api/content/` | GET | List all user content | ✅ |
| `/api/content/{id}` | GET | Get specific content | ✅ |
| `/api/content/{id}` | PUT | Update content | ✅ |
| `/api/content/{id}` | DELETE | Delete content | ✅ |

### Content Generation

| Endpoint | Method | Description | Auth Required |
|----------|--------|-------------|---------------|
| `/api/generate/repurpose` | POST | Generate platform content | ✅ |
| `/api/generate/regenerate/{id}` | POST | Regenerate specific output | ✅ |
| `/api/generate/history` | GET | Get generation history | ✅ |
| `/api/generate/{id}` | GET | Get specific generation | ✅ |
| `/api/generate/{id}` | DELETE | Delete generation | ✅ |

### User & Brand Voice

| Endpoint | Method | Description | Auth Required |
|----------|--------|-------------|---------------|
| `/api/user/profile` | GET | Get user profile | ✅ |
| `/api/user/profile` | PUT | Update user profile | ✅ |
| `/api/user/brand-voice` | POST | Create brand voice template | ✅ |
| `/api/user/brand-voices` | GET | List all brand voices | ✅ |
| `/api/user/brand-voice/{id}` | GET | Get specific brand voice | ✅ |
| `/api/user/brand-voice/{id}` | PUT | Update brand voice | ✅ |
| `/api/user/brand-voice/{id}` | DELETE | Delete brand voice | ✅ |

---

## 💾 Database Schema

```mermaid
erDiagram
    USERS ||--o{ CONTENT : creates
    USERS ||--o{ GENERATIONS : owns
    USERS ||--o{ BRAND_VOICES : defines
    CONTENT ||--o{ GENERATIONS : generates
    BRAND_VOICES ||--o{ GENERATIONS : applies

    USERS {
        int id PK
        string email UK
        string password_hash
        string username UK
        timestamp created_at
        timestamp updated_at
        boolean is_active
        string plan
    }

    CONTENT {
        int id PK
        int user_id FK
        string title
        text original_content
        string content_type
        string source_url
        int word_count
        timestamp created_at
        timestamp updated_at
    }

    GENERATIONS {
        int id PK
        int content_id FK
        int user_id FK
        string platform
        text generated_text
        string tone
        int brand_voice_id FK
        json platform_metadata
        timestamp created_at
    }

    BRAND_VOICES {
        int id PK
        int user_id FK
        string name
        text instructions
        boolean is_default
        timestamp created_at
    }
```

---

## 🎯 Platform-Specific Generation

Each platform has optimized prompts for maximum engagement:

| Platform | Output Format | Key Features |
|----------|---------------|--------------|
| **Twitter** | Thread (5-8 tweets) | Hook first, 280 chars max, emojis, hashtags |
| **LinkedIn** | Professional post | 1300 chars, line breaks, 2-3 hashtags, CTA |
| **Instagram** | Caption + hashtags | 15-30 hashtags, emojis, engagement CTA |
| **Facebook** | Conversational post | Shareable, comment-worthy, 1-3 hashtags |
| **TikTok** | Video script | Hook in 3-5s, trending elements, timing |
| **Email** | Newsletter | 3 subject lines, body, CTA, P.S. line |
| **Summary** | Executive brief | TL;DR, summary, key takeaways, action items |

### Supported Tones

- 💼 **Professional** - Formal, authoritative, business-appropriate
- 😊 **Casual** - Friendly, conversational, approachable
- 🔥 **Enthusiastic** - Energetic, excited, motivating
- 📚 **Educational** - Informative, clear, instructive
- 😄 **Humorous** - Witty, playful, entertaining

---

## 🔒 Security

| Feature | Implementation |
|---------|----------------|
| **Password Hashing** | bcrypt with salt |
| **Authentication** | JWT with access & refresh tokens |
| **Token Expiry** | Access: 30 min, Refresh: 7 days |
| **Input Validation** | Pydantic schemas on all endpoints |
| **CORS** | Configurable allowed origins |
| **File Upload** | Extension validation, size limits |
| **SQL Injection** | SQLAlchemy ORM parameterization |

---

## 🚢 Deployment

### Backend Production

```bash
# Install production server
pip install gunicorn

# Set production environment variables
export DATABASE_URL=postgresql://...
export SECRET_KEY=production-secret-key-here
export GROQ_API_KEY=YOUR_GROQ_API_KEY
export DEBUG=False

# Run with Gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Docker Deployment

```dockerfile
# Backend Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Frontend Production

```bash
# Build for production
npm run build

# Deploy dist/ folder to:
# - Vercel: vercel deploy
# - Netlify: netlify deploy --prod --dir=dist
# - Any static hosting
```

---

## 🔧 Troubleshooting

### Database Connection Failed

```bash
# Verify PostgreSQL is running
pg_isready -h localhost -p 5432

# Check connection string format
# postgresql://username:password@host:port/database
```

### CORS Errors

```bash
# Ensure ALLOWED_ORIGINS includes your frontend URL
# In .env:
ALLOWED_ORIGINS=http://localhost:3000,https://yourdomain.com
```

### AI Generation Not Working

1. Verify `GROQ_API_KEY` is set correctly
2. Check API key at [console.groq.com](https://console.groq.com)
3. The app falls back to mock responses if Groq is unavailable

### Token Errors

- Ensure `SECRET_KEY` is at least 32 characters
- Clear browser localStorage and re-login
- Check token expiration in API responses

---

## 🗺️ Future Roadmap

- [ ] 🎥 **Video/Audio Transcription** - Whisper API integration
- [ ] 📊 **Advanced Analytics** - Engagement tracking & insights
- [ ] 👥 **Team Collaboration** - Multi-user workspaces
- [ ] 🔌 **API Access** - Developer API for third-party integrations
- [ ] 💳 **Stripe Payments** - Subscription billing
- [ ] 📱 **Social Auto-Posting** - Direct platform publishing
- [ ] 🧪 **A/B Testing** - Content variation testing
- [ ] 📅 **Scheduling** - Calendar view & scheduled posts
- [ ] 🏷️ **White-Label** - Custom branding options
- [ ] 📈 **Advanced Reports** - PDF export & analytics

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 💬 Support

Need help? Here's how to get support:

1. 📖 Check this documentation thoroughly
2. 🔍 Review API docs at `/docs` endpoint
3. 🐛 Check browser console & backend logs
4. 📝 Open an issue on GitHub

---

<p align="center">
  <strong>Built with ❤️ for Content Creators</strong>
</p>

<p align="center">
  <sub>Transform your content. Amplify your reach. Save time.</sub>
</p>
