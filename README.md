# Xkcd-Downloader-python
This is a project written in python intented to download Xkcd comics. 


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

Options
--------

    python xkcd.py path=C:\Users\ download=all
    
"path" variable specifies the folder to save the comics in.

"download" variable specifies whether to download "all" comics or the "latest" comic
(Using "latest" will download all the comics published since you the last comic you downloaded. 
If no prior comics have been downloaded, only the most recent comic will be downloaded.)

Author
------
    Victor Otieno
    vickz84259@gmail.com
    
License
-------
read **LICENSE**

Tasks
-------
- [ ] Add concurrency to speed up the project
- [ ] Create option to download comic by their number
- [ ] Have somebody be able to download comic between a certain specific period
- [ ] Create way to view the comics offline on browser via flask framework

Miscellaneous
-------------
I am open to any suggestions on features and improvements on this project.
