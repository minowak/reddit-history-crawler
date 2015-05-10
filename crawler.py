import urllib
import json
import sys
from py2neo import Graph, Path, cypher, rel

reddit_page = 'http://www.reddit.com/'
subreddit = 'r/history'
graph = Graph()

def search(query, debug=False):
	data = {}
	while 'data' not in data:
		if debug: print 'Querying reddit API'
		url = reddit_page + subreddit + '/search.json?q=' + query + '&restrict_sr=1'
		response = urllib.urlopen(url)
		data = json.loads(response.read())
	return data

def get_people_from_db():
	results = graph.cypher.execute("MATCH (a)-[:`http://xmlns.com/foaf/0.1/name`]->(b) RETURN b")
	return results

def add_to_db(data, results, debug=False):
	if debug: print 'Started adding relations to DB'
	for cmt in data.keys():
		if debug: print ' * for ' + cmt + ' (' + str(len(data[cmt])) + 'mentions)'
		if len(data[cmt]) > 1:
			for i in range(0, len(data[cmt]) - 2):
				name1 = data[cmt][i]
				name2 = data[cmt][i+1]
		
				if debug: print 'Adding relation between ' + name1 + ' and ' + name2

				node1 = [ r.b.properties['value'] for r in results if r.b.properties['value'] == name1 ]
				node2 = [ r.b.properties['value'] for r in results if r.b.properties['value'] == name2 ]

				graph.create(rel(node1, "MENTIONED", node2))
				graph.create(rel(node2, "MENTIONED", node1))
				if debug: print ' + Done!'
		else:
			if debug: print '  - not needed'

if __name__ == '__main__':
	debug = False
	if len(sys.argv) > 1 and sys.argv[1] == '-v':
		debug = True
	cmts = { }

	results = get_people_from_db()
	ppl = [ r.b.properties['value'] for r in results ]
	
	for person_name in ppl:
		if debug: print 'Searching reddit mentions for ' + person_name
		data = search(person_name, debug)
		cmt_ids = [ str(d['data']['id']) for d in data['data']['children'] ]
		if debug: print 'Found ' + str(len(cmt_ids)) + ' mentions'
		
		# Save mentions - decreases complexity
		for cmt in cmt_ids:
			if debug: print 'Checking mention with id ' + str(cmt)
			if cmt in cmts:
				if debug: print 'Found! Updating...'
				if person_name not in cmts[cmt]:
					cmts[cmt].append(person_name)
			else:
				if debug: print 'Not found! Creating new one...'
				cmts[cmt] = [ person_name ]


	add_to_db(cmts, results, debug)

	print 'Done.'
		
