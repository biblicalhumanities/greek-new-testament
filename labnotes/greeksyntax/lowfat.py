import os
from BaseXClient import BaseXClient

from IPython.display import HTML
from pygments import highlight
from pygments.lexers import XmlLexer
from pygments.formatters import HtmlFormatter
from IPython.display import HTML

def wrap(query):
	return "<results xmlns:xi='http://www.w3.org/2001/XInclude'>{" + query + "}</results>"

def pretty(xml):
	formatter = HtmlFormatter()
	display(
		HTML('<style type="text/css">{}</style>{}'.format (
			formatter.get_style_defs('.highlight'),
			highlight(xml, XmlLexer(), formatter))))

def milestone(m):
	if m.count("!") == 1:
		return "//w[@osisId='" + m + "']"
	elif m.count(".") == 2:
		return "//sentence[milestone[@id='" + m + "']]"
	else:
		return "//sentence[milestone[starts-with(@id,'" + m + "')]]"


def highlight_query_string(query):
	return r"""
		for $h in """ + query + r"""
		let $sentence := $h/ancestor::sentence
		let $sentencewords :=
				for $w in $sentence/descendant-or-self::w
				order by $w/@n
				return $w
		let $hitwords :=
				for $w in $h/descendant-or-self::w
				order by $w/@n
				return $w
		return
				<p>
					<b>
					{
						$sentence/milestone/@id ! string(.)
					}
					</b>
					<br/>
					{
						for $s in $sentencewords
						let $title := attribute title { $s ! (@class, ": ", @lemma, @number, @gender, @case, @tense, @voice, @mood)}
						let $content := string-join(($s, $s/following-sibling::*[1][local-name(.)='pc']),"")
						return
							if ($s/@n = $hitwords/@n)
								then <span style="color:red">{ $title, $content }</span>
								else <span>{ $title, $content }</span>
					}
				</p>"""

def morph_query_string(query):
	return r"""
		for $h in """ + query + r"""
		let $words := $h/descendant-or-self::w
		return
			<p>
				<b>
				{
					$words[@n=min($words/@n)]/@osisId ! string(.)
				}
				</b>
				{" "}
				{
					for $w in $words
					order by $w/@n
					return
						<span>
							{ attribute title {$w ! (@class, ": ", @lemma, @number, @gender, @case, @tense, @voice, @mood)}}
							{ $w ! string-join((., following-sibling::*[1][local-name(.)='pc']),"") }
						</span>
				}
			</p>"""


def sentence_query_string(query):
	return r"""
		for $h in """ + query + r"""
		let $sentence := $h/ancestor::sentence
		let $sentencewords :=
				for $w in $sentence/descendant-or-self::w
				order by $w/@n
				return $w
		let $hitwords :=
				for $w in $h/descendant-or-self::w
				order by $w/@n
				return $w
		return
			<p>
				<b>
				{
					$sentence/milestone/@id ! string(.)
				}
				</b>
				{" "}
				{
					$sentencewords !
						<span>
							{ attribute title {@class, ": ", @lemma, @number, @gender, @case, @tense, @voice, @mood}}
							{ string-join((., following-sibling::*[1][local-name(.)='pc']),"") }
						</span>
				}
				<br/>
				{ "➡️ " }
				<b>{ $hitwords[1]/@osisId ! string(.) }</b>
				{ " " }
				{
					$hitwords ! string-join((., following-sibling::*[1][local-name(.)='pc']),"")
				}
			</p>"""

class lowfat:
	session = {}

	def __init__(self, dbname):
		self.session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')
		self.session.execute("open " + dbname)

	def xquery(self, query):
		return self.session.query(query).execute()

	def find(self, query):
		display(HTML(self.xquery(morph_query_string(query))))

	def highlight(self, query):
		display(HTML(self.xquery(highlight_query_string(query))))

	def html(self, query):
		print(HTML(self.xquery(highlight_query_string(query))))

	def raw(self, m):
		print(self.xquery(
			"<results xmlns:xi='http://www.w3.org/2001/XInclude'>{"
			   + milestone(m)
			+"}</results>"))

	def sentence(self, query):
		display(HTML(self.xquery(sentence_query_string(query))))
