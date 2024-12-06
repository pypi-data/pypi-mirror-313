from airosentris.crawler.httprequest.HttpRequestCrawlerCIS import HttpRequestCrawlerCIS


class HttpRequestCrawler:
    def __init__(self):
        self.cisCrawler = HttpRequestCrawlerCIS()

    def get_cis_comments(self, start, limit):
        return self.cisCrawler.get_cis_comments(start, limit)
    
    def get_last_sequence(self):
        return self.cisCrawler.get_last_sequence()
    
    def post_comments(self, data):
        return self.cisCrawler.post_comments(data)