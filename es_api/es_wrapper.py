from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search

from post_datatypes import post
from post_datatypes.post import Post


class EsWrapper:
    def __init__(self, client=None, index=None):
        self.ES_ENDPOINT = "http://localhost:9200"

        # connects to localhost by default unless the client is provided
        self.client = Elasticsearch(self.ES_ENDPOINT, ca_serts=False, verify_certs=False) if client is None else client
        self.index = "testing"

    def insert_post(self, post):
        res = self.client.index(index=self.index, body=post.to_dict(), doc_type=post.DOC_TYPE, id=post.id)
        print(res)

    def delete_index(self, index=None):
        """
        If no index is specified, deletes the default index.
        :param index:
        :return:
        """
        if index is None:
            self.client.indices.delete(self.index)
        else:
            self.client.indices.delete(index)

    def find_posts_by_content(self, query, strategy="fuzzy"):
        results = Search(using=self.client).doc_type(Post.DOC_TYPE).query(strategy, content=query).execute()
        posts = []
        for p in results:
            posts.append(p)
        return posts
