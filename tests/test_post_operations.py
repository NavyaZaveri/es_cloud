import unittest

from post_datatypes.post import Post, PostList


class TestPostOperation(unittest.TestCase):
    def test_post_container_hash_function(self):
        """
        It is crucial that hash function for the Post List container is defined correctly
        for the @lru cache to work, offering signifcant speed gains
        """

        p1 = Post(content="hello world", timestamp="0")
        p2 = Post(content="hello world", timestamp="0")
        p3 = Post(content="hello worlds", timestamp="0")

        plist_1 = PostList([p1, p2])
        plist_2 = PostList([p1, p2])
        plist_3 = PostList([p1, p3])
        self.assertEqual(plist_1, plist_2, msg="Hash function on Post List not defined correctly")
        self.assertNotEqual(plist_1, plist_3, msg="Hash function on Post List not defined correctly.")

    def test_post_median(self):
        """
        """
        p1 = Post(content="hello world", timestamp="0", score=1)
        p2 = Post(content="hello world", timestamp="0", score=2)
        p3 = Post(content="hello worlds", timestamp="0", score=3)
