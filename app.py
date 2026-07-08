import streamlit as st
import os
import re
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi
from google import genai

load_dotenv()

st.title("🎥 YouTube Video Summarizer")

def extract_video_id(url):
    pattern = r'(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})'
    match = re.search(pattern, url)
    return match.group(1) if match else None

def get_transcript(video_id):
    try:
        api = YouTubeTranscriptApi()
        transcript_list = api.fetch(video_id)
        return " ".join([item.text for item in transcript_list])
    except Exception as e:
        raise Exception(f"Could not retrieve transcript: {e}")

def summarize_transcript(transcript_text):
    api_key = os.getenv("API_KEY")
    if not api_key:
        raise ValueError("API_KEY environment variable is not set.")
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model='gemini-3.5-flash',
        contents=f"Summarize the following YouTube transcript with key takeaways:\n\n{transcript_text}"
    )
    return response.text


if youtube_url:
    video_id = extract_video_id(youtube_url)
    if video_id:
        st.image(f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg", width=400)
        if st.button("Generate Summary"):
            with st.spinner("Processing..."):
                try:
                    transcript = get_transcript(video_id)
                    summary = summarize_transcript(transcript)
                    st.subheader("Summary")
                    st.write(summary)
                except Exception as e:
                    st.error(str(e))
    else:
        st.error("Invalid YouTube URL.")