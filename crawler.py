import urllib
import json
import sys
from py2neo import Graph, Path

reddit_page = 'http://www.reddit.com/'
subreddit = 'r/history'

def search(query):
	url = reddit_page + subreddit + '/search.json?q=' + query + '&restrict_sr=1'
	response = urllib.urlopen(url)
	data = json.loads(response.read())
	return data

def add_to_neo4j(data):
	graph = Graph()
	tx = graph.cypher.begin()
	for d in data:
		tx.append("TODO QUERY")

if __name__ == '__main__':
	if len(sys.argv) < 2:
		print 'Usage: ' + sys.argv[0] + ' <query>'
	else:
		data = search(sys.argv[1])
		print data

