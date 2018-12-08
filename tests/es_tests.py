import unittest
from app import app


class TestEsApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def testIfApiIsUp(self):
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)

    def testGetMethodforFindingPosts(self):
        res = self.app.get("/query", query_string={"literal_query": "blwf", "limit": 20, "strategy": "fuzzy"})
        self.assertEqual(res.status_code, 200)
