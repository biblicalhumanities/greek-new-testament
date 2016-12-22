<?xml version="1.0" encoding="UTF-8"?>
<!--
* TODO: Milestones for chapter, verse
* TODO: Chunk by chapter
* DONE: Mark incontinuity
* DONE: Highest categorization
* TODO: HTML5 conversion
* TODO: CSS Stylesheets to offer different views of text (customizable)
-->
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema" exclude-result-prefixes="xs" version="3.0">

    <xsl:output method="xml" encoding="utf-8" indent="yes"/>

    <xsl:variable name="clause-level-roles" select="('ADV', 'IO', 'O', 'O2', 'P', 'S', 'V', 'VC')"/>     

    <xsl:template match="/">
        <xsl:processing-instruction name="xml-stylesheet">href="pruned-tree.css"</xsl:processing-instruction>
        <book>
            <xsl:apply-templates/>
        </book>
    </xsl:template>

    <xsl:template match="Sentence">
        <sentence>
          <cite>
            <xsl:value-of select="@ID"/>
          </cite>
          <xsl:apply-templates/>
        </sentence>
    </xsl:template>


    <xsl:template match="Node">
        <p>#### If you see this in output, there's a bug that needs fixing ####</p>
    </xsl:template>

    <xsl:template match="Node[count(*) = 1]">
        <xsl:apply-templates/>
    </xsl:template>

    <xsl:template name="role">
        <xsl:param name="node" as="element(Node)"/>
        <xsl:choose>
            <xsl:when test="count($node/parent::Node/*) = 1 and lower-case(parent::*/@Cat) != 'cl'">
                <xsl:call-template name="role">
                    <xsl:with-param name="node" select="$node/parent::*"/>
                </xsl:call-template>
            </xsl:when>
            <xsl:otherwise>
              <xsl:if test="$node/@Cat = $clause-level-roles">
                <xsl:variable name="cat" select="lower-case($node/@Cat)"/>
                <xsl:attribute name="role" select="$cat"/>
              </xsl:if>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>


    <xsl:template name="head">
        <xsl:param name="node" as="element(Node)"/>
        <xsl:param name="node-position" select="count($node/preceding-sibling::Node)"/>
        <xsl:variable name="parent" as="element(Node)?" select="$node/parent::Node"/>
        <xsl:variable name="siblings" as="element(Node)*" select="$node/preceding-sibling::Node | $node/following-sibling::Node"/>
        <xsl:choose>
            <xsl:when test="count($siblings) gt 0">
                <xsl:choose>
                    <xsl:when test="$node-position = $parent/@Head and $parent/@Cat != 'conj'">
                        <xsl:attribute name="head">true</xsl:attribute>
                    </xsl:when>                  
                </xsl:choose>
            </xsl:when>                
            <xsl:otherwise>                              
                <xsl:if test="$parent">
                    <xsl:call-template name="head">            
                        <xsl:with-param name="node" select="$parent"/>
                    </xsl:call-template>
                </xsl:if>                    
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>


    <xsl:template match="Node[count(*) >1]">
        <wg>
            <xsl:copy-of select="@nodeId"/>
            <xsl:attribute name="class" select="lower-case(@Cat)"/>
            <xsl:call-template name="role">
                <xsl:with-param name="node" select="."/>
            </xsl:call-template>
	<!--
	  Word groups probably don't need heads.

            <xsl:call-template name="head">
                <xsl:with-param name="node" select="."/>
            </xsl:call-template>
	-->

            <xsl:apply-templates/>
        </wg>
    </xsl:template>

    <xsl:template match="Node[empty(*)]">
        <w>
            <xsl:copy-of select="@morphId"/>
            <xsl:attribute name="class" select="lower-case(@Cat)"/>
            <xsl:call-template name="role">
                <xsl:with-param name="node" select="."/>
            </xsl:call-template>
            <xsl:call-template name="head">
                <xsl:with-param name="node" select="."/>
            </xsl:call-template>
            
            <xsl:attribute name="lemma" select="lower-case(@UnicodeLemma)"/>
            <xsl:if test="(following::Node[empty(*)])[1]/@morphId lt @morphId">
                <xsl:attribute name="discontinuous">true</xsl:attribute>
            </xsl:if>

            <xsl:choose>
                <xsl:when test="@Cat='conj'">
                    <!-- Cat End Start Unicode UnicodeLemma morphId nodeId Head Rule -->
                </xsl:when>
                <xsl:when test="@Cat='adj'">
                    <!-- Case Cat End Gender Number Start Unicode UnicodeLemma morphId nodeId Degree Head Rule -->
                    <xsl:attribute name="case" select="lower-case(@Case)"/>
                    <xsl:attribute name="gender" select="lower-case(@Gender)"/>
                    <xsl:attribute name="number" select="lower-case(@Number)"/>
                </xsl:when>
                <xsl:when test="@Cat='verb'">
                    <xsl:choose>
                        <xsl:when test="@Mood = 'Infinitive'">
                            <!--    Cat End Mood Start Tense Unicode UnicodeLemma Voice morphId nodeId -->
                            <xsl:attribute name="tense" select="lower-case(@Tense)"/>
                            <xsl:attribute name="voice" select="lower-case(@Voice)"/>
                            <xsl:attribute name="mood" select="lower-case(@Mood)"/>
                        </xsl:when>
                        <xsl:when test="@Mood = 'Participle'">
                            <!-- Case Cat End Gender Mood Number Start Tense Unicode UnicodeLemma Voice morphId nodeId -->
                            <xsl:attribute name="tense" select="lower-case(@Tense)"/>
                            <xsl:attribute name="voice" select="lower-case(@Voice)"/>
                            <xsl:attribute name="mood" select="lower-case(@Mood)"/>
                            <xsl:attribute name="case" select="lower-case(@Case)"/>
                            <xsl:attribute name="gender" select="lower-case(@Gender)"/>
                            <xsl:attribute name="number" select="lower-case(@Number)"/>
                        </xsl:when>
                        <xsl:otherwise>
                            <!-- Cat End Mood Number Person Start Tense Unicode UnicodeLemma Voice morphId nodeId Case Gender -->
                            <xsl:attribute name="person" select="lower-case(@Person)"/>
                            <xsl:attribute name="number" select="lower-case(@Number)"/>
                            <xsl:attribute name="tense" select="lower-case(@Tense)"/>
                            <xsl:attribute name="voice" select="lower-case(@Voice)"/>
                            <xsl:attribute name="mood" select="lower-case(@Mood)"/>
                        </xsl:otherwise>
                    </xsl:choose>
                </xsl:when>

                <xsl:when test="@Cat='noun'">
                    <!-- Case Cat End Gender Number Start Type Unicode UnicodeLemma morphId nodeId -->
                    <xsl:attribute name="case" select="lower-case(@Case)"/>
                    <xsl:attribute name="gender" select="lower-case(@Gender)"/>
                    <xsl:attribute name="number" select="lower-case(@Number)"/>
                </xsl:when>
                <xsl:when test="@Cat='prep'">
                    <!-- Cat End Start Unicode UnicodeLemma morphId nodeId Head Rule -->
                </xsl:when>
                <xsl:when test="@Cat='det'">
                    <!-- Case Cat End Gender Number Start Unicode UnicodeLemma morphId nodeId -->
                    <xsl:attribute name="case" select="lower-case(@Case)"/>
                    <xsl:attribute name="gender" select="lower-case(@Gender)"/>
                    <xsl:attribute name="number" select="lower-case(@Number)"/>
                </xsl:when>
                <xsl:when test="@Cat='pron'">
                    <!-- Case Cat End Number Start Type Unicode UnicodeLemma morphId nodeId Gender -->
                    <xsl:attribute name="case" select="lower-case(@Case)"/>
                    <xsl:if test="@Gender">
                        <xsl:attribute name="gender" select="lower-case(@Gender)"/>
                    </xsl:if>
                    <xsl:attribute name="number" select="lower-case(@Number)"/>
                </xsl:when>
                <xsl:when test="@Cat='adv'">
                    <!-- Case Cat EndG ender Number Start Unicode UnicodeLemma morphId nodeId Degree Head Rule -->
                </xsl:when>
                <xsl:when test="@Cat='ptcl'">
                    <!-- Cat End Start Unicode UnicodeLemma morphId nodeId Head Rule -->
                </xsl:when>
                <xsl:when test="@Cat='num'">
                    <!-- Cat End Start Unicode UnicodeLemma morphId nodeId -->
                </xsl:when>
                <xsl:when test="@Cat='intj'">
                    <!-- Cat End Head Rule Start nodeId Unicode UnicodeLemma morphId -->
                </xsl:when>
            </xsl:choose>


            <xsl:value-of select="text()"/>
        </w>
        <!-- ### if there's punctuation, put it here! -->
        <xsl:if test="@Unicode != ./text()">
            <pu>
                <xsl:value-of select="substring(@Unicode, string-length(./text())+1)"/>
            </pu>
        </xsl:if>
    </xsl:template>

    <xsl:template match="@*|node()">
        <xsl:apply-templates select="*"/>
    </xsl:template>

</xsl:stylesheet>
