declare function local:clause($node)
(:            
ADV Adverbial Function
IO Indirect Object Function
O Object Function
O2 Second Object Function
S Subject Function
P Predicate Function
V Verbal Function
VC Verbal Copula Function  :)
{
    <wg class="clause">
      {
         $node/@nodeId,
         $node/Node ! local:node(.)
      }
     </wg>
};

declare function local:phrase($node)
{
    <wg>
      {  
         attribute class {$node/@Cat},
         $node/Node ! local:node(.)
      }
    </wg>
};

declare function local:word($node)
{
    <w>{ $node/@*, string($node) }</w>
};

declare function local:node($node as element(Node))
{  (:
   if (empty($node/Node))
   then local:word($node)
   else  :)
       switch($node/@Cat)      
            case "adj"   (: adjective :)
            case "adv"   (: adverb :)
            case "conj"  (: conjunction :)
            case "det"   (: determiner :)
            case "intj"  (: interjection :)
            case "noun"  (: noun :)
            case "num"   (: numeral :)
            case "prep"  (: preposition :)
            case "ptcl"  (: particle :)
            case "pron"  (: pronoun :)
            case "verb"  (: verb  :)
                return local:word($node)
            case "CL"  
                return local:clause($node)
            case "adjp" (: adjectival phrase :)
            case "advp" (: adverbial phrase :)
            case "np"   (: nominal phrase  :)
            case "nump" (: numeral phrase  :)
            case "pp"   (: prepositional phrase  :)
            case "vp"   (: verbal phrase :)         
                return local:phrase($node)
            default 
                return $node/Node
};

declare function local:sentence($node)
{
   <wg class="sentence">
     {
        $node/@nodeId,
        $node/Node ! local:node(.)
     }
   </wg>
};

for $sentence in //Tree/Node
return local:sentence($sentence)
