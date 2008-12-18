#!/usr/bin/env python
# encoding: utf-8
"""
disqus.py

Created by Devin Naquin on 2008-12-17.
Copyright (c) 2008. All rights reserved.
"""

import unittest, warnings

# TODO abstract into same method.
# TODO conditionally warn if key not set. how to do with decorator?
def user_key_required(f):
	def wrapped(*args, **kwargs):
		warnings.warn("method requires a user api key set in the Api class's constructor.")
		return f(*args, **kwargs)
	return wrapped
		
def forum_key_required(f):
	def wrapped(*args, **kwargs):
		warnings.warn("method requires a forum api key set in the Api class's constructor.")
		return f(*args, **kwargs)
	return wrapped


class Api(object):


	def __init__(self, forum_key=None, user_key=None):
		pass


class ApiTests(unittest.TestCase):


	def setUp(self):
		pass


if __name__ == '__main__':
	unittest.main()
