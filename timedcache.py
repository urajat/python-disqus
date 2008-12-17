#!/usr/bin/env python
# encoding: utf-8
"""
timedcache.py

Created by Devin Naquin on 2008-12-17.
Copyright (c) 2008. All rights reserved.
"""

import time, unittest


class TimedCache:


	def __init__(self, producer, seconds=60):
		self.producer = producer
		self.seconds = seconds

	def get(self, key):
		pass


class TimedCacheTests(unittest.TestCase):		

	def setUp(self):
		def make_producer():
			counter = [0]
			def producer(unused):
				counter[0] += 1
				return counter[0]
			return producer
		self.producer = make_producer()

	def testProducer(self):
		self.assertEqual(1, self.producer(None))
		self.assertEqual(2, self.producer(None))

	def testCacheHit(self):
		cache = TimedCache(self.producer, seconds=None)
		result = cache.get('key')
		self.assertEqual(1, result)
		result = cache.get('key')
		self.assertEqual(1, result)

	def testCacheMiss(self):
		cache = TimedCache(self.producer, seconds=2)
		result = cache.get('key')
		self.assertEqual(1, result)
		result = cache.get('key')
		self.assertEqual(1, result)
		time.sleep(2)
		result = cache.get('key')
		self.assertEqual(2, result)


if __name__ == '__main__':
	unittest.main()