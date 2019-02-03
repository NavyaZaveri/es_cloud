from functools import lru_cache

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search

from post_datatypes.post import Post, PostList
from post_statistics.average import group_by, median


class EsWrapper:
    def __init__(self, client=None, index="testing"):
        self.ES_ENDPOINT = "http://localhost:9200"
        self.index = index

        # connects to localhost by default unless the client is provided
        self.client = Elasticsearch(self.ES_ENDPOINT, ca_serts=False, verify_certs=False) if client is None else client
        self.index = "testing"

    def insert_post(self, post):
        res = self.client.index(index=self.index, body=post.to_dict(), doc_type=post.DOC_TYPE, id=post.id)

    def insert_posts(self, *posts):
        for p in posts:
            self.insert_post(p)

    def delete_index(self, index=None):
        """
        If no index is specified, deletes the default index.
        :param index:
        :return:
        """
        if index is None:
            self.client.indices.delete(self.index)
        else:
            self.client.indices.delete(index)

    def find_posts_by_content(self, query, strategy="fuzzy"):
        results = Search(using=self.client).doc_type(Post.DOC_TYPE).query(strategy, content=query).execute()
        posts = []
        for p in results:
            posts.append(p)
        return posts

    @lru_cache(maxsize=128)
    def find_daily_median(self, posts):
        """

        :param posts: A PostList container. It is wrapper around native python list,
        designed specifically to have a __hash___ function  so that the result of this function can be cached
        :return: timestamp_to+medians
        """
        posts = posts.to_raw_list()
        timestamp_to_medians = {}
        timestamp_to_posts = group_by(posts, attr_selector=lambda x: x.timestamp)
        for (timestamp, posts) in timestamp_to_posts.items():
            avg = median(posts, key=lambda x: x.score)
            timestamp_to_medians[timestamp] = avg
        return timestamp_to_medians

    def find_median_scores_of(self, framework):
        """
        Protocol
        (1) We first find  all posts related to this framework
        (2) Then we compute the daily median for each day's worth of scores
        (3) Then return a map, mapping timestamps to medians

        :param framework_name (str)
        :return: timestamp_to_medians (dict)
        """
        relevant_posts = self.find_posts_by_content(framework)

        return self.find_daily_median(PostList.from_raw_list(relevant_posts))
