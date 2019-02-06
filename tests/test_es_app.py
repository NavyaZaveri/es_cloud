"""
unittests on a local instance of the elastic search rest api
(see localhost_app.py)
"""
import time
import unittest
from flask import json
import es_api
from post_datatypes import Post


class TestEsApp(unittest.TestCase):
    def setUp(self):
        self.app = es_api.create_app("TESTING").test_client()

    def tearDown(self):
        pass

    def testIfApiIsUp(self):
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)

    def testStatusCodeWhenSearchingPosts(self):
        # valid query
        res = self.app.get("/search", query_string={"literal_query": "blah", "limit": 20, "strategy": "fuzzy"})
        self.assertEqual(res.status_code, 200)

    def testInvalidParametersPassedToSearch(self):
        # doesn't contain the query
        res = self.app.get("/search", query_string={"limit": 20})

        self.assertEqual(res.status_code, 400)

    def testInsertAndDelete(self):
        res = self.app.post("/insert",
                            data=json.dumps(
                                {"post": {"url": "blah", "score": 1, "content": "blah", "id": 10, "timestamp": 0}}),
                            content_type="application/json")

        self.assertEqual(res.status_code, 201)
        res = self.app.get("/search", query_string={"literal_query": "blah"})

        res = self.app.post("/delete", data=json.dumps({"id": 10}),
                            content_type="application/json")

        self.assertEqual(res.status_code, 201)

    def testMedian(self):
        p1 = Post(content="foobar", timestamp="0", score=1).to_dict()
        p2 = Post(content="foobar1", timestamp="0", score=2).to_dict()
        p3 = Post(content="foobar2", timestamp="0", score=3).to_dict()

        self.app.post("/insert", data=json.dumps({"post": p1}), content_type="application/json")
        self.app.post("/insert", data=json.dumps({"post": p2}), content_type="application/json")
        self.app.post("/insert", data=json.dumps({"post": p3}), content_type="application/json")
        time.sleep(2)
        result = self.app.get("/median", query_string={"framework": "foobar"}).get_json()

        # clean up
        self.app.post("/delete", data=json.dumps({"id": p1["id"]}), content_type="application/json")
        self.app.post("/delete", data=json.dumps({"id": p2["id"]}), content_type="application/json")
        self.app.post("/delete", data=json.dumps({"id": p3["id"]}), content_type="application/json")

        self.assertTrue(result == {"0": 2})
