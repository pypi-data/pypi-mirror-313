import tweepy
from airosentris.crawler.tweepy.TweepyCrawlerTwitter import TweepyCrawlerTwitter


class TweepyCrawler:
    def __init__(self, bearer_token):
        self.client = tweepy.Client(bearer_token=bearer_token)
        self.twitterCrawler = TweepyCrawlerTwitter(client=self.client)

    def get_twitter_post(self, username, date, limit):
        result = self.twitterCrawler.get_twitter_post(username, date, limit)
        return result

    def get_twitter_comment(self, post_code, include_reply=True):
        result = self.instagramCrawler.get_twitter_comment(post_code, include_reply)
        return result
