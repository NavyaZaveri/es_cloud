import hashlib
from textblob import TextBlob


class Post:
    DOC_TYPE = "post"

    def __init__(self, content, timestamp=None, score=None, url=None, id=None):
        self._score = TextBlob(content).sentiment.polarity if score is None else score
        self._timestamp = timestamp
        self._content = content
        self._url = url

        # posts are uniquely defined by their content.
        self._id = int(hashlib.sha1(self.content.encode("utf-8")).hexdigest(), 16) % (10 ** 8) if not id else id

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

    @property
    def url(self):
        return self._url

    def __eq__(self, other):
        return isinstance(other, Post) and self.id == other.id

    def __str__(self):
        return str(self.to_dict())

    def to_dict(self):
        return {
            "content": self.content,
            "timestamp": self.timestamp,
            "id": self.id,
            "score": self.score,
            "url": self.url
        }

    def __hash__(self):
        return self.id


class PostList:
    """
    A simple datatype wrapping a native list of posts, with a custom __hash__ function.
    This is exploited to cache results using @lru_cache.

    """

    def __init__(self, posts=[]):
        self.posts = posts
        all_content = sorted("#".join(post["content"] for post in self.posts))
        self.id = int(hashlib.sha1(str(all_content).encode("utf-8")).hexdigest(), 16) % (10 ** 8)

    def __eq__(self, other):
        return isinstance(other, PostList) and self.id == other.id

    def add(self, post):
        self.posts.append(post)

    def pop(self):
        self.posts.pop()

    def __hash__(self):
        return self.id

    def __str__(self):
        return str(self.posts)

    @classmethod
    def from_raw_list(cls, native_post_list):
        return cls(native_post_list)

    def to_raw_list(self):
        return [p for p in self.posts]
