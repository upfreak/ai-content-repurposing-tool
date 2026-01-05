from config import settings
import logging
import json

logger = logging.getLogger(__name__)


class AIService:
    """Service for interacting with Groq API (falls back to mock if Groq client fails)"""

    def __init__(self):
        self.model = settings.GROQ_MODEL
        self.client = None
        try:
            from groq import Groq
            self.client = Groq(api_key=settings.GROQ_API_KEY)
        except Exception as e:
            logger.warning(f"Groq client unavailable, using mock AI service: {e}")
    
    async def generate_repurposed_content(
        self,
        original_content: str,
        platforms: list,
        tone: str,
        brand_voice: str = None
    ) -> dict:
        """Generate content for multiple platforms"""
        
        results = {}

        # If Groq client not available, return mocked outputs for testing
        if not self.client:
            for platform in platforms:
                snippet = (original_content or "").strip()[:400]
                mock = {
                    "content": f"[MOCK {platform.upper()}] {snippet}",
                    "platform": platform
                }
                results[platform] = mock
            return results

        for platform in platforms:
            try:
                prompt = self._build_prompt(
                    original_content,
                    platform,
                    tone,
                    brand_voice
                )

                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {
                            "role": "system",
                            "content": "You are an expert content repurposing assistant that creates engaging, platform-optimized content."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=0.7,
                    max_tokens=2000
                )

                content = response.choices[0].message.content
                results[platform] = self._parse_response(content, platform)

            except Exception as e:
                logger.error(f"Error generating content for {platform}: {str(e)}")
                results[platform] = {"error": str(e)}

        return results
    
    def _build_prompt(
        self,
        content: str,
        platform: str,
        tone: str,
        brand_voice: str = None
    ) -> str:
        """Build platform-specific prompt"""
        
        base_instructions = f"""You are helping repurpose content for {platform}. 
Tone: {tone}
{f'Brand voice: {brand_voice}' if brand_voice else ''}

ORIGINAL CONTENT:
{content}

"""
        
        platform_prompts = {
            "twitter": self._twitter_prompt,
            "linkedin": self._linkedin_prompt,
            "instagram": self._instagram_prompt,
            "facebook": self._facebook_prompt,
            "tiktok": self._tiktok_prompt,
            "email": self._email_prompt,
            "summary": self._summary_prompt,
        }
        
        prompt_builder = platform_prompts.get(platform, self._default_prompt)
        return base_instructions + prompt_builder()
    
    def _twitter_prompt(self) -> str:
        return """Generate a Twitter thread of 5-8 tweets that:
- First tweet is a compelling hook
- Each tweet is 200-280 characters
- Uses line breaks for readability
- Includes relevant emojis (2-3 per tweet)
- Ends with a CTA in the last tweet
- Returns JSON format: {"tweets": [{"number": 1, "text": "..."}, ...], "hashtags": [...]}"""
    
    def _linkedin_prompt(self) -> str:
        return """Generate a LinkedIn professional post that:
- Is 1300 characters or less
- Starts with a hook
- Uses line breaks for readability
- Includes 2-3 relevant hashtags
- Ends with a professional CTA
- Returns JSON format: {"post": "...", "hashtags": [...]}"""
    
    def _instagram_prompt(self) -> str:
        return """Generate Instagram captions and scripts that:
- Include 5-15 relevant hashtags
- Have engaging, creative language
- Include emojis strategically
- Returns JSON format: {"caption": "...", "hashtags": [...]}"""
    
    def _facebook_prompt(self) -> str:
        return """Generate a Facebook post that:
- Is engaging and conversational
- Includes a clear call-to-action
- Uses emojis appropriately
- Encourages comments/shares
- Returns JSON format: {"post": "...", "cta": "..."}"""
    
    def _tiktok_prompt(self) -> str:
        return """Generate TikTok video script hooks that:
- Are 15-60 seconds when read aloud
- Have a compelling opening
- Include trending concepts if relevant
- Returns JSON format: {"script": "...", "hashtags": [...]}"""
    
    def _email_prompt(self) -> str:
        return """Generate email newsletter content with:
- 3 different subject line options
- Email body (150-300 words)
- Clear CTA
- Returns JSON format: {"subject_lines": [...], "body": "...", "cta": "..."}"""
    
    def _summary_prompt(self) -> str:
        return """Generate content summaries with:
- TL;DR (50 words max)
- Executive summary (100-150 words)
- Key takeaways (3-5 bullet points)
- Returns JSON format: {"tldr": "...", "summary": "...", "key_takeaways": [...]}"""
    
    def _default_prompt(self) -> str:
        return "Repurpose this content for maximum engagement and relevance. Return JSON format output."
    
    def _parse_response(self, response: str, platform: str) -> dict:
        """Parse AI response and extract structured data"""
        try:
            # Try to extract JSON from response
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            
            if json_start != -1 and json_end > json_start:
                json_str = response[json_start:json_end]
                return json.loads(json_str)
            
            # Fallback to returning as is
            return {"content": response, "platform": platform}
        except json.JSONDecodeError:
            logger.warning(f"Failed to parse JSON response for {platform}")
            return {"content": response, "platform": platform}
