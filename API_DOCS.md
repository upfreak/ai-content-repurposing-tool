# API Documentation

## Base URL

```
http://localhost:8000/api
```

## Authentication

All endpoints (except `/auth/register` and `/auth/login`) require JWT authentication.

### Header Format
```
Authorization: Bearer <access_token>
```

## Response Format

All responses follow this format:

### Success Response
```json
{
  "status": "success",
  "data": { ... },
  "message": "Operation successful"
}
```

### Error Response
```json
{
  "status": "error",
  "detail": "Error message",
  "status_code": 400
}
```

## Endpoints

### Authentication

#### Register
```
POST /auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "username": "username",
  "password": "securepassword123"
}

Response:
{
  "id": 1,
  "email": "user@example.com",
  "username": "username",
  "created_at": "2024-01-15T10:30:00",
  "plan": "free",
  "is_active": true
}
```

#### Login
```
POST /auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword123"
}

Response:
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

#### Refresh Token
```
POST /auth/refresh
Content-Type: application/json

{
  "refresh_token": "eyJhbGciOiJIUzI1NiIs..."
}

Response:
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

### Content Management

#### Upload Text/URL Content
```
POST /content/upload
Content-Type: application/json
Authorization: Bearer <token>

{
  "title": "My Blog Post",
  "original_content": "Lorem ipsum dolor sit amet...",
  "content_type": "text"  // or "url"
}

Response:
{
  "id": 1,
  "user_id": 1,
  "title": "My Blog Post",
  "original_content": "Lorem ipsum dolor sit amet...",
  "content_type": "text",
  "word_count": 150,
  "created_at": "2024-01-15T10:30:00",
  "updated_at": "2024-01-15T10:30:00"
}
```

#### Upload File
```
POST /content/upload-file
Content-Type: multipart/form-data
Authorization: Bearer <token>

Form Data:
- title: "My Document"
- file: <binary file data>

Response: (Same as upload text)
```

#### List Content
```
GET /content/?skip=0&limit=20
Authorization: Bearer <token>

Response:
[
  {
    "id": 1,
    "user_id": 1,
    "title": "My Blog Post",
    "original_content": "Lorem ipsum...",
    "content_type": "text",
    "word_count": 150,
    "created_at": "2024-01-15T10:30:00"
  },
  ...
]
```

#### Get Content
```
GET /content/1
Authorization: Bearer <token>

Response: (Single content object)
```

#### Update Content
```
PUT /content/1
Content-Type: application/json
Authorization: Bearer <token>

{
  "title": "Updated Title"
}

Response: (Updated content object)
```

#### Delete Content
```
DELETE /content/1
Authorization: Bearer <token>

Response: 204 No Content
```

### Content Generation

#### Generate Repurposed Content
```
POST /generate/repurpose
Content-Type: application/json
Authorization: Bearer <token>

{
  "content_id": 1,
  "platforms": ["twitter", "linkedin", "email"],
  "tone": "Professional",
  "brand_voice_id": null
}

Response:
{
  "content_id": 1,
  "platform_results": {
    "twitter": {
      "tweets": [
        {"number": 1, "text": "First tweet..."},
        {"number": 2, "text": "Second tweet..."}
      ],
      "hashtags": ["#hashtag1", "#hashtag2"]
    },
    "linkedin": {
      "post": "LinkedIn post content...",
      "hashtags": ["#hashtag1"]
    },
    "email": {
      "subject_lines": [
        "Subject 1",
        "Subject 2",
        "Subject 3"
      ],
      "body": "Email body...",
      "cta": "Click here"
    }
  },
  "generations": [
    {
      "id": 1,
      "content_id": 1,
      "platform": "twitter",
      "generated_text": "...",
      "tone": "Professional",
      "created_at": "2024-01-15T10:30:00"
    },
    ...
  ]
}
```

#### Regenerate Content
```
POST /generate/regenerate/1
Content-Type: application/json
Authorization: Bearer <token>

{
  "tone": "Casual"
}

Response: (Updated generation object)
```

