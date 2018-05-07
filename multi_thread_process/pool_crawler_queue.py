from pymongo import MongoClient
from multiprocessing import Pool 
from downloader_p3 import Downloader
from mongo_queue_p3 import MongoQueue
from mongo_cache_p3 import MongoCache 
from pic_downloader import pic_donwloader
from scrape_callback_p3 import Scrape_Callback
import threading
import urllib.parse
import multiprocessing
import time 
import os


SLEEP_TIME = 2
DEFAULT_CACHE = MongoCache()
DEFAULT_PIC_DOWNLOADER = pic_donwloader()
DEFAULT_SC_CALLBACK = Scrape_Callback()
def threaded_crawler(seed_url,delay=5,cache=DEFAULT_CACHE,pic_downloader=DEFAULT_PIC_DOWNLOADER,scrape_callback=DEFAULT_SC_CALLBACK,user_agent='wswp',proxies=None,num_retries=1,max_threads=10,timeout=60):
	print('process_threaded_crawler=',os.getpid())
	crawl_queue = MongoQueue()
	crawl_queue.clear()
	crawl_queue.push(seed_url)
	print('yes_3')
	D = Downloader(cache=cache,delay=delay,proxies=proxies,num_retries=num_retries,timeout=timeout)
	print('yes_4')
	def process_queue():
		while True:
			try:
				url = crawl_queue.pop()
				print('url = ',url)
			except KeyError:
				break
			else:
				html = D(url).decode('utf-8')
				if pic_downloader:
					pic_downloader.__call__(url,html,D)
				if scrape_callback:
					try:
						links = scrape_callback(url,html)
					except Exception as e:
						print('error in callback for:{}:{}'.format(url,e))
					else:
						for link in links:
							crawl_queue.push(normalize(seed_url,link))
				crawl_queue.complete(url)
	threads = []
	while threads or crawl_queue.peek():
		for thread in threads:
			if not thread.is_alive():
				threads.remove()
		while len(threads) < max_threads and crawl_queue.peek():
			thread = threading.Thread(target = process_queue)
			thread.setDaemon(True)
			thread.start()
			threads.append(thread)
		time.sleep(SLEEP_TIME)
def normalize(seed_url,link):
	link,_= urllib.parse.urldefrag(link)
	return urllib.parse.urljoin(seed_url,link)

def pool_crawler(args):
	num_cpu = multiprocessing.cpu_count()
	pool = Pool(2)
	print('Start {} processing'.format(num_cpu))
	for num in range(2):
		#print('kwargs=',kwargs)
		pool.apply_async(func=threaded_crawler,args=(args,))
	pool.close()
	pool.join()


