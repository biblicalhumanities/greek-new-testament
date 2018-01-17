import os
import sys
from BaseXClient import BaseXClient
from IPython.display import HTML



class csv:
	session = {}

	def __init__(self, dbname):
		self.session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')
		self.session.execute("open " + dbname)
		print(self.session.info())

	def xquery(self, query):
		collation = "declare default collation 'http://basex.org/collation?lang=el;strength=secondary';\n"
		query = collation + query
		try:
			result = self.session.query(query).execute()
		except OSError as err:
			print("Error:", err)
		else:
			if result:
				return result
			else:
				return "No results."

	def count(self, query):
		self.show(self.xquery('count(' + query + ')'))

	def show(self, html):
		display(HTML(html))
