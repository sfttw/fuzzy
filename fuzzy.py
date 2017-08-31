#!/usr/bin/env python3
'''HTTP Web fuzzer: checks for http://example.com/whatever '''
import urllib.request
import argparse 
import ssl  
import threading
# global variables 
global args
global successful
count = 0
wordlist = []
wordlist_size = 0
successful = []
finished = 0
def url_exists(location):
	request = urllib.request.Request(location)
	request.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:5.0)')
	request.get_method = lambda : 'HEAD'
	ctx = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
	ctx.check_hostname = False
	ctx.verify_mode = ssl.CERT_NONE
	try:
		response = urllib.request.urlopen(request, timeout=5, context=ctx)
		return True
	except Exception as ex:
		if '404' in str(ex):
			if args['verbose']: print('[-] '+location)
			return False
		else:print(ex)


def main(domain='example.com'):
	global args
	global finished
	global wordlist
	try:
		if args['domain']:
			domain = args['domain']
	except:
		print('1')
		pass
	if domain[-1:] != '/': domain+='/'
	if domain[0:4] != "http": domain = "http://" + domain
	while True:
		if len(wordlist) > 0:		
			url = domain + wordlist.pop()
			if url_exists(url):
				if args['verbose']: 
						print('\x1b[6;30;42m [+] ' + url + '\x1b[0m')
				successful.append(url)
			else:			
				pass
		else:
			finished += 1
			break
			

def loadWordlist():
	global wordlist
	global wordlist_size
	
	path = args['wordlist']
	dictionary = open(path).readlines()
	wordlist_size = len(dictionary)
	wordlist = [ word.strip() for word in dictionary ] # remove '\r' and '\n'
	wordlist.reverse()
		
if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Python web fuzzer')
	parser.add_argument('domain', help='target domain')
	parser.add_argument('-l','--logfile', help='File full of target domains', required=False)
	parser.add_argument('-w','--wordlist', help='Wordlist to use', required=False, default='http.txt')
	parser.add_argument('-o','--output', help='Output file', required=False)
	parser.add_argument('-v','--verbose', help='Verbose mode', required=False, action='store_true')
	parser.add_argument('-wp','--wordpress', help='Wordpress mode', required=False, action='store_true')
	parser.add_argument('-t','--threadcount', help='Threadcount', required=False, default=4, type=int)

	
	
	args = vars(parser.parse_args())
	threads = []
	threadcount = int(args['threadcount'])
	loadWordlist()
	
	for i in range(threadcount):
		t = threading.Thread(target=main)
		threads.append(t)
		t.start()

	while True:
		if finished == threadcount:			
			successful.sort()
			print('done!')
			for success in successful: 
				print('\x1b[6;30;42m [+] ' + success + '\x1b[0m')
			if args['output']:
				logfile = open(args['output'], 'a')
				for success in successful: logfile.write(success+'\n')
				logfile.close()
			break


