#!/usr/bin/env python
# encoding: utf-8
"""
disqus.py

Created by Devin Naquin on 2008-12-17.
Copyright (c) 2008. All rights reserved.
"""

import unittest, warnings


class Api(object):


	def key_required(key):
		def decorator(f):
			def wrapped(*args, **kwargs):
				self = args[0]
				if not getattr(self, '%s_key' % key):					
					warnings.warn("method requires a %s api key set in the Api class's constructor." % key)
				return f(*args, **kwargs)
			return wrapped
		return decorator

	user_key_required 	= key_required('user')
	forum_key_required	= key_required('forum')


	def __init__(self, forum_key=None, user_key=None):
		self.forum_key = forum_key
		self.user_key = user_key

	@user_key_required
	def user_method(self):
		print 'user_method'


class ApiTests(unittest.TestCase):


	def setUp(self):
		pass


if __name__ == '__main__':
	unittest.main()
