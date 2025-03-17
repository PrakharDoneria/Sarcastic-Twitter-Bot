import os
import tweepy
import google.generativeai as genai

# Twitter API Authentication
client = tweepy.Client(
    bearer_token=os.getenv("TWITTER_BEARER_TOKEN"),
    consumer_key=os.getenv("TWITTER_API_KEY"),
    consumer_secret=os.getenv("TWITTER_API_SECRET"),
    access_token=os.getenv("TWITTER_ACCESS_TOKEN"),
    access_token_secret=os.getenv("TWITTER_ACCESS_SECRET")
)

# Gemini API Configuration
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    generation_config={
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 280,
        "response_mime_type": "text/plain",
    },
    system_instruction=(
        "You are a Twitter bot. Your job is to post tweets tagging @dev__nocap and remember tweet character limit in mind "
        "and mildly trolling him for his addiction to rapper KRSNA. Use sarcasm in a "
        "funny, playful manner. Incorporate KRSNA’s music lyrics to mock his obsession, "
        "wrapping the trolling lines within the lyrics of KRSNA's tracks. Keep the tweet "
        "within Twitter’s character limit. The tone should be sarcastic, playful, and lighthearted, "
        "using KRSNA's lyrics to make fun of @dev__nocap in a lyrical format. Make him laugh, cry, and get triggered all at once."
    ),
)

def generate_tweet():
    try:
        chat_session = model.start_chat(history=[])
        response = chat_session.send_message("Generate a funny, sarcastic, and engaging tweet mocking @dev__nocap for his obsession with KRSNA's music.")
        return f"@dev__nocap {response.text.strip()}"
    except Exception as e:
        print(f"Error generating tweet: {e}")
        return {"status": "error", "message": f"Gemini API error: {str(e)}"}

def post_tweet():
    """Posts a tweet using the generated content."""
    tweet_text = generate_tweet()
    
    if isinstance(tweet_text, dict) and tweet_text.get("status") == "error":
        return tweet_text  # Return the Gemini error response if tweet generation failed

    try:
        client.create_tweet(text=tweet_text)
        print(f"Tweeted: {tweet_text}")
        return {"status": "success", "tweet": tweet_text}
    except tweepy.TweepyException as e:
        print(f"Error posting tweet: {e}")
        return {"status": "error", "message": f"Twitter API error: {str(e)}"}

if __name__ == "__main__":
    response = post_tweet()
    print(response)
