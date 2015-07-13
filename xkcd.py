#! python2
# xkcd.py - Downloads comics from xkcd.com.
#
# Takes 2 optional arguments when launched from the command line
# which in default are "download=latest" and 
# "path=C:\Users\risper.omondi\Desktop\XKCD"
#
# 'download' argument specifies whether to download the 'latest' or
# 'all' XKCD comics
# Using "latest" will download all the comics published since you 
# the last comic you downloaded. If no prior comics have been downloaded, 
# only the most recent comic will be downloaded.
#
#
# 'path' argument specifies the path where to save the comics

import requests, os, bs4, sys

def get_args():
	""" Function to read the system arguments and return a tuple of 
	the 'path' and 'download' arguments respectively
	"""
	path = 'C:\\Users\\risper.omondi\\Desktop\\XKCD'
	download = 'latest'

	# If the argument is only the file name, return the default
	# values.
	if len(sys.argv) == 1:
		return path, download

	else:
		for i in sys.argv[1:]:
			t = tuple(i.split('='))
			if t[0] == 'path':
				path = t[1]
				continue
			elif t[0] == 'download':
				download = t[1]
				continue
		else:
			return path, download


def main():
	website = 'http://xkcd.com'

	path, download = get_args()
	os.chdir(path)

	# Opening the file that lists the xkcd comics 
	# already downloaded.
	with open('xkcd', 'a+b') as statusfile:
		if download == 'latest':
			pass

		elif download == 'all':
			try:
				download_all(website, statusfile)
			except Exception, e:
				print 'There was a problem: {0}'.format(str(e))
			

def download_all(url, stats):
	""" Function to download all of the comics 
	on the xkcd website
	"""
	url = 'http://xkcd.com/1/'
	while not url.endswith('#'):
		# Getting the webpage
		print 'Downloading page {0}...'.format(url)
		res = requests.get(url)
		try:
			# Check whether the website is received successfully 
			# and raises and exception if an error occurs
			res.raise_for_status()
		except Exception, e:
			raise e

		soup = bs4.BeautifulSoup(res.text, "html.parser")

		title = soup.select('#ctitle')[0].getText()

		# Getting the url for the image.
		comicElem = soup.select('#comic img')
		if comicElem == []:
			print 'Could not find comic image.'

			stats.write('{0}--{1}--Comic image not found \n'.format(title, url))

			# skip to the next link
			url = get_next(soup)
			continue
		else:
			try:
				comicUrl = 'http:{0}'.format(comicElem[0].get('src'))

				# Download the image.
				res = download_image(comicUrl)

			except requests.exceptions.MissingSchema:
				stats.write('{0}--{1}--Error downloading \n'.format(title, url))

				# skip this comic
				url = get_next(soup)
				continue

		# Save the image to path
		save_image(res, stats, title, comicUrl)

		# Get the Prev button's url
		url = get_next(soup)

def get_next(soupobj):
	""" This function returns a link to the previous comic

	It takes a BeautifulSoup object as an argument
	"""

	nextLink = soupobj.select('a[rel="next"]')[0]
	return 'http://xkcd.com' + nextLink.get('href')

def download_image(imgurl):
	""" This function downloads the image.

	It returns a requests object.
	"""

	print 'Downloading image {0}...'.format(imgurl)
	res = requests.get(imgurl)
	try:
		res.raise_for_status()
	except Exception, e:
		raise e

	return res

def save_image(req, statusfile, comictitle, name):
	""" This function takes a requests object and a file object as
	parameters.

	The file object is used to keep a record of the image being saved.
	"""
	with open(os.path.basename(name), 'wb') as imageFile:
		for chunk in req.iter_content(100000):
				imageFile.write(chunk)

	statusfile.write('{0}--{1}--Sucess \n'.format(comictitle, name))


if __name__ == '__main__':
	main()
