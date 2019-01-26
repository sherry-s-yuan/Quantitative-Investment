import sqlite3
import urllib.error
import ssl
from urllib.parse import urljoin
from urllib.parse import urlparse
from urllib.request import urlopen
from bs4 import BeautifulSoup
import datetime
import random

import TweetStreamAnalysis
import dictionary
import twitter_credential
import textPreprocess
import trainModel

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

conn = sqlite3.connect('spider_url.sqlite')
cur = conn.cursor()

def spider(starturl):
	# Collected String
	paragraphs = ''
	dictionarys = ''
	time = ''
	# establish tables if not exist
	cur.execute('''CREATE TABLE IF NOT EXISTS Pages
		(id INTEGER PRIMARY KEY, url TEXT UNIQUE, html TEXT,
		 error INTEGER, old_rank REAL, new_rank REAL)''')

	cur.execute('''CREATE TABLE IF NOT EXISTS Links
		(from_id INTEGER, to_id INTEGER)''')

	cur.execute('''CREATE TABLE IF NOT EXISTS Webs (url TEXT UNIQUE)''')

	# see if restart spidering
	cur.execute('SELECT id,url FROM Pages WHERE html is NULL and error is NULL ORDER BY RANDOM() LIMIT 1')
	row = cur.fetchone()
	# resume the last search
	if row is not None:
		print("Restarting existing crawl.  Remove spider.sqlite to start a fresh crawl.")
	else:
		web = ['https://www.investors.com/market-trend/stock-market-today/dow-jones-futures-2019-stock-market-rally-apple-stock-amazon-stock/?src=A00239A', 
	   'https://www.investopedia.com/markets/stocks/aapl/#News',
	   'https://ca.finance.yahoo.com/quote/AAPL?p=AAPL',
	   'https://www.thestreet.com/',
	   'https://www.wsj.com/news/markets/stocks',
	   'https://www.msn.com/en-us/money/markets', 
	   'https://seekingalpha.com/market-news/tech']

		# set default goto URL
		if len(starturl) == 0:
			starturl = web[random.randint(0,len(web)-1)]
		# get rid of / at the end of URL
		if(starturl.endswith('/')):
			starturl = starturl[:-1]
		web = starturl
		# extract only the html web
		if(starturl.endswith('.htm') or starturl.endswith('.html')):
			pos = starturl.rfind('/')
			web = starturl[:pos]
		if(len(web) > 1):
			cur.execute('INSERT OR IGNORE INTO Webs (url) VALUES ( ? )', ( web, ) )
			cur.execute('INSERT OR IGNORE INTO Pages (url, html, new_rank) VALUES ( ?, NULL, 1.0 )', ( starturl, ) )
			conn.commit()

	cur.execute('''SELECT url FROM Webs''')
	webs = []
	for row in cur:
		webs.append(str(row[0]))
	print("webs: ",webs)

	num_iteration = 0
	while True:
		paragraphs = ''
		time = ''
		# get number of iteration
		if(num_iteration < 1):
			num_spider = input('retrieve how many pages? (hit enter to cancel): ')
			if(len(num_spider) < 1): break
			try:
				num_iteration = int(num_spider)
			except:
				break
			if(num_iteration == 0): break

		num_iteration -= 1
		cur.execute('SELECT id,url FROM Pages WHERE html is NULL and error is NULL ORDER BY RANDOM() LIMIT 1')
		# check if HTML page can be found
		try:
			row = cur.fetchone()
			fromid = row[0]
			url = row[1]
		except:
			print('No unretrieved HTML pages found')
			many = 0
			break

		print(fromid, url, end=' ')
		# If we are retrieving this page, there should be no links from it
		cur.execute('DELETE from Links WHERE from_id=?', (fromid, ) )
		try:
			# open url and read
			document = urlopen(url, context = ctx)
			html = document.read()
			if document.getcode() != 200 :
				print("Error on page: ",document.getcode())
				cur.execute('UPDATE Pages SET error=? WHERE url=?', (document.getcode(), url) )

			# Ignore non text/html page
			if 'text/html' != document.info().get_content_type() :
				print("Non text/html page ignored")
				cur.execute('DELETE FROM Pages WHERE url=?', ( url, ) )
				cur.execute('UPDATE Pages SET error=0 WHERE url=?', (url, ) )
				conn.commit()
				continue

			print('('+str(len(html))+')', end=' ')
			soup = BeautifulSoup(html, "html.parser")
		# if program interupted by user
		except KeyboardInterrupt:
			print('')
			print('Program interupted...')
			break
		#unknown error
		except:
			print("Unable to retrieve...")
			cur.execute('UPDATE Pages SET error=-1 WHERE url=?', (url, ) )
			conn.commit()
			continue

		cur.execute('INSERT OR IGNORE INTO Pages (url, html, new_rank) VALUES ( ?, NULL, 1.0 )', ( url, ) )
		cur.execute('UPDATE Pages SET html=? WHERE url=?', (memoryview(html), url ) )
		conn.commit()

		# retrieve all anchor tags
		a_tags = soup('a')
		p_tags = soup('p')
		time_tags = soup('time')
		count = 0
		for tag in a_tags:
			href = tag.get('href', None)
			if(href == None): continue
			up = urlparse(href)
			if(len(up.scheme) < 1):
				href = urljoin(url, href)
			ipos = href.find('#')
			if ipos > 1 : href = href[:ipos]
			if href.endswith('.png') or href.endswith('.jpg') or href.endswith('.jpeg') or href.endswith('.gif') or href.endswith('.pdf'): continue
			if href.endswith('/') : href = href[:-1]
			if len(href) < 1 : continue

			found = False
			# only save website in the same domain as the starturl
			for web in webs:
				if(href.startswith(web)):
					found = True
					break
			if not found: continue

			cur.execute('INSERT OR IGNORE INTO Pages (url, html, new_rank) VALUES ( ?, NULL, 1.0 )', ( href, ) )
			count = count + 1
			conn.commit()

			cur.execute('SELECT id FROM Pages WHERE url=? LIMIT 1', ( href, ))
			try:
				row = cur.fetchone()
				toid = row[0]
			except:
				print('Could not retrieve id')
				continue
			# print fromid, toid
			cur.execute('INSERT OR IGNORE INTO Links (from_id, to_id) VALUES ( ?, ? )', ( fromid, toid ) )
	
		print(count)

		# append collected string
		for tag in p_tags:
			tag_string = tag.string
			if tag_string != None and if_add_string_to_csv(tag_string):
				tag_string = tag_string.lower()
				dictionarys += tag_string
				#if tag_string.lower():
				paragraphs += tag_string
		#print(paragraphs)
		if len(time_tags) != 0:
			time = time_tags[0]['datetime']
		else:
			time = str(datetime.datetime.now())

		if len(paragraphs) > 0:
			paragraphs = textPreprocess.preprocess(paragraphs.lower())		
			print("Added Paragraph: ", paragraphs)
			TweetStreamAnalysis.news_streaming(paragraphs, time)
		#print("time",time)

	cur.close()
	if len(dictionarys) > 0:
		if dictionary.expand_by_spidering(textPreprocess.preprocess(dictionarys.lower())):
			trainModel.r_nr()
			trainModel.bull_bear()
	#return paragraphs

def if_add_string_to_csv(paragraphs):
	for track in twitter_credential.track:
		if track in paragraphs:
			return True
	return False

#spider()

