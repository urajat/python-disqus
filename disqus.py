"""
    disqus.py

    A Python interface to DISQUS API

    Copyright (c) 2009 Rajat Upadhyaya
    Partly based on Devin Naquin's 'python-disqus' at http://github.com/devin/python-disqus
"""

import sys
import urllib, urllib2

try:
    # Python 2.6 or greater
    import json
except ImportError:
    import simplejson as json

from BaseHTTPServer import BaseHTTPRequestHandler


class ApiError(Exception):
    """ Error raised by a Disqus API call """

    def __init__(self, code, message):
        self.code, self.mesg = code, message

    def __str__(self):
        return '%s (%s)' % (self.code, self.mesg)


class Api:
    """
        Encapsulates Disqus API methods 
        API docs at http://wiki.disqus.net/API
    """

    # Base path for API methods
    URL = 'http://disqus.com/api/'

    # Supported API versions
    __VERSIONS = ['1.0', '1.1']

    # For v1.1 use
    __forum_key_methods = ['create_post', 'thread_by_identifier', 'update_thread']

    # For v1.0 use
    __user_key_methods = ['get_forum_list', 'get_forum_api_key']


    def __init__(self, user_key, version='1.1'):
        self.user_key = user_key

        if version in self.__VERSIONS:
            self.version = version
        else:
            raise ApiError('VersionError', 'Version %s is unsupported'
                           %(version)) 

        if version == '1.1':
            self.user_name = self.invoke('get_user_name', {}, type='POST')


    def load_forums(self):
        self.forums = self.get_forum_list()
        for f in self.forums:
            f['api_key'] = self.get_forum_api_key(f['id'])
 
    def set_forum_key(self, forum_key):
        self.forum_key = forum_key

    def invoke(self, name, args=None, type='GET'):
        if args is None:
            args = {}
        method_url = self.URL + name

        args['api_version'] = self.version

        if self.version == '1.1':
            if name in self.__forum_key_methods:
                args['forum_api_key'] = self.forum_key
            else:
                args['user_api_key'] = self.user_key
        elif self.version == '1.0':
            if name in self.__user_key_methods:
                args['user_api_key'] = self.user_key
            else:
                args['forum_api_key'] = self.forum_key

        data = urllib.urlencode(args)

        try:
            if type == 'GET':
                response = urllib2.urlopen(method_url + '?' + data)
            else:
                req = urllib2.Request(method_url + '/', data)
                response = urllib2.urlopen(req)
        except IOError, e:
            if hasattr(e, 'reason'):
                print 'URL Error: %s' % e.reason
            elif hasattr(e, 'code'):
                print 'HTTP Error %d: %s' % (e.code, BaseHTTPRequestHandler.responses[e.code])
            else:
                print 'IO Error: %s' % e
            return False

        r = json.load(response)
        if r['succeeded']:
            return r['message']

        raise ApiError(r['code'], r['message'])

    # GET methods
    def get_forum_list(self):
        return self.invoke('get_forum_list')

    def get_forum_api_key(self, forum_id):
        return self.invoke('get_forum_api_key', { 'forum_id': forum_id })

    def get_thread_list(self):
        return self.invoke('get_thread_list')

    def get_num_posts(self, thread_list):
        return self.invoke('get_num_posts', { 'thread_ids': ','.join(thread_list) })

    def get_thread_by_url(self, url):
        return self.invoke('get_thread_by_url', { 'url': url })

    def get_thread_posts(self, thread_id):
        return self.invoke('get_thread_posts', { 'thread_id': thread_id })


    # POST methods
    def create_post(self, attributes):
        return self.invoke('create_post', attributes, type='POST')

    def thread_by_identifier(self, identifier, title=None):
        return self.invoke('thread_by_identifier',
                           {'identifier': identifier, 'title': title },
                           type='POST')

    def update_thread(self, thread_id, attributes={}):
        attributes['thread_id'] = thread_id
        return self.invoke('update_thread', attributes, type='POST')

    # v1.1 only methods
    def get_user_name(self):
        if self.version == '1.1':
            return self.invoke('get_user_name', {}, type='POST')
        
        raise ApiError('get_user_name', 'Unsupported in API v1.0')

    def moderate_post(self):
        if self.version == '1.1':
            raise ApiError('moderate_post', 'Unimplemented method')
        
        raise ApiError('get_user_name', 'Unsupported in API v1.0')

    def get_updated_threads(self):
        if self.version == '1.1':
            raise ApiError('get_updated_threads', 'Unimplemented method')
        
        raise ApiError('get_user_name', 'Unsupported in API v1.0')

    def get_forum_posts(self):
        if self.version == '1.1':
            raise ApiError('get_forum_posts', 'Unimplemented method')
        
        raise ApiError('get_user_name', 'Unsupported in API v1.0')


class Forum:
#    FIELDS = ['id', 'shortname', 'name', 'created_at']
    
    def __init__(self, attributes):
        for k, v in attributes.iteritems():
            setattr(self, k, v)


class Thread:
#    FIELDS = ['id', 'forum', 'slug', 'title', 'created_at', 'allow_comments', 'url', 'identifier']

    def __init__(self, attributes):
        for k, v in attributes.iteritems():
            setattr(self, k, v)


class Post:
#    FIELDS = ['id', 'forum', 'thread', 'created_at', 'message', 'parent_post', 'shown', 'is_anonymous', 'anonymous_author', 'author']

    def __init__(self, attributes):
        for k, v in attributes.iteritems():
            setattr(self, k, v)


