import json
from flask import Blueprint, request, jsonify
import post_utils
from es_wrapper import EsWrapper, Post


def create_blueprint(config):
    """
    :param config: a Config Object with elastic client and index attributes
    :return: a blueprint for the app
    """

    client = config.CLIENT
    index = config.INDEX
    es_blueprint = Blueprint("es_blueprint", __name__)
    es = EsWrapper(client=client, index=index)

    @es_blueprint.route("/", methods=["GET"])
    def home():
        posts = es.find_posts(query="python")
        return json.dumps({"result": posts}), 200

    @es_blueprint.route("/search", methods=["GET"])
    def find_posts():
        q = request.args.get("literal_query")
        limit = request.args.get("limit")
        s = request.args.get("strategy")
        if not q:
            return jsonify({
                "result": "invalid query parameter - please set literal query"
            }), 400

        posts = es.find_posts(query=q, size=limit) if limit else es.find_posts(query=q)
        return jsonify({"result": posts}), 200

    @es_blueprint.route("/insert", methods=["POST"])
    def insert_post():
        json_blob = request.get_json()

        try:
            post = json_blob["post"]
        except KeyError:
            return json.dumps({
                "result":
                    "key missing in json,"
                    "please make you sure the json has the field 'post'"
            }), 400

        if not post_utils.is_valid_post(post):
            return jsonify({
                "result":
                    "missing content field in the post,"
                    " please make sure you have them as attributes in your post"
            }), 400

        # inserts a post
        es.insert_post(post)
        return "ok", 201

    @es_blueprint.route("/retrieve", methods=["GET"])
    def retrieve_post():
        pass

    @es_blueprint.route("/bulkInsert", methods=["POST"])
    def bulk_insert():
        pass

    @es_blueprint.route("/delete", methods=["POST"])
    def delete_post_by():
        json_post_query = request.get_json()
        if "score" not in json_post_query and "id" not in json_post_query > 1:
            return jsonify({"error": "Only 2 types"
                                     "of post deletions are supported at the moment. "
                                     "(1) posts with score = 0, and (2) post with a given id"}), 400
        if "score" in json_post_query:
            score = json_post_query["score"]
            es.delete_post_by({
                "query": {
                    "match": {
                        "score": score
                    }
                }
            })
        elif "id" in json_post_query:
            post_id = json_post_query["id"]
            es.delete_post_by({
                "query": {
                    "match": {
                        "id": post_id
                    }
                }
            })

    @es_blueprint.route("/median", methods=["GET"])
    def get_median():
        framework = request.args.get("framework")
        timestamp_to_medians = es.find_median_scores_of(framework)
        sorted_timestamps = sorted(timestamp_to_medians)
        medians = [timestamp_to_medians[t] for t in sorted_timestamps]
        return jsonify({
            "timestamps": sorted_timestamps,
            "medians": medians
        }), 200

    return es_blueprint