#### Get Generation History
```
GET /generate/history?skip=0&limit=50&platform=twitter
Authorization: Bearer <token>

Response:
[
  {
    "id": 1,
    "content_id": 1,
    "platform": "twitter",
    "generated_text": "...",
    "tone": "Professional",
    "created_at": "2024-01-15T10:30:00"
  },
  ...
]
```

#### Get Generation
```
GET /generate/1
Authorization: Bearer <token>

Response: (Single generation object)
```

#### Delete Generation
```
DELETE /generate/1
Authorization: Bearer <token>

Response: 204 No Content
```

### User Management

#### Get Profile
```
GET /user/profile
Authorization: Bearer <token>

Response:
{
  "id": 1,
  "email": "user@example.com",
  "username": "username",
  "created_at": "2024-01-15T10:30:00",
  "plan": "free",
  "is_active": true
}
```

#### Update Profile
```
PUT /user/profile
Content-Type: application/json
Authorization: Bearer <token>

{
  "username": "newusername",
  "plan": "pro"
}

Response: (Updated user object)
```

#### Create Brand Voice
```
POST /user/brand-voice
Content-Type: application/json
Authorization: Bearer <token>

{
  "name": "Professional Brand",
  "instructions": "Always use formal language, include statistics, professional tone..."
}

Response:
{
  "id": 1,
  "user_id": 1,
  "name": "Professional Brand",
  "instructions": "Always use formal language...",
  "is_default": false,
  "created_at": "2024-01-15T10:30:00"
}
```

#### List Brand Voices
```
GET /user/brand-voices
Authorization: Bearer <token>

Response:
[
  {
    "id": 1,
    "user_id": 1,
    "name": "Professional Brand",
    "instructions": "...",
    "is_default": false,
    "created_at": "2024-01-15T10:30:00"
  },
  ...
]
```

#### Get Brand Voice
```
GET /user/brand-voice/1
Authorization: Bearer <token>

Response: (Single brand voice object)
```

#### Update Brand Voice
```
PUT /user/brand-voice/1
Content-Type: application/json
Authorization: Bearer <token>

{
  "name": "Updated Name",
  "instructions": "Updated instructions...",
  "is_default": true
}

Response: (Updated brand voice object)
```

#### Delete Brand Voice
```
DELETE /user/brand-voice/1
Authorization: Bearer <token>

Response: 204 No Content
```

## Error Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | OK | Request successful |
| 201 | Created | Resource created successfully |
| 204 | No Content | Resource deleted successfully |
| 400 | Bad Request | Invalid input data |
| 401 | Unauthorized | Missing or invalid authentication |
| 403 | Forbidden | User doesn't have permission |
| 404 | Not Found | Resource not found |
| 409 | Conflict | Resource already exists |
| 422 | Unprocessable Entity | Validation error |
| 500 | Server Error | Internal server error |

## Rate Limiting

- **Free Plan**: 100 requests per hour per user
- **Pro Plan**: Unlimited (future feature)

Rate limit headers:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1705317600
```

## Example Requests

### cURL

```bash
# Register
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "username",
    "password": "password123"
  }'

# Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123"
  }'

# Upload content
curl -X POST http://localhost:8000/api/content/upload \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My Post",
    "original_content": "Content...",
    "content_type": "text"
  }'
```

### JavaScript (Fetch)

```javascript
// Register
const response = await fetch('http://localhost:8000/api/auth/register', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    email: 'user@example.com',
    username: 'username',
    password: 'password123'
  })
});

// Login
const loginResponse = await fetch('http://localhost:8000/api/auth/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    email: 'user@example.com',
    password: 'password123'
  })
});

const { access_token } = await loginResponse.json();

// Upload content
const contentResponse = await fetch('http://localhost:8000/api/content/upload', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${access_token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    title: 'My Post',
    original_content: 'Content...',
    content_type: 'text'
  })
});
```

## Interactive Documentation

Access the interactive API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
