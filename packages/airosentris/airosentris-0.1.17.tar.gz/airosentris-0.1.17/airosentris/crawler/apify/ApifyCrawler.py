from apify_client import ApifyClient
from airosentris.crawler.apify.ApifyCrawlerInstagram import ApifyCrawlerInstagram


class ApifyCrawler:
    def __init__(self, token):
        self.client = ApifyClient(token)
        self.instagramCrawler = ApifyCrawlerInstagram(client=self.client)

    def get_instagram_post(self, username, date, limit):
        result = self.instagramCrawler.get_instagram_post(username, date, limit)
        return result

    def get_instagram_comment(self, post_short_code, include_reply=True):
        result = self.instagramCrawler.get_instagram_comment(post_short_code, include_reply)
        return result
