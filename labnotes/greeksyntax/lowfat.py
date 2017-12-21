import os
import sys
from BaseXClient import BaseXClient

from IPython.display import HTML
from pygments import highlight
from pygments.lexers import XmlLexer
from pygments.formatters import HtmlFormatter
from IPython.display import HTML

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
						let $title := attribute title { $s ! (@class, ": ", @lemma, @number, @gender, @case, @tense, @voice, @mood, " - ", @gloss)}
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
							{ attribute title {$w ! (@class, ": ", @lemma, @number, @gender, @case, @tense, @voice, @mood, " - ", @gloss)}}
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
							{ attribute title {@class, ": ", @lemma, @number, @gender, @case, @tense, @voice, @mood, " - ", @gloss}}
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

# TODO: Debug count parameter below.  Works fine if no count is specified.

def interlinear_query_string(query, count):
	if count == 0:
		where = ""
	else:
	    where = """
	    	let $normalized := $w/@normalized
	    	where count(//w[@normalized=$normalized]) <
	    """ + str(count)

	return """
	  <table>
		{
			let $in := """ + query + """
			for $w in $in/descendant-or-self::w """ + where + """
			order by $w/@n
			return
				<tr>
					<td style="text-align:left;">{ string($w) }</td>
					<td style="text-align:left;">{ string($w/@gloss) }</td>
					<td style="text-align:left;">{ string-join($w ! (@class, ": ", @lemma, @number, @gender, @case, @tense, @voice, @mood)," ") }</td>
				</tr>
		}
	  </table>"""



class lowfat:
	session = {}

	def __init__(self, dbname):
		self.session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')
		self.session.execute("open " + dbname)
		print(self.session.info())

	def xquery(self, query):
		try:
			result = self.session.query(query).execute()
		except OSError as err:
			print("Error:", err)
		else:
			if result:
				return result
			else:
				return "No results."

	def find(self, query):
		self.show(self.xquery(morph_query_string(query)))

	def highlight(self, query):
		self.show(self.xquery(highlight_query_string(query)))

	def sentence(self, query):
		self.show(self.xquery(sentence_query_string(query)))

	def interlinear(self, query, count=0):
		self.show(self.xquery(interlinear_query_string(query, count)))

	def show(self, html):
		display(HTML(html))
