# SBLGNT Lowfat: Greek New Testament Syntax Trees

https://github.com/biblicalhumanities/greek-new-testament/syntax-trees/sblgnt-lowfat

Last modified: 6 Jan, 2017

These syntax trees were created to be easier to query and to display using standard Web technologies.  They are called "lowfat" because they are simpler and have fewer nodes than the equivalent GBI trees: about 1/2 as many elements, and about 1/3 as many attributes.

Please report bugs by creating issues on this github directory. You can also contact us at:

- Twitter: @bibhumanities
- Email: jonathan.robie@ibiblio.org
- Forums: biblicalhumanities.org or ibiblio.org/bgreek


## Copyright

Syntax diagram markup copyright 2014-2017 by Jonathan Robie and Micheal Palmer,  made available under under a
[CC-BY-SA License] (http://creativecommons.org/licenses/by-sa/3.0/).  
Created by a transformation from Syntax
diagram markup copyright 2013-2015 by the Global Bible Initiative, made available under under a
[CC-BY-SA License] (http://creativecommons.org/licenses/by-sa/3.0/).  
Morphological parsing and lemmatization copyright 2013 by MorphGNT,  made available under a
[CC-BY-SA License](http://creativecommons.org/licenses/by-sa/3.0/).  
SBLGNT text copyright 2010 by the Society of Biblical Literature and Logos Bible Software,
use subject to the [SBLGNT EULA](http://sblgnt.com/license/).

## Markup scheme

This is an example of the current markup scheme:

```xml
<sentence>
   <cite>Jhn11:35:1-11:35:3</cite>
   <wg nodeId="430110350010030" class="cl">
      <w morphId="43011035001" class="verb" role="v" head="true" lemma="δακρύω"
         person="third"
         number="singular"
         tense="aorist"
         voice="active"
         mood="indicative">ἐδάκρυσεν</w>
      <wg nodeId="430110350020020" class="np" role="s">
         <w morphId="43011035002" class="det" lemma="ὁ" case="nominative"
            gender="masculine"
            number="singular">ὁ</w>
         <w morphId="43011035003" class="noun" head="true" lemma="ἰησοῦς" case="nominative"
            gender="masculine"
            number="singular">Ἰησοῦς.</w>
      </wg>
   </wg>
</sentence>
```

Here is an overview of this format:

- &lt;sentence> is, obviously, a sentence. Sentences are determined based purely on punctuation used in the original text.
- &lt;cite> is a citation that identifies the text in a sentence.
- &lt;wg> stands for "word group", and is used to identify a group of words.
- &lt;w> stands for "word", and identifies a single word.

A &lt;wg> can have the following attributes:

- nodeId: an identifier for the &lt;wg> node
- class: the class of the word group. Permitted values: np cl pp vp adjp advp nump adv conj
- role: the clause-level role of the world group. Permitted values: s v vc o p io o2 adv

A &lt;w> can have the following attributes:

- morphId: identifier for the word occurrence
- class: the class of the word. Permitted values: noun verb det conj pron prep adj adv ptcl num int
- role: the clause-level role of the word. Permitted values: s v vc o  io o2 p adv
- head: 'true' if the word is the head of the phrase.
- discontinuous: 'true' if the word is discontinuous with respect to sentence order due to reordering in the syntax tree
- lemma: the lemma of the word
- person: first, second, or third
- number: singular or plural
- gender: masculine, feminine, or neuter
- case: nominative, genitive, dative, accusative, or vocative
- tense: aorist, present, imperfect, future, perfect, or pluperfect
- voice: active, passive, middle, or middlepassive
- mood: indicative, imperative, subjunctive, optative, participle, or infinitive
