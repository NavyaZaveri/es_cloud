import hashlib
import json
from functools import lru_cache
from textblob import TextBlob
import elasticsearch
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from collections import defaultdict


class Post:
    DOC_TYPE = "post"

    def __init__(self, content, timestamp=None):
        self._score = TextBlob(content).sentiment.polarity
        self._timestamp = timestamp
        self._content = content

        # posts are uniquely defined by their content.
        self._id = int(hashlib.sha1(self.content.encode("utf-8")).hexdigest(), 16) % (10 ** 8)

    @property
    def score(self):
        return self._score

    @property
    def timestamp(self):
        return self._timestamp

    @property
    def content(self):
        return self._content

    @property
    def id(self):
        return self._id

    def __str__(self):
        return "{content = {}, score = {}, timestamp = {}, id = {}}".format(self.content,
                                                                            self.score, self.timestamp, self.id)

    def to_dict(self):
        return {
            "content": self.content,
            "timestamp": self.timestamp,
            "id": self.id,
            "score": self.score
        }

    def __hash__(self):
        return self.id


class PostList:
    """
    A simple datatype wrapping a native list of posts, with a custom __hash__ function.
    This is exploited to cache results using @lru_cache

    The implementation is flexible enough that the constructor arg,  posts, can be a a list of Post Objects,
    or a list of dict (with attributes of a Post object)


    """

    def __init__(self, posts=[]):
        self.posts = posts

    def __eq__(self, other):
        return self.posts == other.posts

    def add(self, post):
        self.posts.append(post)

    def pop(self):
        self.posts.pop()

    def __hash__(self):
        return int(hashlib.sha1(str(self.posts).encode("utf-8")).hexdigest(), 16) % (10 ** 8)

    def __str__(self):
        return str(self.posts)

    def group_by(self, post_attr_selector):
        attribute_to_posts = defaultdict(list)
        for post in self.posts:
            attribute_to_posts[post_attr_selector(post)].append(post)
        return attribute_to_posts

    @classmethod
    def from_raw_list(cls, native_post_list):
        return cls(native_post_list)

    def to_raw_list(self):
        return [p for p in self.posts]


class EsWrapper:
    def __init__(self, client=None, index=None):
        self.ES_ENDPOINT = "http://localhost:9200"

        # connects to localhost by default unless the client is provided
        self.client = Elasticsearch(self.ES_ENDPOINT, ca_serts=False, verify_certs=False) if client is None else client
        self.index = "testing"

    def insert_post(self, post):
        res = self.client.index(index=self.index, body=post.to_dict(), doc_type=post.DOC_TYPE, id=post.id)
        print(res)

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
