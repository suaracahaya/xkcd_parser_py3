import sys
import urllib
import urllib.request
import re
from lxml import etree
import random
import datetime


class Downloader():
	'''
	Class to retrieve HTML code
	and binary files from a
	specific website
	'''

	def __init__(self, url):
		self.url = url

	def download(self, image_name='', is_image=False, comicno=''):

		#browser = urllib.urlopen(self.url) --> this works for Python 2.x
		#for Python 3.x :
		try:
			browser = urllib.request.urlopen(self.url)
			response = browser.getcode()
		except:
			print('Bad connection')
			sys.exit()

		if response == 200:
			contents = browser.read()
		else:
			print('Bad header response')
			sys.exit()

		if is_image:
			self.save_image(contents, image_name, comicno)

		return contents


	def save_image(self, contents, image_name, comicno):
			filename = str(comicno)+" "+image_name+".jpg"
			image_file = open(filename, 'wb')
			image_file.write(contents)
			image_file.close()
			#print('Image has been saved!')


# The image will be saved on the local machine in the current directory (where the script is placed).


class xkcdParser():
	'''
	Class for parsing xkcd.com
	'''

	def __init__(self):
		self.url = "http://xkcd.com/"
		self.last_comic_nr = None
		self.contents = ''
		self.title = ''
		self.caption = ''
		self.comicnumber = ''

	def set_last_comic_nr(self):
		downloader = Downloader(self.url)
		self.contents = downloader.download() #seems that this produces bytes, not string 
		
		# old code; return error in Python 3
		#self.last_comic_nr = re.search(r'http://xkcd.com/(\d+)', self.contents).group(1)
		
		# new code; convert contents from byte to string before search
		searchlastcomic = re.search(r'http://xkcd.com/(\d+)', self.contents.decode('utf-8'), re.I | re.U)
		if searchlastcomic is None:
			print('No last comic is found!')
		else:
			self.last_comic_nr = searchlastcomic.group(1)
			self.last_comic_nr = int(self.last_comic_nr)
			#print(self.last_comic_nr)
	
	def get_current_comic(self):
		self.set_last_comic_nr()
		self.get_title()
		self.get_caption()
		self.get_comic()

	def get_comic_by_id(self, comic_nr):
		if not self.last_comic_nr:
			self.set_last_comic_nr()

		try:
			comic_nr = int(comic_nr)
		except:
			print('The comic number should be an integer')
			sys.exit()

		if comic_nr <= self.last_comic_nr:
			url = self.url + str(comic_nr)
			downloader = Downloader(url)
			self.contents = downloader.download()
			self.comicnumber = comic_nr
			self.get_title()
			self.get_caption()
			self.get_comic()
			self.save_comic_info()


	def get_random_comic(self):
		if not self.last_comic_nr:
			self.set_last_comic_nr()

		comic_nr = random.randint(1, self.last_comic_nr)
		self.get_comic_by_id(comic_nr)


	def get_title(self):
		if self.contents:
			tree = etree.HTML(self.contents)
			self.title = tree.xpath("string(//div[@id='ctitle'])")

	def get_caption(self):
		if self.contents:
			tree = etree.HTML(self.contents)
			self.caption = tree.xpath("string(//div[@id='comic']/img/@title)")

	def get_comic(self):
		if self.contents:
			tree = etree.HTML(self.contents)
			url = tree.xpath("string(//div[@id='comic']/img/@src)")

			downloader = Downloader(url)
			downloader.download(self.title, True, self.comicnumber)
			# the parameter True will tell Downloader that it is passing an image, 
			# thus provoking function save_image().

	# I made this function by myself
	def save_comic_info(self):
		s = str(datetime.datetime.now()) + '\n' + str(self.comicnumber) + ' ' + self.title + '\n' + self.caption + '\n\n'
		with open("xkcd_download_history.txt","a+") as f:
    			f.write(s)

		print('Comic info has been saved!')
		


if __name__ == '__main__':
	
	xkcd_parser = xkcdParser()
	
	# get current comic
	#xkcd_parser.get_current_comic()
	
	# get random comic
	xkcd_parser.get_random_comic()

	print("Downloaded comic no." + str(xkcd_parser.comicnumber))

