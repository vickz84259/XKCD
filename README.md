# Xkcd-python
This is a project written in python intented to download Xkcd comics. 

I wrote it as a project a beginner would be involved in.

What is [xkcd](http://xkcd.com)?
-------------
It is a webcomic created Randall Munroe. The subject matter of the comic varies from 
statements on life and love to mathematical and scientific in-jokes.
You can view the comics at http://xkcd.com

Prerequisites
-------------
The project is written for python 2.7. Support for python 3 will be included later on.

Libraries Used
--------------
The project currently uses the following external python libraries

    1. Requests - For downloading files and webpages 
    2. Beautiful Soup - For parsing HTML

Check out the documentations of the above libraries if you are not familiar with how
they are used.

[Requests Documentation](http://docs.python-requests.org) 

[Beautiful Soup Documentation](http://www.crummy.com/software/BeautifulSoup/bs4/doc/)

Installation
------------
To use this project and prevent conflict with other projects, it is recommended that you use **virtualenv** 

For those who might not know, **virtualenv** (as the name suggests), allows you to create a python virtual environment where you can install modules in a specific environment and not system-wide where it can cause conflicts.

For users starting out using **virtualenv**, get **virtualenvwrapper**
alongside **virtualenv** and the process of maintaining the virtual environments will be easier. (**personal opinion**)

For Windows users you can get **virtualenvwrapper-win**

**Assumption**
You already have **pip** and **setuptools** installed.

Once in your virtual environment, Enter:
	
	pip install requests

This installs the requests module.

	pip install beautifulsoup4

This installs the beautiful soup module.

Usage
------
(If you installed the external libraries in a virtual environment, 
navigate to the project's location and activate the virtual environment before executing the command below.)
Navigate to the project's location on the repository that you have cloned on your computer 
and execute:

    python xkcd.py
    
This will download the latest comic from [xkcd](http://xkcd.com)

Examples on how to use the program
----------------------------------

	python xkcd.py --path C:\Users\admin\Desktop\xkcd --all
**all xkcd comics will be saved in path described**

	python xkcd.py -n 158
**downloads comic number 158**

	python xkcd.py --range 300 #
**downloads all comics from comic number 300 to the latest one. Inclusive of the latest one.**

	python xkcd.py --range 4 100
**downloads the comics between 4 and 100. Including both the comics numbered 4 and 100**

Command-Line options
--------

	-p <path>, --path <path>
**The path where comics will be downloaded**

	-l, --latest
**Downloads the latest comic if there are no previously downloaded comics. Otherwise it downloads all the comics since the last one that was downloaded**

	-a, -all
**Downloads all xkcd comics**

	-n 
**Downloads the comic specified by the number**

	--range
**Download the comics in the specified range**

Author
------
    Victor Otieno
    vickz84259@gmail.com
    
License
-------
read **LICENSE**

Miscellaneous
-------------
If you have any issue, feature request or you want to report a bug; please open an issue about it.

Feel free to fork out and improve on the code. When done, do a pull request and I will get back to you