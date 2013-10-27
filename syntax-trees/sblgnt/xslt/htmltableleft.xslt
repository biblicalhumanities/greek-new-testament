<?xml version="1.0" encoding="UTF-8"?>
<!--
     Possible strategy: each node works down and to the right, first child lands to the right as well.
     Keep track of indent level = node depth.
     Words always to the far right.
     -->
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">

    <xsl:strip-space elements="*"/>

    <xsl:template match="/">
      <html>
	<head>
	  <meta charset="UTF-8"/>
	  <style type="text/css">
	    table { 
	      border-top: 1px solid grey;
	      border-right: 1px solid grey;
	      border-bottom: 1px solid grey;	      
	      text-align: left;
	      align: left;
	    }
	    td {
	      align: right;
	    }
	    .text {
	      color: blue;	      
	      text-align: left;
	      align: left;
	      font-size: 150%;
	      width: 15em;
	      display: inline;
	    }
	    .analysis {
	      text-align: center;
	      display: inline;
	    }
	  </style>
	</head>
	<h1>Greek New Testament Syntax Trees (SBLGNT)</h1>

	<p><a href="./index.html">[Table of Contents]</a></p>

	<p>Hover mouse over blue Greek text for morphology.</p>


	<p>HTML rendering copyright 2013 by biblicalhumanities.org,  made available under under a [CC-BY-SA License] (<a href="http://creativecommons.org/licenses/by-sa/3.0/">http://creativecommons.org/licenses/by-sa/3.0/</a>).
Created from Asia Bible Society syntax diagram markup (<a href="https://github.com/biblicalhumanities/greek-new-testament/syntax-trees/sblgnt">https://github.com/biblicalhumanities/greek-new-testament/syntax-trees/sblgnt</a>), 
copyright 2013 by the Asia Bible Society, made available under under a [CC-BY-SA License] (<a href="http://creativecommons.org/licenses/by-sa/3.0/">http://creativecommons.org/licenses/by-sa/3.0/</a>). 

Morphological parsing and lemmatization copyright 2013 by MorphGNT,  made available under a [CC-BY-SA License](<a href="http://creativecommons.org/licenses/by-sa/3.0/">http://creativecommons.org/licenses/by-sa/3.0/</a>).  

SBLGNT text copyright 2010 by the Society of Biblical Literature and Logos Bible Software, use subject to the [SBLGNT EULA](<a href="http://sblgnt.com/license/">http://sblgnt.com/license/</a>).
         </p>

	<xsl:apply-templates/>
      </html>
    </xsl:template>

    <xsl:template match="Sentences/Sentence">
	<h1>
	  <xsl:value-of select="./@ID"/>
	</h1>
	<xsl:apply-templates/>
    </xsl:template>

    <xsl:template match="Node">
      <table>
	<tr>
	  <td>
	    <xsl:apply-templates/>
	  </td>
	  <td>
	    <xsl:if test="text()">
	        <xsl:attribute name="title">
		  <xsl:value-of select="normalize-space(concat(@UnicodeLemma,' ',@Tense,' ',@Voice,' ',@Mood,' ',@Case,' ',@Number,' ',@Gender))"/>
		</xsl:attribute>
		<p class="text">
		  <xsl:value-of select="text()"/>
		</p>
	    </xsl:if>
	    <p class="analysis">
	      <xsl:value-of select="./@Cat"/>
	    </p>
	  </td>
	</tr>
      </table>
    </xsl:template>

    <xsl:template match="text()"/>

</xsl:stylesheet>
