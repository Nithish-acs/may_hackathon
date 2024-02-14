# app.py
from flask import Flask, render_template, request, jsonify
import openai
from urllib.parse import parse_qs, urlparse
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        video_url = request.form.get('videoURL')

        # Call YouTube API to get subtitles (you need to implement this)
        subtitles = get_subtitles(video_url)
        print("subtitles", subtitles)

        # Combine subtitles into a single string
        text_summary = ' '.join(subtitles)

        # Call ChatGPT API for text summarization (you need to implement this)
        audio_summary = summarize_text(text_summary)

        # Convert text summary to audio (you need to implement this)
        base64_audio = text_to_speech(audio_summary)

        # Create summary video (you need to implement this)
        base64_video = create_summary_video(video_url)

        return jsonify({'base64Video': base64_video, 'base64Audio': base64_audio})

    return render_template('index.html')

def get_subtitles(video_url):
    parsed_url = urlparse(video_url)
    query_parameters = parse_qs(parsed_url.query)

    video_id = query_parameters.get('v', [''])[0]

    print("Extracted Video ID:", video_id)

    if not video_id:
        # Handle the case where video ID is not found
        return []

    # Make a Google API call to get captions (replace YOUR_GOOGLE_API_KEY with your actual API key)
    google_api_key = 'AIzaSyC9qrDd7hMWinffcA78WmqlYQq9cm8NzRQ'
    captions_url = f'https://www.googleapis.com/youtube/v3/captions?part=snippet&videoId={video_id}&key={google_api_key}'
    
    try:
        response = requests.get(captions_url)
        response.raise_for_status()
        captions_data = response.json()

        # Extract captions from the response (modify this based on the actual response structure)
        subtitles = [item['snippet']['textOriginal'] for item in captions_data.get('items', [])]

        print("Generated Subtitles:")
        for subtitle in subtitles:
            print(subtitle)

        # return subtitles
        return ["hackathon", "guidlines"]

    except requests.exceptions.RequestException as e:
        # Handle API request errors
        print(f"Error fetching captions: {e}")
        print(f"Response content: {response.content if 'response' in locals() else ''}")
        return ["hackathon", "guidlines"]
        # return []


def summarize_text(text):
    openai.api_key = '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'

    try:
        # Make the ChatGPT API call for text summarization
        response = openai.Completion.create(
            engine="text-davinci-003",  # Choose the appropriate engine
            prompt=text,
            max_tokens=150,  # Adjust as needed
            temperature=0.7,  # Adjust as needed
        )

        # Extract the generated summary from the API response
        summary = response.choices[0].text.strip()
        print("Generated Summary:", summary)
        
        return summary

    except Exception as e:
        # Handle API request errors
        print(f"Error summarizing text: {e}")
        return None

def text_to_speech(text):
    # Implement text-to-speech conversion
    # Return the base64-encoded audio
    pass

def create_summary_video(video_url):
    # Implement video processing to create a summary video
    # Return the base64-encoded video
    pass

if __name__ == '__main__':
    app.run(debug=True)
