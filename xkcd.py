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
import os, sys, ConfigParser, argparse, logging

# Third-party modules
import requests, bs4

# Project-specific modules

# Defining Constants
STATUS = ['Image not found', 'Error downloading', 'Success']

# Constant defining the current comic
CURRENT_COMIC = ''

logging.basicConfig(filename='xkcd.log', level=logging.INFO,
	format='%(levelname)s:%(message)s')

def create_config():
	config = ConfigParser.ConfigParser()
	config.add_section('Defaults')
	config.set('Defaults', 'path', 'C:\\XKCD')

	with open('xkcd.cfg', 'wb') as configfile:
		config.write(configfile)

	return config

def get_args():
	if not os.path.lexists('xkcd.cfg'):
		config = create_config()
	else:
		config = ConfigParser.ConfigParser()
		config.read('xckd.cfg')

	parser = argparse.ArgumentParser(
		formatter_class=argparse.RawDescriptionHelpFormatter,
		description=textwrap.dedent('''\
			Examples on how to use the program
			----------------------------------
			python xkcd.py --path C:\\Users\\admin\\Desktop\\xkcd --all
				**all xkcd comics will be saved in path described

			python xkcd.py comic --number 158
				**downloads comic number 158

			python xkcd.py range --number 300 #
				**downloads all comics from comic number 300
					to the latest one. Inclusive of the latest one.

			python xkcd.py --latest
				**
			'''))
	# Creating sub commands to be used
	subparsers = parser.add_subparsers()
	# comic command
	parser_comic = subparsers.add_parser('comic', 
		help='Download a specific comic')
	# range command 
	parser_range = subparsers.add_parser('range',
		help='Download a range of comics')

	parser.add_argument('-p', '--path', default=config.get('Defaults', 'path'),
		help='The folder where the xkcd comics will be saved\
				(default: %(default)s)')

	# Only one of the arguments can be present in the command line.
	group = parser.add_mutually_exclusive_group()
	group.add_argument('-l', '--latest', action='store_true',
		help='Downloads the latest comic if there are no previously\
			downloaded comics. Otherwise it downloads all the\
			comics since the last one that was downloaded.')

	group.add_argument('-a', '--all', action='store_true',
		help='Downloads all xkcd comics.')

	group.parser_comic.add_argument('-n', '--number', dest='comic_number',
		default=argparse.SUPPRESS,
		help='The comic number to be downloaded.')

	group.parser_range.add_argument('-r', '--range', dest='comic_range',
		default=argparse.SUPPRESS, nargs=2, 
		help='Download the range of comics. e.g. --range 30 100\
		  # represents the latest comic.')

	args = parser.parse_args()

	if args.path != config.get('Defaults', 'path') and (not os.path.lexists(args.path)):
		os.mkdir(args.path)
		config.set('Defaults', 'path', args.path)
		os.chdir(args.path)
	else:
		os.chdir(config.get('Defaults', 'path')

	return args

def main():

	args = vars(get_args())

	if args['latest']:
		try:
			pass
		except Exception, e:
			logging.exception()
			print 'There was a problem: {0}'.format(str(e))

	elif args['all']:
		try:
			download_comic()
		except Exception, e:
			logging.exception()
			print 'There was a problem: {0}'.format(str(e))

def download_comic(start='1', end='#'):
	""" Function to download the comics 
	on the xkcd website

	Start parameter specifies the first comic to download and
	end specifies where to stop. If end is a comic number, the
	specified comic will not be downloaded.
	"""
	global CURRENT_COMIC
	CURRENT_COMIC = start
	url = 'http://xkcd.com/{0}'.format(start)

	while not url.endswith(end):

		res = get_resource(url)

		soup = bs4.BeautifulSoup(res.text, "html.parser")

		# Getting the url for the image.
		comicElem = soup.select('#comic img')
		if len(comicElem) > 0:
			try:
				comicurl = 'http:{0}'.format(comicElem[0].get('src'))

				# Download and save the image
				res = download_image(comicUrl)

				# Get the nexk link
				url = get_next_url()

			except requests.exceptions.MissingSchema:
				logging.error('{0}: {1}'.format(CURRENT_COMIC, STATUS[1]))

				# skip this comic
				url = get_next_url()
				continue
		else:
			logging.error('{0}: {1}'.format(CURRENT_COMIC, STATUS[0]))

			# skip to the next link
			url = get_next_url()
			continue

	logging.info('{0}--{1}: {2}'.format(start, end, STATUS[2]))

def get_next_url(ascending=True):
	global CURRENT_COMIC

	if ascending:
		CURRENT_COMIC += 1
	else:
		CURRENT_COMIC -= 1

	return 'http://xkcd.com/{0}'.format(CURRENT_COMIC) 

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
