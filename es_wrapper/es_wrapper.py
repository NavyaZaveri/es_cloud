from functools import lru_cache

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from flask import jsonify

from post_datatypes.post import Post, PostList
from post_statistics.average import group_by, median


class EsWrapper:
    def __init__(self, client=None, index="testing", endpoint="http://localhost:9200"):
        self.ES_ENDPOINT = endpoint
        self.index = index
        # connects to localhost by default unless the client is provided
        self.client = Elasticsearch(self.ES_ENDPOINT, ca_serts=False, verify_certs=False) if client is None else client

    def insert_post(self, post):
        if isinstance(post, Post):
            self.client.index(index=self.index, body=post.to_dict(), id=post.id, doc_type=Post.DOC_TYPE)
        elif isinstance(post, dict):
            self.client.index(index=self.index, body=post, id=post["id"], doc_type=Post.DOC_TYPE)
        else:
            raise ValueError("Post to be inserted is not an object of type Post or Dict")

    def insert_posts(self, *posts):
        for p in posts:
            self.insert_post(p)

    def delete_index(self, index=None):
        """
        If no index is specified, deletes the default index.
        :param index:
        :return: None
        """
        if index is None:
            self.client.indices.delete(self.index)
        else:
            self.client.indices.delete(index)

    def find_posts(self, query, strategy="fuzzy", size=50):
        """
        Find all posts that match against the query searched.
        Fuzzy matching is turned on by default, but we can use exact
        string matching by simply the changing strategy arg to "match"

        :param size:
        :param query (str): what are we searching for
        :param strategy (str): matching strategy
        :return: posts (list): a list of posts (dicts) that are similar to the query, by content
        """
        search = Search(using=self.client)
        search.update_from_dict({"size": size})
        results = search.doc_type(Post.DOC_TYPE).query(strategy, content=query).execute()
        posts = []
        for hit in results:
            posts.append(hit.to_dict())
        return posts

    @lru_cache(maxsize=128)
    def find_daily_median(self, posts):
        """

        :param posts: A PostList container. It is wrapper around native python list,
        designed specifically to have a __hash___ function  so that the result of this function can be cached
        :return: timestamp_to_medians (dict)
        """
        posts = posts.to_raw_list()
        timestamp_to_medians = {}
        timestamp_to_posts = group_by(posts, attr_selector=lambda x: x["timestamp"])

        for (timestamp, posts) in timestamp_to_posts.items():
            avg = median(posts, key=lambda x: x["score"])
            timestamp_to_medians[timestamp] = avg
        return timestamp_to_medians

    def find_median_scores_of(self, framework):
        """
        Protocol
        (1) We first find  all posts related to this framework
        (2) Then we compute the daily median for each day's worth of scores
        (3) Then return a map, mapping timestamps to medians

        :param: framework_(str)
        :return: timestamp_to_medians (dict)
        """
        max_limit = 10000  # elastic search limit
        relevant_posts = self.find_posts(framework, size=max_limit)
        return self.find_daily_median(PostList.from_raw_list(relevant_posts))
