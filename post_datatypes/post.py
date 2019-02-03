import hashlib
from collections import defaultdict

from textblob import TextBlob


class Post:
    DOC_TYPE = "post"

    def __init__(self, content, timestamp=None, score=None):
        self._score = TextBlob(content).sentiment.polarity if score is None else score
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

    def __eq__(self, other):
        return self._id == other.id

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
        return all([p1 == p2 for p1, p2 in zip(self.posts, other.posts)])

    def add(self, post):
        self.posts.append(post)

    def pop(self):
        self.posts.pop()

    def __hash__(self):
        all_content = "".join(content for content in self.posts)
        print(all_content)
        return int(hashlib.sha1(str(all_content).encode("utf-8")).hexdigest(), 16) % (10 ** 8)

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
