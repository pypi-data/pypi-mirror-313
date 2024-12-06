import tweepy
import datetime
import time


class TweepyCrawlerTwitter:

    def __init__(self, client):
        self.client = client

    def get_twitter_post(self, username, date_str, limit, retries=3, delay=5):
        attempt = 0
        while attempt < retries:
            try:
                # Get user ID from the username
                user = self.client.get_user(username=username)
                user_id = user.data.id
                print(f"User ID for {username}: {user_id}")

                # Convert date_str to the required format (ISO 8601 with time)
                since_date = datetime.strptime(date_str, '%Y-%m-%d').isoformat() + 'Z'

                # Fetch the tweets after the specific date with a limit
                response = self.client.get_users_tweets(
                    id=user_id,
                    start_time=since_date,
                    max_results=limit,
                    tweet_fields=['created_at']
                )

                # Handle the response and print the tweets
                if response.data:
                    for tweet in response.data:
                        print(f"Tweet ID: {tweet.id} | Created at: {tweet.created_at} | Text: {tweet.text}")
                else:
                    print(f"No tweets found for {username} after {date_str}")

                break  # Exit the loop if the request was successful

            except tweepy.errors.TwitterServerError as e:
                print(f"TwitterServerError: {e}. Retrying in {delay} seconds...")
                attempt += 1
                time.sleep(delay)

        if attempt == retries:
            print("Failed to fetch tweets after multiple attempts.")

