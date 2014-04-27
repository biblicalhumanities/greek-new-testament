<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="3.0">

    <xsl:template match="Sentences/Sentence">
        <xsl:text/>
        <xsl:text>Sentence: </xsl:text>
        <xsl:value-of select="./@ID"/>
        <xsl:apply-templates/>
        <xsl:text/>
    </xsl:template>

    <xsl:template match="Node">
        <xsl:text>[</xsl:text>
        <xsl:value-of select="./@Cat"/>
        <xsl:text> </xsl:text>
        <xsl:apply-templates/>
        <xsl:text>]</xsl:text>
    </xsl:template>

</xsl:stylesheet>
