import cherrypy
import jinja2
import os
from django.utils import simplejson
import urllib2
import re

template_dir = os.path.join(os.path.dirname(__file__), 'Templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)
resources_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Resources/')

api_url = "http://api.thriftdb.com/api.hnsearch.com/items/_search?filter[fields][type]=submission&filter[fields][title]=show+hn&sortby=%s+desc&start=%s"

class Post(object):
	"""docstring for Post"""
	def __init__(self, arg):
		super(Post, self).__init__()
		self.title 		= arg['title']
		self.desc 		= arg['text']
		self.username 	= arg['username']
		self.date 		= arg['create_ts']
		self.url 		= arg['url']
		self.id     	= arg['id']
		self.points		= arg.get('points')


		website_regex = re.compile("(?P<url>https?://[^\s/]+)")

		if self.url == None:
			
			url   =  re.search(website_regex ,self.desc)
			if url != None:
				self.url = url.group("url")

		if (self.title == None) and (arg['discussion']['title'] != ""):
			self.title = arg['discussion']['title']

		if (self.title == None) and (self.url != None):
			self.title = self.url

def parsePage(start, filter):

	try:
		filter = int(filter)
	except Exception, e:
		filter = 1

	filters = ["score", "create_ts", "points"]
	filter_to_use = filters[filter-1]
	response 	= urllib2.urlopen(api_url % (filter_to_use, str(start)))
	html 		= response.read()
	jsonData  	= simplejson.loads(html)
	return jsonData

def perform_parse(start, filter):
	raw_posts  = parsePage(start, filter)['results']

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

		post_filter = 1
		if len(kwargs) > 0:
			try:
				post_filter = int(kwargs.get('filter', 1))
			except Exception, e:
				post_filter = 1

		if (post_filter < 1) or (post_filter > 3):
			post_filter = 1

		start = (page -1) * 10
		posts = perform_parse(start, post_filter)

		if  (posts == None) or (len(posts) == 0):
			return "Error Occured"

		return html.render({
        	'posts' : posts,
        	'page'	: page,
        	'filter': post_filter
        	})
		
    index.exposed = True

    def default(self, attr='abc',  *args, **kwargs):
		cherrypy.response.status = 404
		html = jinja_env.get_template('404.html')
		return html.render()
    default.exposed = True

config_dict = {
        '/': {
        'tools.staticdir.root': resources_path, 
		},
        '/Resources/js': {
          'tools.staticdir.on': True,
          'tools.staticdir.dir': 'js/'
          	},
        '/Resources/css': {
          'tools.staticdir.on': True,
          'tools.staticdir.dir': 'css/'
        },
        '/Resources/images': {
          'tools.staticdir.on': True,
          'tools.staticdir.dir': 'images/'
        },
        '/bootstrap': {
          'tools.staticdir.on': True,
          'tools.staticdir.dir': 'bootstrap/'
        }
      }


cherrypy.config.update({'server.socket_host': '0.0.0.0',})
cherrypy.config.update({'server.socket_port': int(os.environ.get('PORT', '5000')),})
cherrypy.quickstart(PageLoader(), config = config_dict)