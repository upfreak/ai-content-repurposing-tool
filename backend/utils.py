import os
from datetime import datetime

def create_sample_brand_voices():
    """Create sample brand voice templates for users"""
    return [
        {
            "name": "Professional Corporate",
            "instructions": """Your brand voice is professional and authoritative. 
Guidelines:
- Use formal, polished language
- Include relevant statistics and data
- Maintain a serious, confident tone
- Target business professionals and C-suite executives
- Avoid slang and casual language
- Always proofread for grammatical accuracy
- Use industry-specific terminology appropriately"""
        },
        {
            "name": "Casual & Friendly",
            "instructions": """Your brand voice is approachable and conversational.
Guidelines:
- Use conversational, friendly language
- Include personal anecdotes and relatable examples
- Use contractions and informal sentence structures
- Add emojis strategically (2-3 per post)
- Be authentic and genuine
- Use humor occasionally (but appropriately)
- Make readers feel like they're talking to a friend"""
        },
        {
            "name": "Educational & Informative",
            "instructions": """Your brand voice is educational and knowledge-focused.
Guidelines:
- Explain concepts clearly and thoroughly
- Break down complex ideas into digestible pieces
- Use examples and case studies
- Include actionable takeaways
- Maintain accuracy above all else
- Cite sources when appropriate
- Structure content for easy learning"""
        },
        {
            "name": "Enthusiastic & Energetic",
            "instructions": """Your brand voice is enthusiastic and energetic.
Guidelines:
- Use exclamation points and energetic language
- Include lots of relevant emojis
- Express genuine excitement about topics
- Use power words and dynamic verbs
- Create a sense of urgency and momentum
- Be positive and optimistic
- Inspire action and engagement"""
        },
        {
            "name": "Witty & Humorous",
            "instructions": """Your brand voice is clever, witty, and humorous.
Guidelines:
- Use clever wordplay and puns
- Include relatable humor
- Be sarcastic when appropriate
- Use memes and cultural references
- Keep humor inclusive and inoffensive
- Balance humor with substance
- Make readers smile while delivering value"""
        }
    ]


def create_platform_guidelines():
    """Platform-specific guidelines for content generation"""
    return {
        "twitter": {
            "char_limit": 280,
            "best_practices": [
                "Hook the reader in the first 20 characters",
                "Use 2-3 relevant emojis per tweet",
                "Include 1-2 hashtags maximum",
                "Ask questions to drive engagement",
                "Break threads into 5-8 tweets for clarity"
            ],
            "engagement_tips": [
                "Post between 8-10 AM or 5-6 PM",
                "Use trending hashtags",
                "Ask for retweets and replies"
            ]
        },
        "linkedin": {
            "char_limit": 1300,
            "best_practices": [
                "Start with a compelling hook",
                "Use line breaks for readability",
                "Include 2-3 relevant hashtags",
                "Focus on professional value",
                "Tell stories and share insights",
                "End with a call-to-action"
            ],
            "engagement_tips": [
                "Post during business hours (8 AM - 5 PM)",
                "Use metrics and data",
                "Share articles and insights"
            ]
        },
        "instagram": {
            "char_limit": 2200,
            "best_practices": [
                "Lead with emojis and visual descriptions",
                "Use 15-30 hashtags for reach",
                "Include a clear call-to-action",
                "Use line breaks for readability",
                "Focus on visual storytelling",
                "Link hashtags naturally in text"
            ],
            "engagement_tips": [
                "Post when audience is active (varies by niche)",
                "Use Instagram Stories for timely content",
                "Engage with comments in the first hour"
            ]
        },
        "facebook": {
            "char_limit": 63206,
            "best_practices": [
                "Start with an attention-grabbing hook",
                "Use 1-3 hashtags maximum",
                "Include emojis for personality",
                "Share personal stories",
                "Encourage comments and shares",
                "Use short paragraphs and line breaks"
            ],
            "engagement_tips": [
                "Post 1-2 times daily for best reach",
                "Respond to comments promptly",
                "Use Facebook Live for engagement"
            ]
        },
        "tiktok": {
            "char_limit": 150,
            "format": "Video script (15-60 seconds)",
            "best_practices": [
                "Hook viewers in first 3 seconds",
                "Use trending sounds and music",
                "Include on-screen text",
                "Show personality and emotion",
                "Use trending effects",
                "Make content shareable"
            ],
            "engagement_tips": [
                "Post 3-5 times per week",
                "Engage with sounds your audience loves",
                "Participate in TikTok trends",
                "Use captions and hashtags"
            ]
        },
        "email": {
            "char_limit": 5000,
            "best_practices": [
                "Create compelling subject lines (50 characters)",
                "Lead with value proposition",
                "Use personalization",
                "Keep paragraphs short",
                "Include clear call-to-action",
                "Use friendly, conversational tone"
            ],
            "engagement_tips": [
                "Send on Tuesday-Thursday",
                "A/B test subject lines",
                "Segment your email list",
                "Include a clear unsubscribe option"
            ]
        }
    }


# Setup instructions for developers
SETUP_INSTRUCTIONS = """
AI Content Repurposing Tool - Setup Instructions

BACKEND SETUP:
1. Navigate to backend directory: cd backend
2. Create virtual environment: python -m venv venv
3. Activate: venv\\Scripts\\activate (Windows) or source venv/bin/activate (Mac/Linux)
4. Install dependencies: pip install -r requirements.txt
5. Create .env file from .env.example
6. Create PostgreSQL database: createdb content_repurpose
7. Run backend: uvicorn main:app --reload

FRONTEND SETUP:
1. Navigate to frontend directory: cd frontend
2. Install dependencies: npm install
3. Run dev server: npm run dev
4. Open http://localhost:3000

FEATURES:
✓ User authentication with JWT
✓ Multi-format content input (text, URL, files)
✓ AI-powered content generation for 7 platforms
✓ Customizable tone and brand voice
✓ Content management and library
✓ Generation history
✓ User dashboard

PLATFORMS SUPPORTED:
- Twitter/X (thread format)
- LinkedIn (professional posts)
- Instagram (captions + hashtags)
- Facebook (engaging posts)
- TikTok (video scripts)
- Email (newsletters with subject lines)
- Summary (TL;DR, executive summary, key takeaways)

NEXT STEPS:
1. Configure .env files
2. Set up PostgreSQL database
3. Start backend server
4. Start frontend dev server
5. Register and test the application
"""
