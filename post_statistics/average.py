from collections import defaultdict

import numpy as np


def group_by(post_list, attr_selector):
    attribute_to_posts = defaultdict(list)
    for post in post_list:
        attribute_to_posts[attr_selector(post_list)].append(post)
    return attribute_to_posts


def mean(list_of_numeric_attrs):
    return np.mean(np.array(list_of_numeric_attrs))


def median(list_of_numeric_attrs):
    return np.median(np.array(list_of_numeric_attrs))


def custom_average(list_of_numeric_attrs, callback):
    return callback(list_of_numeric_attrs)
