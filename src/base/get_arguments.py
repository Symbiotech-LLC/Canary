# -*- coding: utf-8 -*-
"""
Summary:
		This Module will accept command line arguments to drive all activity in other modules
author:
grimm venom <grimmvenom@gmail.com>

"""

import argparse, sys, os
import getpass, re
import base64


def get_arguments():
	parser = argparse.ArgumentParser()
	parser.add_argument('-u', "-url", action='append', dest='url', help='-u <url> \thttp://<url> or https://<URL>')
	parser.add_argument('-f', "-file", action='store', dest='file', help=' -f <filepath.txt> \n.txt file to import a list of urls from. One URL per line. Include http:// or https://')
	parser.add_argument('-base', action='store', dest='base_url', help='-base "http://www.google.com" \nbase url to be prepended to urls without specified base url or don\'t start with http(s)://')
	parser.add_argument('-user', "-username", "-webuser", action='store', dest='web_username', help='--user <username> \nusername for website, you will be prompted for password')
	
	# Option to check url status
	parser.add_argument('-status', action='store_true', dest='status', help='-status \nto verify urls are available')
	# Scrape + Verify Options
	parser.add_argument("-scrape", action='store_true', dest='scrape', help='-scrape \nto scrape and build report of (links, images, form elements')
	parser.add_argument('-verify', action='store_true', dest='verify', help='-verify \nto verify scraped images and links')
	parser.add_argument('--limit', action='append', dest='limit', help='--limit <domain> \nto only check content with specified domain')
	parser.add_argument('--exclude', action='append', dest='exclude', help='--exclude <domain> \nSpecific domains to ignore content for')
	
	parser.add_argument('--excel', action='store_true', dest='excel_output', help='Write Output in Excel format instead of json')
	arguments = parser.parse_args()
	arguments.urls = list()
	
	print("\n")
	
	try:
		arguments.urls = list(arguments.url)
	except:
		pass
	
	if arguments.file:
		f = open(arguments.file, 'r')
		file_urls = f.read().splitlines(keepends=False)
		for url in file_urls:
			if len(url) > 2:
				arguments.urls.append(url)
	
	# If List of Urls is not at least 1, exit
	if len(arguments.urls) < 1:
		parser.error("You must specify a url with the (-u) flag or specify a .txt filepath with 1 url per line with the (-f) flag")
		exit()
		
	if arguments.base_url:
		if arguments.base_url.endswith("/"):
			arguments.base_url = arguments.base_url.replace('/', '', 1)[-1]
			if not arguments.base_url.startswith('http://') and not arguments.base_url.startswith('https://'):
				arguments.base_url = "http://" + arguments.base_url
		print("Base URL: " + str(arguments.base_url))
		for index, url in enumerate(arguments.urls):
			if not url.startswith(arguments.base_url):
				if not url.startswith('http://') and not url.startswith('https://'):
					if url.startswith("/"):
						url = arguments.base_url + url
					else:
						url = arguments.base_url + "/" + url
					arguments.urls[index] = url
	
	if arguments.status:  # If Status is defined, don't scrape and verify content on pages
		arguments.scrape = False
		arguments.verify = False
		
	# Ensure Scrape and Verify Flags work together
	if arguments.verify:  # If verify, auto scrape
		arguments.scrape = True
	if not arguments.status and not arguments.scrape and not arguments.verify:  # if status and verify not selected,
		arguments.scrape = True
	if arguments.scrape:  # If scrape is set, don't do status report
		arguments.status = False
	
	if arguments.web_username:
		arguments.web_password = getpass.getpass('Please enter your authentication\'s Password: ')
	
	return arguments