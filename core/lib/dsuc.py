import requests 
import bs4 
import argparse

external = []
unknown =  []

def extractor(soup , host) : 
	all_links = list()
	for link in soup.find_all('a' , href = True) :
		if link['href'].startswith('/') : 
			if link['href'] not in all_links : 
				all_links.append(host+link['href'])
		elif host in link['href'] : 
			if link['href'] not in all_links : 
				all_links.append( link['href'] )
		elif 'http://' in host : 
			if 'https://'+host.split('http://')[1] in link['href'] and link['href'] not in all_links: 
					all_links.append( link['href'] )
		elif 'http' not in link['href'] and 'www' not in link['href'] and len(link['href']) > 2 and '#' not in  link['href'] : 
			if link['href'] not in all_links : 
				all_links.append(host+'/'+link['href'])
		elif len (link['href']) > 6 : 
			external.append( link['href'] )
		else : 
			unknown.append( link['href'] )
	return all_links
	
def fuzzable_extract(linklist):
	fuzzables = []
	for link in linklist : 
		if "=" in link : 
			fuzzables.append(link)
	return fuzzables 	
def xploit(link , host = None) : 
	if host is None : 
		host = link
	try : 
		res = requests.get(link , allow_redirects=True)
		soup = bs4.BeautifulSoup(res.text , 'lxml')
		return extractor(soup , host)
	except :
		return []
	
def r3dxtractor(linklist , host) : 
	final_list = list()
	try :
		for link in linklist :
			print('[VERBOSE] [STATUS] CRAWLING INSIDE : ' , link)
			for x in xploit(link , host) :
				if x not in final_list : 
						final_list.append(x)
						print("[VERBOSE] [STATUS] Appended : " , x)
			if link not in final_list : 
				final_list.append(link)
		return final_list
	except : 
		return final_list