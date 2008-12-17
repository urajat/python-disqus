#!/usr/bin/env python
# encoding: utf-8
"""
timedcache.py

Created by Devin Naquin on 2008-12-17.
Copyright (c) 2008. All rights reserved.
"""

from datetime import datetime, timedelta
import time, unittest


class TimedCache:


	def __init__(self, producer, seconds=60):
		self.producer = producer
		if seconds and seconds>0:
			self.delta = timedelta(seconds=seconds)
		else:
			self.delta = None

		self.store = {}

	def get(self, key):
		now = datetime.now()

		# If key not in cache or cache has expiration time and key expired.
		# Compute and cache result.
		if key not in self.store or \
				(self.delta and self.store[key][0] + self.delta < now):
			result = self.producer(key)
			
			self.store[key] = (now, result)
			
			return result
		else:
			return self.store[key][1]


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