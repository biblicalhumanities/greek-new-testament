# Greek New Testament Syntax Trees (Nestle 1904)

https://github.com/biblicalhumanities/greek-new-testament/syntax-trees/nestle1904

Last modified: 21 Dec, 2016

This is based on the 1904 edition of Eberhard Nestle's Greek New
Testament, often referred to as the Nestle 1904 or British Foreign
Bible Society 1904.

Syntax diagram markup copyright 2014-2017 by the Global Bible Initiative, made available under under a 
[CC-BY-SA License] (http://creativecommons.org/licenses/by-sa/3.0/).  

Morphological parsing and lemmatization by Dr. Ulrik Sandborg-Petersen
of Emergence Consult and Aalborg University, Denmark, and released
into the public domain. Available at https://github.com/biblicalhumanities/Nestle1904.

Greek text transcribed by Diego Renato dos Santos, available at
https://sites.google.com/site/nestle1904/.

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
