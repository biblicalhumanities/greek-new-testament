# Greek New Testament Syntax Trees (SBLGNT Low Fat)

https://github.com/biblicalhumanities/greek-new-testament/syntax-trees/sblgnt-lowfat

Last modified: 2 Feb, 2015

These syntax trees were created to be easier to query and to display using standard Web technologies.

Syntax diagram markup copyright 2014-2015 by Jonathan Robie and Micheal Palmer,  made available under under a
[CC-BY-SA License] (http://creativecommons.org/licenses/by-sa/3.0/).  
Created by a transformation from Syntax diagram markup copyright 2013-2015 by the Global Bible Initiative, made available under under a
[CC-BY-SA License] (http://creativecommons.org/licenses/by-sa/3.0/).  
Morphological parsing and lemmatization copyright 2013 by MorphGNT,  made available under a
[CC-BY-SA License](http://creativecommons.org/licenses/by-sa/3.0/).  
SBLGNT text copyright 2010 by the Society of Biblical Literature and Logos Bible Software,
use subject to the [SBLGNT EULA](http://sblgnt.com/license/).

These syntax trees were automatically generated, then carefully corrected by hand.  Please report any errors you encounter.


Current markup scheme:

Cat = Part-of-speech Category  
Rule = Rule used to combine nodes—some of these are arbitrary, some make meaningful distinctions (for example, when two nouns are connected together, we have different rules differentiating apposition, genitive modification, or two nouns conjoined/juxtaposed without conjunction in between).  
Start = indicates starting position of the node in the tree  
End = indicates ending position of the node in the tree (at the word level start & end would be the same; at a higher node, e.g., a multi-word phrase, the starting & ending position indicates the span of the multi-word phrase)  
Person = grammatical person  
Number = grammatical number  
Gender = grammatical gender  
Case = grammatical case  
Degree = degree of adjectives  
Tense = grammatical tense of verbs  
Voice = grammatical voice of verbs  
Mood = grammatical mood of verbs  
Relative = appears only with pronouns, will have True value if pronoun is a Relative pronoun  
Personal = appears only with pronouns, will have True value if pronoun is a Personal pronoun  
Demonstrative = appears only with pronouns, will have True value if pronoun is a Demonstrative pronoun  
Interrogative = appears only with pronouns, will have True value if pronoun is an Interrogative pronoun  
Unicode = Unicode of surface text  
UnicodeLemma = Unicode of lexical lemma  
morphId = morphId was developed as unique ID for building our translation memory & a host of other interlinear tools  
nodeId = BBCCCVVVWWWSSSL as previously noted, where WWW represents the beginning position (the Nth word) of a node/sub-tree
SSS represents the SPAN of a node (how many words it covers) L (Level) is used to distinguish nodes which have the same span (in cases of non-branching nodes)  

The following only occur in non-terminal nodes:

ClType = This occurs only for CL nodes. By default, there is no Type value--all clauses with V or VC (any verbal form) have no value. It is the clauses without a V or VC (any verbal form) that have Type value to distinguish Verbless from VerbElided clauses  
HasDet = Has True value when a phrase has a determiner included in it  
