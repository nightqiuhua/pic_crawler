import re
import lxml.html


DEFAULT_ROOT_CCS = 'div.nav-links>a.page-numbers'
DEFAULT_NODE_CSS = 'div.postlist>ul#pins>li>span>a'
DEFAULT_NODE_REGX = 'http://www.mzitu.com/[0-9]+'
class Scrape_Callback:
	def __init__(self,node_regx=DEFAULT_NODE_REGX,root_ccs=DEFAULT_ROOT_CCS,node_ccs=DEFAULT_NODE_CSS):
		self.node_regx = node_regx
		self.root_ccs = root_ccs
		self.node_ccs = node_ccs
		self.links = []
		self.root_page_links = []
		self.node_page_links = []

	def __call__(self,url,html):
		if not re.match(self.node_regx,url):
			tree = lxml.html.fromstring(html)
			self.root_page_links = self.get_links(tree,self.root_ccs)
			#print('self.root_page_links=',self.root_page_links)
			self.node_page_links = self.get_links(tree,self.node_ccs)
			self.links.extend(self.root_page_links+self.node_page_links)
			return self.links
		else:
			return []

	def get_links(self,tree_html,ccs):
		ccs_links= []
		results = tree_html.cssselect(ccs)
		ccs_links.extend(result.get('href') for result in results)
		#print('root_links=',root_links)
		return ccs_links

