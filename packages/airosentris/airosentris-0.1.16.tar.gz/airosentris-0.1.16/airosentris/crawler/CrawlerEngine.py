import os
from dotenv import load_dotenv
from airosentris.crawler.apify.ApifyCrawler import ApifyCrawler
from airosentris.crawler.tweepy.TweepyCrawler import TweepyCrawler

load_dotenv()


class CrawlerEngine:
    _instances = {}

    def __init__(self, method: str = 'apify', apify_token: str = None, twitter_bearer_token: str = None):
        self.method = method
        self.apify_token = apify_token or os.getenv('APIFY_TOKEN')
        self.twitter_bearer_token = twitter_bearer_token or os.getenv('TWITTER_BEARER_TOKEN')

        if not self.apify_token and method == 'apify':
            raise ValueError("APIFY_TOKEN is required for ApifyCrawler.")
        if not self.twitter_bearer_token and method == 'tweepy':
            raise ValueError("TWITTER_BEARER_TOKEN is required for TweepyCrawler.")

        self.crawler = self._get_or_create_instance(method)

    def _get_or_create_instance(self, method: str):
        if method not in self._instances:
            if method == 'apify':
                self._instances[method] = ApifyCrawler(self.apify_token)
            elif method == 'tweepy':
                self._instances[method] = TweepyCrawler(bearer_token=self.twitter_bearer_token)
            elif method == 'graphapi':
                raise NotImplementedError("GraphAPI method is not implemented yet.")
            elif method == 'instaloader':
                raise NotImplementedError("Instaloader method is not implemented yet.")
            elif method == 'selenium':
                raise NotImplementedError("Selenium method is not implemented yet.")
            else:
                raise ValueError(f"Unsupported crawling method: {method}")
        return self._instances[method]

    def change_method(self, method: str):
        """Change the crawling method dynamically."""
        self.method = method
        self.crawler = self._get_or_create_instance(method)

    def get_instagram_post(self, username: str, date: str, limit: int):
        """
        Retrieves Instagram posts for a given username.

        Parameters:
        username (str): The Instagram username to fetch posts for.
        date (str): The date to filter posts.
        limit (int): The maximum number of posts to retrieve.

        Returns:
        list: A list of Instagram posts.
        """
        return self.crawler.get_instagram_post(username, date, limit)

    def get_instagram_comment(self, post_short_code: str, include_reply: bool):
        """
        Retrieves comments for a given Instagram post.

        Parameters:
        post_short_code (str): The short code of the Instagram post.
        include_reply (bool): Whether to include replies to comments.

        Returns:
        list: A list of Instagram comments.
        """
        return self.crawler.get_instagram_comment(post_short_code, include_reply)

    def get_twitter_post(self, username: str, date: str, limit: int):
        """
        Retrieves Twitter posts for a given username.

        Parameters:
        username (str): The Twitter username to fetch posts for.
        date (str): The date to filter posts.
        limit (int): The maximum number of posts to retrieve.

        Returns:
        list: A list of Twitter posts.
        """
        return self.crawler.get_twitter_post(username, date, limit)
