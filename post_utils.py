def toPost(elastic_hit):
    """
    TODO:
    need to raise a warning if any of the attributes aren't present..
    :param elastic_hit:
    :return:
    """
    post = {}
    if "score" in elastic_hit:
        post["score"] = elastic_hit["score"]
    if "url" in elastic_hit:
        post["url"] = elastic_hit["url"]
    if "content" in elastic_hit:
        post["content"] = elastic_hit["content"]
    return post
