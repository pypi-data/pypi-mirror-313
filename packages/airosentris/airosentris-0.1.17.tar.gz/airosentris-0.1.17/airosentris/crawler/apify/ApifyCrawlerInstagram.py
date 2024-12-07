from datetime import datetime
import logging


class ApifyCrawlerInstagram:

    def __init__(self, client):
        self.client = client
        self.actor_instagram_post = 'shu8hvrXbJbY3Eb9W'
        self.action_instagram_comment = 'SbK00X0JYCPblD2wp'

    def _run_instagram_post_input(self, username, date_str, limit):
        # Run the Actor and wait for it to finish
        run_input = {
            "directUrls": ["https://www.instagram.com/" + username + "/"],
            "resultsType": "posts",
            "resultsLimit": limit,
        }

        if date_str is not None:
            run_input["onlyPostsNewerThan"] = date_str

        # Run the Actor and wait for it to finish
        run = self.client.actor(self.actor_instagram_post).call(run_input=run_input)

        return run["defaultDatasetId"]

    def get_instagram_post(self, username, date_str, limit):
        """
        Fetches Instagram posts for a given username from a specific date onwards.

        :param username: Instagram username whose posts are to be fetched
        :param date_str: Start date in 'YYYY-MM-DD' format (optional)
        :param limit: Limit on the number of posts to fetch (optional)
        :return: Dictionary with keys: 'success', 'data', 'message'
        """

        dataset_id = self._run_instagram_post_input(username, date_str, limit)
        # dataset_id = 'VbsLRXSQURJz5aWYs'

        # Fetch and print Actor results from the run's dataset (if there are any)
        result = []

        for post in self.client.dataset(dataset_id).iterate_items():
            try:
                if post['timestamp'] is None:
                    raise Exception("Timestamp is null")

                dt = datetime.strptime(post['timestamp'], '%Y-%m-%dT%H:%M:%S.%fZ')
                post_info = {
                    "platform_code": "instagram",
                    "platform_internal_id": post['shortCode'],
                    "title": None,
                    "post_date": dt.strftime('%Y-%m-%d %H:%M:%S'),
                    "caption": post['caption'],
                    "source_url": "https://instagram.com/p/" + post['shortCode'],
                    "comments_count": post['commentsCount'],
                    "likes_count": post['likesCount']
                }

                result.append(post_info)
            except Exception as e:
                print(e)

        return result

    def _run_instagram_comment_input(self, post_short_code, include_reply=True):
        # Run the Actor and wait for it to finish
        run_input = {
            "directUrls": ["https://www.instagram.com/p/" + post_short_code + "/"],
        }

        # Run the Actor and wait for it to finish
        run = self.client.actor(self.action_instagram_comment).call(run_input=run_input)

        return run["defaultDatasetId"]

    def get_instagram_comment(self, post_short_code, include_reply=True):
        """
        Fetches comments and their replies for a given Instagram post shortcode.

        :param post_short_code: The shortcode of the Instagram post
        :param include_reply: Include replies of Instagram comments (default: True)
        :return: Dictionary with keys: 'success', 'data', 'message'
        """

        dataset_id = self._run_instagram_comment_input(post_short_code, include_reply)
        # dataset_id = 'j4dduVWmz7SUCtjqf'
        comments = []
        print(f"Dataset ID : {dataset_id}")

        for comment in self.client.dataset(dataset_id).iterate_items():
            dt = datetime.strptime(comment['timestamp'], '%Y-%m-%dT%H:%M:%S.%fZ')

            comment_info = {
                "platform_post_id": post_short_code,
                "platform_comment_id": comment['id'],
                "platform_user_id": None,
                "platform_username": comment['ownerUsername'],
                "comment_text": comment['text'],
                "comment_date": dt.strftime('%Y-%m-%d %H:%M:%S'),
                "profile_pic": comment['ownerProfilePicUrl'],
                "likes_count": comment['likesCount'],
                'total_reply': 0,
                'owner_reply': False,
                'is_replied': False,
                "replies": []
            }

            comments.append(comment_info)

        print(f"Total Comments : {len(comments)}")

        # Function to parse date from string
        def parse_date(date_str):
            return datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')

        if len(comments) == 0:
            return []

        # Sort comments by date first
        comments.sort(key=lambda x: parse_date(x['comment_date']))

        # Relate comments and replies, and set additional properties
        for comment in comments:
            for reply in comments:
                # Check if the reply is directed at the original commenter
                if reply['platform_username'] == 'pdamsuryasembada' \
                        and comment['platform_username'] in reply['comment_text']:
                    # Check if the reply was made after the comment
                    if parse_date(reply['comment_date']) > parse_date(comment['comment_date']):
                        comment['replies'].append(reply)
                        comment['total_reply'] += 1
                        comment['is_replied'] = True
                        if reply['platform_username'] == 'pdamsuryasembada':
                            comment['owner_reply'] = True

        # Filter out comments that are actually replies
        reply_ids = {reply['platform_comment_id'] for comment in comments for reply in comment['replies']}
        final_comments = [comment for comment in comments if comment['platform_comment_id'] not in reply_ids]

        logging.info(f"Fetched {len(comments)} comments for post {post_short_code}")

        return final_comments
