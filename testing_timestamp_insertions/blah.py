import hashlib

import elasticsearch_dsl
from elasticsearch_dsl import Document, Text, Keyword, Date, InnerDoc, Nested, AttrList, CustomField, Integer
from elasticsearch import Elasticsearch
from elasticsearch_dsl.connections import connections
import time
import datetime

"""
Protocol for insertion:
Args: (topic, post)

If the post exists, don't insert (test)

If it doesn't exist, dump it into the index 

Update the framework median 

"""

ES_ENDPOINT = "http://localhost:9200"
client = Elasticsearch(ES_ENDPOINT, ca_serts=False, verify_certs=False)
connections.create_connection(hosts=['localhost'])


class Article(Document):
    content = Text(analyzer='snowball', fields={'raw': Keyword()})

    def save(self, **kwargs):
        return super(Article, self).save(**kwargs)


class Thing(Document):
    content = Text(analyzer='snowball', fields={'raw': Keyword()})

    class Index:
        name = 'blog'
        doc_type = "thing"

    def save(self, **kwargs):
        return super(Thing, self).save(**kwargs)


class Post(Document, InnerDoc):
    content = Text(analyzer='snowball', fields={'raw': Keyword()})

    def save(self, **kwargs):
        print("saving post")
        super(Post, self).save(**kwargs)

    def __hash__(self):
        return hash(self.content)

    class Index:
        name = 'blog'
        doc_type = "post"


class Framework(Document):
    name = Text(analyzer='snowball', fields={'raw': Keyword()})
    posts = Nested(properties={
        Post: Integer
    })

    class Index:
        name = 'blog'
        doc_type = "framework"

    def add_post(self, post):
        self.posts.append(post)

    def save(self, **kwargs):
        print("saving faemworkd")
        super(Framework, self).save(**kwargs)


"""
Article.init()
Thing.init()
Post.init()

thing = Thing(meta={'id': 144653930895353261282233826065192032313}, content='thingies')
article = Article(meta={'id': 114}, content='an article ')
article.save()
thing.save()
print("saving....")
time.sleep(2)

ubq = Thing.search(using=client).query("fuzzy", content="thingie")  # change 1st arg to fuzzy
# ubq = Article.search(using=client).query("fuzzy", content="stuffie")  # change 1st arg to fuzzy

res = ubq.execute()
for i in res:
    print("first")
    print(i.content)
    i.update(content="goofball")
time.sleep(2)
ubq = Thing.search(using=client).query("fuzzy", content="goofball")  # change 1st arg to fuzzy
res = ubq.execute()
for i in res:
    print("second")
    print(i.content)
"""

Framework.init()
Post.init()
p = Post(meta={'id': 99}, content="cool beans ")
f = Framework(meta={'id': 100}, name="kotlin")
p.save()
f.save()
time.sleep(2)

res = Post.search(using=client).query("fuzzy", content="cool").execute()
for p in res:
    print(p)
    f_search = Framework.search(using=client).query("fuzzy", name="kotlin").execute()
    for f in f_search:
        print(f)
        f.add_post({p: 1})
        f.save()

Post.update()

f = Framework(meta={'id': 300}, name="python")
f.save()
print("saving famework")
time.sleep(2)
f_search = Framework.search(using=client).query("fuzzy", name="Kotlin").execute()
time.sleep(2)
for f in f_search:
    print(f)
    print(f.posts[0].content)

es = Elasticsearch()
es.indices.delete(index='blog', ignore=[400, 404])
client.index

