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

Usage
------
Navigate to the project's location on the repository that you have cloned on your computer 
and execute:

    python xkcd.py 
    
This will download the latest comic from [xkcd](http://xkcd.com)

Options
--------

    python xkcd.py path="C:\\Users\" download="all"
    
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
- [ ] Create option to download comic by their number
- [ ] Have somebody be able to download comic between a certain specific period
- [ ] Create way to view the comics offline on browser via flask framework

Miscellaneous
-------------
I am open to any suggestions on features and improvements on this project.
