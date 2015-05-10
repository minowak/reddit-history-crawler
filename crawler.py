import urllib
import json
import sys
from py2neo import Graph, Path, cypher

reddit_page = 'http://www.reddit.com/'
subreddit = 'r/history'
graph = Graph()

def search(query):
	url = reddit_page + subreddit + '/search.json?q=' + query + '&restrict_sr=1'
	response = urllib.urlopen(url)
	data = json.loads(response.read())
	return data

def handle_node(node):
	print node[0]

def get_people_from_db():
	# Is ID necessary? Maybe not
	results = graph.cypher.execute("MATCH (a)-[:`http://xmlns.com/foaf/0.1/name`]->(b) RETURN b")
	return [ r.b.properties['value'] for r in results]

def add_to_db(data, debug=False):
	for node in data:
		cmt_ids = node['cmt_ids']

	tx = graph.cypher.begin()
	for d in data['children']:
		tx.append("TODO QUERY") # TODO

if __name__ == '__main__':
	debug = False
	if len(sys.argv) > 1 and sys.argv[1] == '-v':
		debug = True
	cmts = {}
	
	for person_name in get_people_from_db():
		if debug: print 'Searching reddit mentions for ' + person_name
		data = search(person_name)
		cmt_ids = [ str(d['data']['id']) for d in data['data']['children'] ]
		if debug: print 'Found ' + str(len(cmt_ids)) + ' mentions'
		
		# Save mentions - decreases complexity
		for cmt in cmt_ids:
			if debug: print 'Checking mention with id ' + str(cmt)
			if cmt in cmts:
				if debug: print 'Found! Updating...'
				cmts[cmt].append(person_name)
			else:
				if debug: print 'Not found! Creating new one...'
				cmts[cmt] = [ person_name ]


	print str(cmts)

	# add_to_db(g)
		
