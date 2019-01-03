"""
A REST api hosted on heroku, acting as a wrapper around
the elastic-search dl library.
"""

import re
import es_api
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from elasticsearch_dsl.query import MultiMatch
from flask import Flask, json, request, jsonify

import post_utils

app = es_api.create_app("PRODUCTION")
''''
app = Flask(__name__)
app.config.from_object("config.ProductionConfig")

bonsai = app.config.get("ES_ENDPOINT")
auth = re.search('https\:\/\/(.*)\@', bonsai).group(1).split(':')
host = bonsai.replace('https://%s:%s@' % (auth[0], auth[1]), '')

# Connect to cluster over SSL using auth for best security:
es_header = [{
    'host': host,
    'port': 443,
    'use_ssl': True,
    'http_auth': (auth[0], auth[1])
}]

client = Elasticsearch(es_header)


@app.route("/", methods=["GET"])
def index():
    query = MultiMatch(
        query="python", fields=['title', 'content'], fuzziness='AUTO')
    s = Search(using=client).query(query)
    response = s.execute()
    posts = []
    for hit in response:
        posts.append(post_utils.toPost(hit))
    return json.dumps({"result": posts}), 200


@app.route("/query", methods=["GET"])
def find_posts():
    q = request.args.get("literal_query")
    l = request.args.get("limit")
    s = request.args.get("strategy")
    if not q:
        return jsonify({
            "result": "invalid query parameters - please set query"
        }), 400

    query = MultiMatch(query=q, fields=['content'], fuzziness='AUTO')
    s = Search(using=client).query(query)

    response = s.execute()
    posts = []

    for hit in response:
        posts.append(post_utils.toPost(hit))
    return jsonify({"result": posts}), 200


@app.route("/repopulate", methods=["POST"])
def populate_es_database():
    """
    delete all existing documents and
    repopulate the index with contents
    in the json file

    """
    # check if the post request has the file part
    if "file" not in request.files:
        return jsonify({"result": "please send a json file"}), 400

    file = request.files["file"]

    return "ok"


@app.route("/insert", methods=["POST"])
def insert_post():
    json_post = request.get_json()

    try:
        post = json_post["post"]
    except KeyError:
        return json.dumps({
            "result":
                "key missing in json,"
                "please make you sure the json has the field 'post'"
        }), 400

    if not post_utils.is_valid_post(post):
        return jsonify({
            "result":
                "missing content/id field in the post,"
                " please make sure you have them as attributes in your post"
        }), 400

    # inserts a post
    client.index(app.config.get("INDEX"), "doc", post, id=post["id"])

    return "ok", 201


@app.route("/retrieve", methods=["GET"])
def retrieve_post():
    pass


@app.route("/bulkInsert", methods=["POST"])
def bulk_insert():
    pass


@app.route("/delete", methods=["POST"])
def delete_post():
    """
    deletes a post, given an id
    """
    json_id = request.get_json()
    if json_id is None:
        return jsonify({
            "result":
                "json content not received. Please make sure you send json,"
                " with content_type='application/json'"
        }), 400

    id_to_be_deleted = json_id["id"]
    client.delete(index=app.config.get("INDEX"), doc_type="doc", id=id_to_be_deleted)
    return "ok", 201

'''
if __name__ == "__main__":
    app.run()
