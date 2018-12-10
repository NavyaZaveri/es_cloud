import unittest
from flask import json
from test_app import app


class TestEsApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def testIfApiIsUp(self):
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)

        print("testIfApiIsUp() passed")

    def testFindRelevantPosts(self):
        # valid query
        res = self.app.get("/query", query_string={"literal_query": "blah", "limit": 20, "strategy": "fuzzy"})
        self.assertEqual(res.status_code, 200)

        print("testFindRelevantPosts passed")

    def testInvalidParm(self):
        # doesn't contain the query
        res = self.app.get("/query", query_string={"limit": 20})

        self.assertEqual(res.status_code, 400)
        print("Invalid Param tests passed")

    def testInsertAndDelete(self):
        res = self.app.post("/insert",
                            data=json.dumps({"post": {"url": "blah", "score": 1, "content": "blah", "id": 100}}),
                            content_type="application/json")

        self.assertEqual(res.status_code, 201)
        self.app.post("/delete", data=json.dumps({"id": 100}),
                      content_type="application/json")

        print("insert + delete tests passed")

    def testEverything(self):
        self.app.post("/insert",
                      data=json.dumps({"post": {"content": "scala is great", "score": 1, "url": "blah", "id": 100}}),
                      content_type="application/json")

        # uses fuzzy matching by default (thus the explicit typo)
        res = self.app.get("/query", query_string={"literal_query": "scala"})

        # there should more than 1 match
        self.assertTrue(len(res.get_json()["result"]) >= 1)
        print(res.get_json()["result"])

        res = self.app.post("/delete", data=json.dumps({"id": 100}))

        # post deleted, everything's fine
        self.assertTrue(res.status_code, 201)
