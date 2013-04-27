import cherrypy
import jinja2
import os
from django.utils import simplejson
import urllib2
import re

template_dir = os.path.join(os.path.dirname(__file__), 'Templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)
resources_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Resources/')

api_url = "http://api.thriftdb.com/api.hnsearch.com/items/_search?filter[fields][type]=submission&filter[fields][title]=show+hn&sortby=create_ts+desc&start="

class Post(object):
	"""docstring for Post"""
	def __init__(self, arg):
		super(Post, self).__init__()
		self.title 		= arg['title']
		self.desc 		= arg['text']
		self.username 	= arg['username']
		self.date 		= arg['create_ts']
		self.url 		= arg['url']

		website_regex = re.compile("(?P<url>https?://[^\s/]+)")

		if self.url == None:
			
			url   =  re.search(website_regex ,self.desc)
			if url != None:
				self.url = url.group("url")

		if (self.title == None) and (arg['discussion']['title'] != ""):
			self.title = arg['discussion']['title']

		if (self.title == None) and (self.url != None):
			self.title = self.url

def parsePage(start):
	response 	= urllib2.urlopen(api_url + str(start))
	html 		= response.read()
	jsonData  		= simplejson.loads(html)
	return jsonData

def perform_parse(start):
	raw_posts  = parsePage(start)['results']

	if raw_posts == []: 
		return 'No Projects Found'

	posts = []
	for raw_post in raw_posts:	
		post = Post(raw_post['item'])
		posts.append(post)
	return posts

class PageLoader(object):
    def index(self, *args, **kwargs):
		html = jinja_env.get_template('index.html')
		page = 1
		if len(kwargs) > 0:
			try:
				page = int(kwargs.get('page', 1))
			except Exception, e:
				page = 1

		start = (page -1) * 10
		posts = perform_parse(start)

		return html.render({
        	'posts' : posts,
        	'page'	: page
        	})
		
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


cherrypy.config.update({'server.socket_host': '0.0.0.0',})
cherrypy.config.update({'server.socket_port': int(os.environ.get('PORT', '5000')),})
cherrypy.quickstart(PageLoader(), config = config_dict)