import time
import unittest

from es_wrapper import EsWrapper, PostList
from post_datatypes import Post


class TestEsWrapper(unittest.TestCase):
    def setUp(self):
        """"
         sets up a client connected to the localhost
         by default
         """
        self.client = EsWrapper()

    def testPostInsertion(self):
        post = Post(content="foo bar", timestamp="1").to_dict()
        self.client.insert_post(post)

        # for some reason, the elastic search inverted index isn't atomic; thus, the sleep() invocation
        # mitigates against  race conditions.
        # but still need to investigate why es isn't atomic...
        time.sleep(1)

        # fuzzy matching on by default
        posts = self.client.find_posts_on("foo")
        self.assertTrue(len(posts) == 1)

    def tearDown(self):
        self.client.delete_index()

    def testMedianProcessing(self):
        """
        let's create a bunch of posts about a framework, foobar
        """
        p1 = Post(content="tflow1", timestamp="0", score=0.1).to_dict()
        p2 = Post(content="tflow2", timestamp="0", score=0.5).to_dict()
        p3 = Post(content="tflow3", timestamp="0", score=1.0).to_dict()
        p4 = Post(content="tflow4", timestamp="1", score=0.44).to_dict()

        # insert them all
        self.client.insert_posts(p1, p2, p3, p4)

        time.sleep(1)

        avg_score_at = self.client.find_median_scores_of(framework="tflow")

        self.assertEqual(avg_score_at["0"], 0.5, msg="Median Tests failed")
        self.assertEqual(avg_score_at["1"], 0.44, msg="Median Tests failed")

    def test_cache_hits(self):
        # create a bunch of posts
        p1 = Post(content="tflow1", timestamp="0", score=0.1).to_dict()
        p2 = Post(content="tflow2", timestamp="0", score=0.5).to_dict()
        p3 = Post(content="tflow3", timestamp="1", score=1.0).to_dict()
        self.client.insert_posts(p1, p2, p3)

        # create 3 post containers
        post_list_1 = PostList.from_raw_list([p1, p2, p3])
        post_list_2 = PostList.from_raw_list([p1, p3, p2])
        post_list_3 = PostList.from_raw_list([p1, p2, p3])

        self.client.find_daily_median(post_list_1)
        self.client.find_daily_median(post_list_2)
        self.client.find_daily_median(post_list_3)

        actual_hits = self.client.find_daily_median.cache_info().hits
        expected_hits = 2
        self.assertTrue(actual_hits == expected_hits, msg="test_cache_hits() failed. Check __hash__() on PostList")
