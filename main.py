import os
from fastmcp import FastMCP
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs

# Initialize the server
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

        ytt_api = YouTubeTranscriptApi()
        fetched_transcript = ytt_api.fetch(video_id, languages=['en'])
        full_text = " ".join(snippet.text for snippet in fetched_transcript)

        return f"--- TRANSCRIPT FOR VIDEO {video_id} ---\n\n{full_text}"
    except Exception as e:
        return f"Could not fetch transcript: {str(e)}"

if __name__ == "__main__":
    # Render automatically tells us what port to use via this environment variable
    port = int(os.environ.get("PORT", 8000))
    
    # Run using the new standard HTTP transport
    mcp.run(transport="streamable-http", host="0.0.0.0", port=port)
