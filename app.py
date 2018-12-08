from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from elasticsearch_dsl.query import MultiMatch
from flask import Flask, json, request
import post_utils

app = Flask(__name__)
client = None
TESTING = True

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
    print(response)
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
        return json.dumps({"result": "invalid query paramaters - please set query"}), 400

    query = MultiMatch(query=q, fields=['title', 'content'], fuzziness='AUTO')
    s = Search(using=client).query(query)

    response = s.execute()
    for hit in response:
        print(hit.content)
        print(hit.score)

    return json.dumps({"result": "success"}), 200


@app.route("/repopulate", methods=["POST"])
def populate_es_database():
    """
    delete all existing documents and
    repopulate them from the json file

    """
    # check if the post request has the file part
    if "file" not in request.files:
        return json.dumps({"result": "please send a json file"}), 400

    file = request.files["file"]
    print(file)
    return "ok"


if __name__ == "__main__":
    app.run()
