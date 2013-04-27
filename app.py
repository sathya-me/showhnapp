import cherrypy
import jinja2
import os
from django.utils import simplejson
import urllib2
import re

template_dir = os.path.join(os.path.dirname(__file__), 'Templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)
resources_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Resources/')

api_url = "http://api.thriftdb.com/api.hnsearch.com/items/_search?q=show+hn&type=submission&sortby=create_ts+desc&pretty_print=true"

#config_file = os.path.join(os.path.dirname(__file__), 'dev.conf')

class Post(object):
	"""docstring for Post"""
	def __init__(self, arg):
		super(Post, self).__init__()
		self.title 		= arg['title']
		self.desc 		= arg['text']
		self.username 	= arg['username']
		self.date 		= arg['create_ts']
		self.url 		= arg['url']

		if self.url == None:
			regex = re.compile("(?P<url>https?://[^\s]+)")
			url   =  re.search(regex ,self.desc)
			if url != None:
				self.url = url.group("url")

def parsePage():
	response 	= urllib2.urlopen(api_url)
	html 		= response.read()
	jsonData  		= simplejson.loads(html)
	return jsonData

def perform_parse():
	raw_posts  = parsePage()['results']

	if raw_posts == []: 
		return 'No Projects Found'

	posts = []
	for raw_post in raw_posts:	
		post = Post(raw_post['item'])
		posts.append(post)
	return posts

class PageLoader(object):
    def index(self):
    	html = jinja_env.get_template('index.html')
    	posts = perform_parse()
        return html.render({'posts' : posts})
    index.exposed = True
    def about(self):
    	return config_file
    about.exposed = True
    def parse(self):
    	return perform_parse()
    parse.exposed = True


config_dict = {
        '/': {
        'tools.staticdir.root': resources_path, 
		},
        '/Resources/js': {
          'tools.staticdir.on': True,
          'tools.staticdir.dir': os.path.join(resources_path, 'js/')
          	},
        '/Resources/css': {
          'tools.staticdir.on': True,
          'tools.staticdir.dir': os.path.join(resources_path, 'css/')
        },
        '/Resources/images': {
          'tools.staticdir.on': True,
          'tools.staticdir.dir': os.path.join(resources_path, 'images/')
        },
        '/bootstrap': {
          'tools.staticdir.on': True,
          'tools.staticdir.dir': os.path.join(resources_path, 'bootstrap/')
        }
      }


cherrypy.quickstart(PageLoader(), config = config_dict)