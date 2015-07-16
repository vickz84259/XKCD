#! python2
# xkcd.py - Downloads comics from xkcd.com.
#
# Takes 2 optional arguments when launched from the command line
# which in default are "download=latest" and 
# "path=C:\XKCD"
#
# 'download' argument specifies whether to download the 'latest' or
# 'all' XKCD comics
# Using "latest" will download all the comics published since you 
# the last comic you downloaded. If no prior comics have been downloaded, 
# only the most recent comic will be downloaded.
#
#
# 'path' argument specifies the path where to save the comics

# Standard library modules
import os, sys

# Third-party modules
import requests, bs4

# Project-specific modules

# Defining Constants
STATUS = ['Comic image not found', 'Error downloading', 'Success']

def get_args():
	""" Function to read the system arguments and return a tuple of 
	the 'path' and 'download' arguments respectively
	"""
	defaultpath = 'C:\\XKCD'
	path = defaultpath
	download = 'latest'

	# Checks whether the default path exists and creates it if 
	# necessary.
	# The default path hosts a file named: 'pathfile' which stores
	# the path to the xkcd comics.
	if not os.path.lexists(path):
		os.mkdir(path)
		record_path(path, defaultpath)
	else:
		# Reading the path to the xkcd comics.
		os.chdir(path)
		with open('pathfile', 'rb') as f:
			path = f.readline()
		if not os.path.lexists(path):
			os.mkdir(path)

		os.chdir(path)

	# If the argument is only the file name, return the default
	# values.
	if len(sys.argv) == 1:
		return path, download

	else:
		for i in sys.argv[1:]:
			t = tuple(i.split('='))
			if t[0] == 'path':
				path = t[1]

				# Changes the path where xkcd comics are to be stored
				# as specified by the user comments.
				# Records the path to the file 'pathfile' for future
				#reference
				if not os.path.lexists(path):
					os.mkdir(path)
					record_path(defaultpath, path)
				else:
					record_path(defaultpath, path)
				continue

			elif t[0] == 'download':
				download = t[1]
				continue
		else:
			return path, download

def record_path(filepath, newpath):
	""" Function to record the path to the xkcd comics.

	filepath parameter specifies where the file:'pathfile' exists.
	This should be: 'C:\\XKCD' or the value in defaultpath

	newpath parameter specifies the path to where the xkcd comics are
	to be stored.
	"""

	os.chdir(filepath)
	with open('pathfile', 'wb') as f:
		f.write(newpath.encode('utf-8', 'replace'))

	os.chdir(newpath)

def main():

	path, download = get_args()

	if download == 'latest':
		try:
			pass
		except Exception, e:
			print 'There was a problem: {0}'.format(str(e))

	elif download == 'all':
		try:
			download_comic()
		except Exception, e:
			print 'There was a problem: {0}'.format(str(e))

def download_comic(start='1', end='#'):
	""" Function to download the comics 
	on the xkcd website

	Start parameter specifies the first comic to download and
	end specifies where to stop. If end is a comic number, the
	specified comic will not be downloaded.
	"""

	url = 'http://xkcd.com/{0}'.format(start)
	while not url.endswith(end):

		res = get_resource(url)

		soup = bs4.BeautifulSoup(res.text, "html.parser")

		# Getting the comic number and title 
		comicno = os.path.split(url)[1]
		title = soup.select('#ctitle')[0].getText()

		# Getting the url for the image.
		comicElem = soup.select('#comic img')
		if len(comicElem) > 0:
			try:
				comicurl = 'http:{0}'.format(comicElem[0].get('src'))

				# Download and save the image
				res = download_image(comicUrl)

				update_file('xkcd', comicno, title, STATUS[2])

				# Get the nexk link
				url = get_url(soup)

			except requests.exceptions.MissingSchema:
				update_file('xkcd', comicno, title, STATUS[1])

				# skip this comic
				url = get_url(soup)
				continue
		else:
			print 'Could not find comic image.'
			update_file('xkcd', comicno, title, STATUS[0])

			# skip to the next link
			url = get_url(soup)
			continue

def update_file(filename, *args):
	""" Function to update a file with specific information

	args is the information to be written in the file as per the 
	recording format.
	"""
	with open(filename, 'a+b') as f:
		f.write('{0}***{1}***{2} \n' \
			.format(args[0], args[1], args[2]).encode('utf-8', 'replace'))

def get_url(soupobj, link='next'):
	""" This function returns a link to the previous or next comic

	It takes a BeautifulSoup object as an argument.

	Link argument takes either 'next' or 'prev'.
	"""

	nextLink = soupobj.select('a[rel="{0}"]'.format(link))[0]
	return 'http://xkcd.com{0}'.format(nextLink.get('href')) 

def download_image(url):
	""" This function downloads and saves the image specified
	by the given url.
	"""

	print 'Downloading image {0}...'.format(os.path.basename(url))
	res = get_resource(url)

	with open(os.path.basename(url), 'wb') as imageFile:
		for chunk in res.iter_content(100000):
			imageFile.write(chunk)

def get_resource(url):
	""" Function to download a web resource at the specified url. 
	Example: website, image e.t.c

	It returns a requests object
	"""
	res = requests.get(url)
	try:
		res.raise_for_status()
	except Exception, e:
		raise e

	return res

if __name__ == '__main__':
	main()
