"""
Utility functions for prompts and AI integration
"""

SYSTEM_PROMPT = """You are an expert content repurposing specialist. Your role is to transform long-form content into platform-specific, engaging social media posts while maintaining the core message and value.

Key principles:
1. Adapt tone and style to match platform norms
2. Optimize for engagement and shareability
3. Maintain accuracy and credibility
4. Include relevant hashtags and CTAs
5. Follow platform best practices
6. Use emojis strategically
7. Keep the brand voice consistent

Always provide responses in the specified format (usually JSON) for easy parsing."""

PLATFORM_PROMPTS = {
    "twitter": """Generate a Twitter thread (5-8 tweets) from this content. 

Requirements:
- First tweet must be a compelling hook that stops scrolling
- Each tweet: 200-280 characters max
- Use line breaks for readability
- Include 2-3 relevant emojis per tweet
- End with a clear call-to-action (CTA) in the final tweet
- Use {tone} tone
- {brand_voice_instruction}

Format output as JSON:
{{
  "tweets": [
    {{"number": 1, "text": "...", "emoji": "..."}},
    {{"number": 2, "text": "...", "emoji": "..."}}
  ],
  "hashtags": ["#hashtag1", "#hashtag2"],
  "engagement_tip": "Best time to post and engagement tactics"
}}""",

    "linkedin": """Generate a LinkedIn professional post from this content.

Requirements:
- Length: Up to 1300 characters
- Start with a compelling hook
- Use line breaks for readability (5-7 line breaks)
- Include 2-3 relevant hashtags at the end
- Focus on professional value and insights
- Use {tone} tone
- {brand_voice_instruction}
- End with a clear call-to-action

Format output as JSON:
{{
  "post": "Full post content here",
  "hashtags": ["#hashtag1", "#hashtag2", "#hashtag3"],
  "cta": "Specific call-to-action",
  "engagement_tip": "Tips for maximum engagement"
}}""",

    "instagram": """Generate Instagram captions from this content.

Requirements:
- Lead with 1-2 emojis and an attention-grabbing first line
- Include a caption (200-300 characters)
- Use 15-30 relevant hashtags
- Use {tone} tone
- {brand_voice_instruction}
- Include call-to-action (e.g., "Double tap if you agree")
- Format with line breaks for readability

Format output as JSON:
{{
  "caption": "Full caption with initial hook",
  "hashtags": ["#hashtag1", "#hashtag2", ...],
  "cta": "Call-to-action",
  "emoji_suggestions": ["😀", "🚀"],
  "carousel_script": "Optional: Script for carousel posts (if applicable)"
}}""",

    "facebook": """Generate a Facebook post from this content.

Requirements:
- Conversational and engaging tone
- 200-500 characters (can be longer)
- Use 1-3 hashtags maximum
- Include 2-4 emojis strategically placed
- Use {tone} tone
- {brand_voice_instruction}
- Share personal stories or relatable elements
- Clear call-to-action
- Encourage comments and shares

Format output as JSON:
{{
  "post": "Full post content",
  "hashtags": ["#hashtag1"],
  "cta": "Clear call-to-action",
  "emoji_guide": "Where to place emojis for maximum impact"
}}""",

    "tiktok": """Generate a TikTok video script from this content.

Requirements:
- Hook viewers in the first 3-5 seconds
- Total runtime: 15-60 seconds
- Include trending sounds or music descriptions
- Use {tone} tone
- {brand_voice_instruction}
- On-screen text suggestions
- Call-to-action (follow, like, comment, share)
- Trending hashtags and effects

Format output as JSON:
{{
  "hook": "First 5 seconds - must be attention-grabbing",
  "script": "Full video script with timing",
  "trending_elements": ["sound name", "effect name", "#hashtag"],
  "hashtags": ["#hashtag1", "#hashtag2"],
  "cta": "Clear call-to-action",
  "timing": {{"hook": "0-5s", "main": "5-45s", "cta": "45-60s"}}
}}""",

    "email": """Generate email newsletter content from this content.

Requirements:
- 3 different subject line options (50 characters max each)
- Email body: 200-400 words
- Clear value proposition in first paragraph
- Include specific call-to-action
- Use {tone} tone
- {brand_voice_instruction}
- Personalization suggestions
- P.S. line for additional engagement

Format output as JSON:
{{
  "subject_lines": [
    {{"option": 1, "text": "Subject line 1", "vibe": "curiosity"}},
    {{"option": 2, "text": "Subject line 2", "vibe": "value"}},
    {{"option": 3, "text": "Subject line 3", "vibe": "urgency"}}
  ],
  "preview_text": "Preview text for email client (80 chars)",
  "body": "Full email body",
  "cta": "Primary call-to-action",
  "ps": "P.S. line for additional engagement"
}}""",

    "summary": """Generate content summaries from this content.

Requirements:
- TL;DR (maximum 50 words)
- Executive Summary (100-150 words)
- Key Takeaways (3-5 bullet points)
- Use {tone} tone
- {brand_voice_instruction}
- Highlight most important information
- Make it scannable and easy to digest

Format output as JSON:
{{
  "tldr": "One-sentence summary (max 50 words)",
  "executive_summary": "Paragraph summary (100-150 words)",
  "key_takeaways": [
    "Takeaway 1",
    "Takeaway 2",
    "Takeaway 3"
  ],
  "action_items": [
    "Action item 1",
    "Action item 2"
  ],
  "best_for": "Who should read this and why"
}}"""
}

def get_platform_prompt(platform: str, tone: str, brand_voice: str = None) -> str:
    """Get platform-specific prompt"""
    
    if platform not in PLATFORM_PROMPTS:
        return f"Repurpose this content for {platform} using {tone} tone. Focus on engagement and platform best practices."
    
    base_prompt = PLATFORM_PROMPTS[platform]
    
    # Add brand voice instruction if provided
    if brand_voice:
        brand_voice_instruction = f"Brand voice guidelines: {brand_voice}"
    else:
        brand_voice_instruction = "Maintain a professional and authentic brand voice."
    
    # Format the prompt
    return base_prompt.format(
        tone=tone,
        brand_voice_instruction=brand_voice_instruction
    )
