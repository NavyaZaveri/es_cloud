"""
A REST api hosted on that acts as a wrapper around
the elastic-search dl library
"""

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from elasticsearch_dsl.query import MultiMatch
from flask import Flask, json, request, jsonify
import post_utils

app = Flask(__name__)
client = None
TESTING = False

if not TESTING:
    app.config.from_object("config.ProductionConfig")
    client = Elasticsearch(app.config.get("ES_ENDPOINT"),
                           http_auth=(app.config.get("ES_USERNAME"), app.config.get("ES_PASSWORD")))
else:
    app.config.from_object("config.TestingConfig")
    client = Elasticsearch(app.config.get("ES_ENDPOINT"), ca_serts=False, verify_certs=False)


@app.route("/", methods=["GET"])
def index():
    """
    """

    query = MultiMatch(query="python", fields=['title', 'content'], fuzziness='AUTO')
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
        return jsonify({"result": "invalid query parameters - please set query"}), 400

    query = MultiMatch(query=q, fields=['title', 'content'], fuzziness='AUTO')
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
    repopulate them from the json file

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
        return json.dumps({"result": "missing in json,"
                                     "please make you sure the json has the field 'post'"}), 400

    if not post_utils.is_valid_post(post):
        return jsonify(
            {"result": "missing content/id field in the post,"
                       " please make sure you have them as attributes in your post"}), 400

    # inserts a post
    client.index("es_docs", "doc", post, id=post["id"])

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
    deletes a post given an id
    """
    json_id = request.get_json()
    if json_id is None:
        return jsonify(
            {"result": "json content not received. Please make sure you send json,"
                       " with content_type='application/json'"}), 400

    id_to_be_deleted = json_id["id"]
    client.delete(index="es_docs", doc_type="doc", id=id_to_be_deleted)
    return "ok", 201


if __name__ == "__main__":
    app.run()
