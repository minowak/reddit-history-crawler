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

def get_people_from_db()
	# TODO
	return []

def add_to_db(data):
	graph = Graph()
	tx = graph.cypher.begin()
	for d in data['children']:
		tx.append("TODO QUERY") # TODO

if __name__ == '__main__':
	g = []
	for person in get_people_from_db():
		peron_name = person['name'] # TODO
		data = search(person_name)
		for cmt in data:
			existing_nodes = [n for n in g if n['person'] == person_name]

			if len(existing_nodes) > 0:
				for e_node in existing_nodes:
					mentioned_person = {]
					mentioned_person['id'] = data['data']['id']
					metioned_person['person'] = person_name
					e_node['mentioned'].add(mentioned_person)
					g.add(e_node)
			
			node = {}
			node['id'] = data['data']['id']
			node['person'] = person_name
			node['mentioned'] = []
			g.add(node)

