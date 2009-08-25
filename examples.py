import sys, json, disqus

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print "ERROR: User key not supplied"
        print "Usage: %s <user_key> [version_number (Default = 1.1)]" % sys.argv[0]
        sys.exit(1)
    elif len(sys.argv) == 3:
        version = sys.argv[2]
    else:
        version = '1.1'

    api = disqus.Api(sys.argv[1], version)

#   
#    f = api.get_forum_list()
#    print f
#    print "Forum id = " + f['id']
#    f = Forum(t)

#    fk = api.get_forum_api_key(f['id'])
#    print "Forum key = " + fk
#    api.set_forum_key(fk)

    api.load_forums()
#    print api.forums

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

