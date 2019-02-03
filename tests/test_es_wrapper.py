import time
import unittest

from es_wrapper import EsWrapper
from post_datatypes import Post


class TestEsWrapper(unittest.TestCase):
    def setUp(self):
        """"
         sets up a client connected to the localhost
         by default
         """
        self.client = EsWrapper()

    def testPostInsertion(self):
        post = Post(content="foo bar", timestamp="1")
        self.client.insert_post(post)

        # weirdly the elastic search inverted index isn't atomic, so the sleep() prevents any  race conditions
        # still need to investigate...
        time.sleep(1)

        # fuzzy matching on by default
        posts = self.client.find_posts_by_content("foo")
        self.assertTrue(len(posts) == 1)

    def tearDown(self):
        self.client.delete_index()

    def testMedianProcessing(self):
        p1 = Post(content="foobar 1", timestamp="0", score=0.1)
        p2 = Post(content="foobar 2", timestamp="0", score=0.5)
        p3 = Post(content="foobar 3", timestamp="0", score=1.0)
        p4 = Post(content="foobar 4", timestamp="1", score=0.44)

        self.client.insert_posts(p1, p2, p3, p4)

        time.sleep(1)

        avg_score_at = self.client.find_median_scores_of(framework="foobar")

        self.assertEqual(avg_score_at["0"], 0.5, msg="Median Tests failed")
        self.assertEqual(avg_score_at["1"], 0.44, msg="Median Tests failed")
