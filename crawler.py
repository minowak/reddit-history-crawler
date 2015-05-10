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
	results = graph.cypher.execute("MATCH (a)-[:`http://xmlns.com/foaf/0.1/name`]->(b) RETURN b")
	return [ r.b.properties['value'] for r in results]

def add_to_db(data):
	tx = graph.cypher.begin()
	for d in data['children']:
		tx.append("TODO QUERY") # TODO

if __name__ == '__main__':
	g = []
	print get_people_from_db()
#	for person in get_people_from_db():
#		person_name = person['name'] # TODO
#		data = search(person_name)
#		for cmt in data:
#			existing_nodes = [n for n in g if n['person'] == person_name]
#
#			if len(existing_nodes) > 0:
#				for e_node in existing_nodes:
#					mentioned_person = {]
#					mentioned_person['id'] = data['data']['id']
#					metioned_person['person'] = person_name
#					e_node['mentioned'].add(mentioned_person)
#					g.add(e_node)
#			
#			node = {}
#			node['id'] = data['data']['id']
#			node['person'] = person_name
#			node['mentioned'] = []
#			g.add(node)

