import os
from BaseXClient import BaseXClient

from IPython.display import HTML
from pygments import highlight
from pygments.lexers import XmlLexer
from pygments.formatters import HtmlFormatter
from IPython.display import HTML

session = {}

def __init__():
	global session = session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')
	session.execute("open nestle1904lowfat")


	# def boxwood(self, xml):
	#     display(HTML('<style type="text/css">{}{}{}</style>{}'.format(
	#         "hit { display: block; margin-top: 2em; }",
	#         open('css/treedown.css').readlines(),
	#         open('css/boxwood.css').readlines(),
	#         xml)))

def xquery(query):
    return session.query(query).execute()

def sentence(query):
    q = r"""
       for $h in """ + query + """
       let $sentence := $h/ancestor::sentence
       return
          <p>
            <b>{ $sentence/milestone ! string(.)}</b>
            <br/>
            { $sentence/p ! string(.)}
            <br/>
            { "➡️" }
            {
                for $w in $h/descendant-or-self::w
                order by $w/@n
                return $w ! string(.)
            }
          </p>"""
    display(HTML(xquery(q)))

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
                  <w>
                    { attribute title {$w ! (@class, ": ", @lemma, @number, @gender, @case, @tense, @voice, @mood)}}
                    { $w ! string(.) }
                  </w>
            }
          </p>"""

def milestone(m):
    if m.count("!") == 1:
        return "//w[@osisId='" + m + "']"
    elif m.count(".") == 2:
        return "//sentence[milestone[@id='" + m + "']]"
    else:
        return "//sentence[milestone[starts-with(@id,'" + m + "')]]"

def find(query):
    display(HTML(xquery(morph_query_string(query))))

def wrap(query):
	return "<results xmlns:xi='http://www.w3.org/2001/XInclude'>{" + query + "}</results>"

def raw(query):
    print(xquery(wrap(query)))

def pretty(query):
    formatter = HtmlFormatter()
    display(
        HTML('<style type="text/css">{}</style>{}'.format (
            formatter.get_style_defs('.highlight'),
            highlight(xquery(wrap(query)), XmlLexer(), formatter))))
