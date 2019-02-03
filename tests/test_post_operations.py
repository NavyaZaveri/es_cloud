import unittest
from post_datatypes.post import Post, PostList
from post_statistics.average import group_by, median, mean


class TestPostOperation(unittest.TestCase):
    def test_post_container_hash_function(self):
        """
        It is crucial that hash function for the Post List container is defined correctly
        for the @lru cache to work, which would ensure significant performance gains.
        """

        p1 = Post(content="hello world", timestamp="0")
        p2 = Post(content="hello world", timestamp="0")
        p3 = Post(content="hello worlds", timestamp="0")

        plist_1 = PostList([p1, p2])
        plist_2 = PostList([p1, p2])
        plist_3 = PostList([p1, p3])
        post_set = set()

        post_set.add(p1)
        post_set.add(p2)

        self.assertTrue(len(post_set) == 1)
        self.assertEqual(plist_1, plist_2, msg="Hash function on Post List not defined correctly")
        self.assertNotEqual(plist_1, plist_3, msg="Hash function on Post List not defined correctly.")

    def test_post_statistics(self):
        """
        Testing basic operations - mean and median. Both are implemented with numpy for performance gains
        """
        p1 = Post(content="hello world1", timestamp="0", score=1)
        p2 = Post(content="hello world2", timestamp="0", score=2)
        p3 = Post(content="hello world3", timestamp="1", score=3)
        timestamp_to_posts = group_by([p1, p2, p3], lambda x: x.timestamp)

        self.assertEqual(median(timestamp_to_posts["0"], key=lambda x: x.score), 1.5)
        self.assertEqual(mean(timestamp_to_posts["1"], key=lambda x: x.score), 3)
