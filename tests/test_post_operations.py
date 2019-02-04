import unittest
from post_datatypes.post import Post, PostList
from post_statistics.average import group_by, median, mean


class TestPostOperation(unittest.TestCase):
    def test_hash_function_of_post_container(self):
        """
        It is crucial that hash function for the Post List container is defined correctly
        for the @lru cache to work, which would ensure significant performance gains.
        """

        p1 = Post(content="hello world", timestamp="0").to_dict()
        p2 = Post(content="hello world", timestamp="0").to_dict()
        p3 = Post(content="hello worlds", timestamp="0").to_dict()

        plist_1 = PostList([p1, p2])
        plist_2 = PostList([p2, p1])
        plist_3 = PostList([p1, p3])
        set_of_postContainers = set()

        # Posts p1 and p2 are the same.
        # Thus the containers carrying both of these points should also evaluated as equal
        # We don't care about the order of the posts
        set_of_postContainers.add(plist_1)
        set_of_postContainers.add(plist_2)
        self.assertTrue(len(set_of_postContainers) == 1)

        set_of_postContainers.add(plist_3)
        self.assertTrue(len(set_of_postContainers) == 2)
        self.assertNotEqual(p1, p3, msg="Hash function on Post not defined correctly.")

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
