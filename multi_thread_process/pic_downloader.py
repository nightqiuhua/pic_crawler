import csv
import re
import lxml.html 
import urllib.parse 
import urllib.request
import os
import gzip 

DEFAULT_DIR_PATH = 'G:\\pic'
DEFAULT_NODE_REGX = 'http://www.mzitu.com/[0-9]+'

class pic_donwloader:
	def __init__(self,DIR_PATH=DEFAULT_DIR_PATH,node_regx=DEFAULT_NODE_REGX):
		self.DIR_PATH = DIR_PATH 
		self.node_regx = node_regx 

	def __call__(self,seed_url,html,downloader):
		if re.match(self.node_regx,seed_url):
			print('downloading:',seed_url)
			tree = lxml.html.fromstring(html)
			folder_name = tree.xpath('//h2[@class="main-title"]/text()')[0]
			print('folder_name=',folder_name)
			dir_result = self.make_directors(folder_name)
			img_page_seen = set()
			img_url_page = [seed_url]
			D = downloader
			img_links=[]
			while img_url_page:
				img_url = img_url_page.pop()
				img_html = D(img_url).decode('utf-8')
				img_tree = lxml.html.fromstring(img_html)
				img_links.append(self.get_img_link(img_tree))
				for link in self.get_img_page_link(img_tree):
					if link not in img_page_seen:
						if re.match(seed_url,link):
							img_page_seen.add(link)
							img_url_page.append(link)
			print('img_links =',img_links)
			self.save_picture(img_links,folder_name,Downloader=D)


	def make_directors(self,folder_name):
		path = os.path.join(self.DIR_PATH,folder_name)
		if not os.path.exists(path):
			os.makedirs(path)
			print(path)
			os.chdir(path)
			return True 
		print('Folder has existed!')
		return False 

	def save_picture(self,img_urls,folder_name,Downloader):
		dir_path = os.path.join(self.DIR_PATH,folder_name)
		print('download pic')
		if os.path.exists(dir_path):
			number = 0
			for url in img_urls:
				number += 1
				img = Downloader(url)
			#保存图片
				imgpath = os.path.join(dir_path,'pic_cnt_{}.jpg'.format(number))
				try:
					with open(imgpath,'wb') as f:
						f.write(img)
				except Exception as e:
					print(e)
		else:
			print('dir_path does not exist,please build one')

	def delete_empty_dire():
		if os.path.exists(dir):
			if os.path.isdir(dir):
				for d in os.listdir(dir):
					path = os.path.join(dir,d)
					if os.path.isdir(path):
						delete_empty_dir(path)
			if not os.listdir(dir):
				os.rmdir(dir)
				print('remove the empty dir: {}'.format(dir))
			else:
				print('Please start your performance!')

	def get_img_link(self,img_html):
		return img_html.xpath('//div[@class="main-image"]/p/a/img/@src')[0]

	def get_img_page_link(self,img_html):
		return img_html.xpath('//div[@class="pagenavi"]/a/@href')

