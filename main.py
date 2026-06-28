import os
from mcp.server.fastmcp import FastMCP
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs

# 1. FIXED: Keep initialization simple with just the server name
mcp = FastMCP("YouTube Reader")

@mcp.tool()
def get_video_transcript(video_url: str) -> str:
    """Extracts the text transcript from a YouTube video URL."""
    try:
        parsed_url = urlparse(video_url)
        if "youtube.com" in parsed_url.netloc:
            video_id = parse_qs(parsed_url.query).get("v", [None])[0]
        elif "youtu.be" in parsed_url.netloc:
            video_id = parsed_url.path.strip("/")
        else:
            return "Error: Invalid YouTube link."

        if not video_id:
            return "Error: Could not find video ID."

        transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
        full_text = " ".join([item['text'] for item in transcript_list])
        return f"--- TRANSCRIPT FOR VIDEO {video_id} ---\n\n{full_text}"
    except Exception as e:
        return f"Could not fetch transcript: {str(e)}"

if __name__ == "__main__":
    # Get port from environment or default to 8000
    port = int(os.environ.get("PORT", 8000))
    
    # 2. FIXED: Transport strategy belongs down here in the run method
    mcp.run(transport="sse", host="0.0.0.0", port=port)
