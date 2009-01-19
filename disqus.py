"""
    disqus.py

    A Python interface to DISQUS API

    Copyright (c) 2009 Rajat Upadhyaya
    Partly based on Devin Naquin's 'python-disqus' at http://github.com/devin/python-disqus
"""

import sys
import urllib, urllib2

# Python 2.6 or greater
import json

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
        API docs at http://disqus.com/docs/api/
    """

    # Base path for API methods
    URL = 'http://disqus.com/api/'

    def __init__(self, user_key):
        self.user_key = user_key

    def set_forum_key(self, forum_key):
        self.forum_key = forum_key

    def invoke(self, name, args={}, type='GET'):
        method_url = self.URL + name + '/'

        if name in ['get_forum_list', 'get_forum_api_key']:
            args['user_api_key'] = self.user_key
        else:
            args['forum_api_key'] = self.forum_key
        data = urllib.urlencode(args)

        try:
            if type == 'GET':
                response = urllib2.urlopen(method_url + '?' + data)
            else:
                req = urllib2.Request(method_url, data)
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
        response = self.invoke('get_forum_list')

        # Assumes single forum
        return response[0]

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


class Forum:
    FIELDS = ['id', 'shortname', 'name']
    
    def __init__(self, attributes):
        for k, v in attributes.iteritems():
            if k in self.FIELDS:
                setattr(self, k, v)


class Thread:
    FIELDS = ['id', 'forum', 'slug', 'title', 'created_at', 'allow_comments', 'url', 'identifier']

    def __init__(self, attributes):
        for k, v in attributes.iteritems():
            if k in self.FIELDS:
                setattr(self, k, v)


class Post:
    FIELDS = ['id', 'forum', 'thread', 'created_at', 'message', 'parent_post', 'shown', 'is_anonymous', 
               'anonymous_author', 'author']

    def __init__(self, attributes):
        for k, v in attributes.iteritems():
            if k in self.FIELDS:
                setattr(self, k, v)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print "ERROR: User key not supplied"
        print "Usage: %s <user_key>" % sys.argv[0]
        sys.exit(1)

    api = Api(sys.argv[1])
    f = api.get_forum_list()
    print f
    print "Forum id = " + f['id']
#    f = Forum(t)

    fk = api.get_forum_api_key(f['id'])
    print "Forum key = " + fk
    api.set_forum_key(fk)

"""
    Examples:
    ---------
#   Get all threads associated with the forum
    threads = api.get_thread_list()
    print json.dumps(threads, sort_keys=True, indent=4)
#    threads = [Thread(t) for t in api.get_thread_list()]

#   Get the number of posts for each thread whose id is specified
    t = api.get_num_posts(['1234567', '7654321'])
    print t

#   Get a thread by its URL and update various fields
#    t = api.get_thread_by_url('http://example.com/some/path/')
    print t
    t = api.update_thread(t['id'], 
                          {
			   'title'         : 'Some title here',
			   'slug'          : 'some_slug_here',
			   'url'           : 'http://example.com/path/',
			   'allow_comments': 0                             # 0 or 1
			  })
    print t

#   Get all posts with the given 'id'
    t = api.get_thread_posts(t['id'])
    print json.dumps(t, sort_keys=True, indent=4)
#    posts = [Post(p) for p in api.get_thread_posts('1234567')]

#   Attach a post as a reply to another post
    m = {'author_name' : 'Me', 
         'author_email': 'me@example.com',
         'author_url'  : 'http://example.com/',
         'ip_address'  : '192.168.1.1'}
    t = api.get_thread_posts(t['id'])
    parent = t[4]
    th = t[1]
    m['thread_id']   = th['thread']
    m['message']     = th['message']
    m['created_at']  = th['created_at']
    m['parent_post'] = parent['id']
    r = api.create_post(m)
    print r

#   Get a thread by its identifier or create a thread with the given identifier
    t = api.thread_by_identifier('Some identifier here', 'Optional title here')
    print t
"""

