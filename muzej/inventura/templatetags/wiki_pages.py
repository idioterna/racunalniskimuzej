from django import template
from wiki.models import Page

register = template.Library()

class GetWikiPagesNode(template.Node):
	def __init__(self, varname):
		self.varname = varname

	def __repr__(self):
		return "<GetWikiPagesNode Node>"

	def render(self, context):
		context[self.varname] = pages = Page.objects.all()
		return ''

class DoGetWikiPages:
	def __init__(self, tag_name):
		self.tag_name = tag_name

	def __call__(self, parser, token):
		tokens = token.contents.split()
		if len(tokens) != 3:
			raise template.TemplateSyntaxError("'%s' statements require two arguments" %
					(self.tag_name,))
		if tokens[1] != 'as':
			raise template.TemplateSyntaxError("Second argument in '%s' must be 'as'" %
					self.tag_name)
		return GetWikiPagesNode(varname=tokens[2])

register.tag('get_wiki_pages', DoGetWikiPages('get_wiki_pages'))
