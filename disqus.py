#!/usr/bin/env python
# encoding: utf-8
"""
disqus.py

Created by Devin Naquin on 2008-12-17.
Copyright (c) 2008. All rights reserved.
"""

import unittest, warnings

import simplejson as json


class Api(object):
	"""
	TODO write
	"""

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


	def __init__(self, forum_key=None, user_key=None, disqus_fetcher=None):
		self.forum_key 	= forum_key
		self.user_key	= user_key

		# TODO check for none and insert default
		self.disqus_fetcher = None


class Forum(object):


	def __init__(self, id, shortname, name):
		self.id			= id
		self.shortname	= shortname
		self.name		= name


class Thread(object):


	def __init__(self, id, forum_id, slug, title, created_at, allow_comments,
			url, identifier):
		self.id				= id
		self.forum_id		= forum_id
		self.slug			= slug
		self.title			= title
		self.created_at		= created_at
		self.allow_comments	= allow_comments
		self.url			= url
		self.identifier		= identifier


class Post(object):


	def __init__(self, id, forum_id, thread_id, created_at, message,
			parent_post_id, shown, is_anonymous, anonymous_author, author):
		self.id					= id
		self.forum_id			= forum_id
		self.thread_id			= thread_id
		self.created_at			= created_at
		self.message			= message
		self.parent_post_id		= parent_post_id
		self.shown				= shown
		self.is_anonymous		= is_anonymous
		# TODO author depends on is_anonymous.
		# TODO author is compound data type
		self.anonymous_author	= anonymous_author
		self.author				= author


class DisqusFetcher(object):
	"""
	TODO write
	returns JSON
	"""


	def __init__(self):
		pass

	# get methods
	def get_forum_list(self):
		pass

	def get_forum_api_key(self, forum_id):
		pass

	def get_thread_list(self):
		pass

	def get_thread_by_url(self):
		pass

	def get_thread_posts(self):
		pass

	def get_num_posts(self):
		pass

	# post methods
	def create_post(self):
		pass

	def thread_by_identifier(self):
		pass

	def update_thread(self):
		pass


class ApiTests(unittest.TestCase):


	class MockFetcher(DisqusFetcher):

		def __init__(self, forums, threads, posts):
			self.forums		= forums
			self.threads	= threads
			self.posts		= posts

		# get methods
		def get_forum_list(self):
			serializable = [forum.__dict__ for forum in self.forums]

			return json.dumps(serializable)

		def get_forum_api_key(self, forum_id):
			pass

		def get_thread_list(self):
			pass

		def get_thread_by_url(self):
			pass

		def get_thread_posts(self):
			pass

		def get_num_posts(self):
			pass

		# post methods
		def create_post(self):
			pass

		def thread_by_identifier(self):
			pass

		def update_thread(self):
			pass

	def setUp(self):
		pass


if __name__ == '__main__':
	unittest.main()
