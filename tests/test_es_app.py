"""
unittests on a local instance of the elastic search rest api
(see localhost_app.py)
"""

import unittest
from flask import json
import es_api


class TestEsApp(unittest.TestCase):
    def setUp(self):
        self.app = es_api.create_app("TESTING").test_client()

    def testIfApiIsUp(self):
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)

        print("testIfApiIsUp() passed")

    def testFindRelevantPosts(self):
        # valid query
        res = self.app.get("/search", query_string={"literal_query": "blah", "limit": 20, "strategy": "fuzzy"})
        self.assertEqual(res.status_code, 200)

        print("testFindRelevantPosts passed")

    def testInvalidParm(self):
        # doesn't contain the query
        res = self.app.get("/search", query_string={"limit": 20})

        self.assertEqual(res.status_code, 400)
        print("Invalid Param tests passed")

    def testInsertAndDelete(self):
        res = self.app.post("/insert",
                            data=json.dumps({"post": {"url": "blah", "score": 1, "content": "blah", "id": 10}}),
                            content_type="application/json")
        res = self.app.post("/insert",
                            data=json.dumps({"post": {"url": "blah", "score": 1, "content": "foobar", "id": 200}}),
                            content_type="application/json")

        self.assertEqual(res.status_code, 201)
        res = self.app.get("/search", query_string={"literal_query": "blah"})
        print(res.get_json())

        res = self.app.post("/delete", data=json.dumps({"id": 10}),
                            content_type="application/json")

        self.assertEqual(res.status_code, 201)

        print("testInsertAndDelete() passed")
