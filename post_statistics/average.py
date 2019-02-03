from collections import defaultdict

import numpy as np


def group_by(post_list, attr_selector):
    attribute_to_posts = defaultdict(list)
    for post in post_list:
        attribute_to_posts[attr_selector(post)].append(post)
    return attribute_to_posts


def mean(list_of_posts, key=lambda x: x):
    return np.mean(np.array([key(p) for p in list_of_posts]))


def median(list_of_posts, key=lambda x: x):
    return np.median(np.array([key(p) for p in list_of_posts]))


def custom_average(list_of_numeric_attrs, callback):
    return callback(list_of_numeric_attrs)
