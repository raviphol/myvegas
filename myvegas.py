import urllib
import sys
import urllib2
import webbrowser
from json import loads
from time import sleep, time

access_token = sys.argv[1]
last_created_time = int(time())

def refresh():
	global last_created_time
	query = "SELECT message, attachment, created_time FROM stream WHERE source_id=518895678148586 AND created_time > " + str(last_created_time)
	params = urllib.urlencode({'q': query, 'access_token': access_token})

	url = "https://graph.facebook.com/fql?" + params
	data = loads(urllib.urlopen(url).read())
	links = set()
	if 'data' in data:
		for record in data['data']:
			msg, attachment, created_time = record['message'], record['attachment'], record['created_time']
			tok_msgs = [mm for m in msg.split('\n') for mm in m.split()]
			if 'href' in attachment:
				temp = attachment['href'][attachment['href'].find('://'):]
				if not 'http' + temp in tok_msgs and not 'https' + temp in tok_msgs:
					tok_msgs.append(attachment['href'])
			for tok in tok_msgs:
				if len(tok) > 30 and tok.find('://apps.facebook.com/playmyvegas/award/feed/') >= 0:
					links.add(tok)
					webbrowser.open_new_tab(tok)
			last_created_time = max(last_created_time, created_time)
	else:
		print data

while True:
	refresh()
	sleep(2)