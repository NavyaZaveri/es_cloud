import unittest
from app import app


class TestEsApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def testIfApiIsUp(self):
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)

    def testGetMethodforFindingPosts(self):
        # valid query
        res = self.app.get("/query", query_string={"literal_query": "blwf", "limit": 20, "strategy": "fuzzy"})
        self.assertEqual(res.status_code, 200)

    def testInvalidParm(self):
        # doesn't contain the query
        res = self.app.get("/query", query_string={"limit": 20})
        self.assertEqual(res.status_code, 400)
