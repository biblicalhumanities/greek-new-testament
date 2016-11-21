declare function local:osisBook($nodeId)
{
  switch (xs:integer(substring($nodeId, 1, 2)))
    case  1  return "Matt"
    case  2  return "Mark"
    case  3  return "Luke"
    case  4  return "John"
    case  5  return "Acts"
    case  6  return "Rom"
    case  7  return "1Cor"
    case  8  return "2Cor"
    case  9  return "Gal"
    case  10 return "Eph"
    case  11 return "Phil"
    case  12 return "Col"
    case  13 return "1Thess"
    case  14 return "2Thess"
    case  15 return "1Tim"
    case  16 return "2Tim"
    case  17 return "Titus"
    case  18 return "Phlm"
    case  19 return "Heb"
    case  20 return "Jas"
    case  21 return "1Pet"
    case  22 return "2Pet"
    case  23 return "1John"
    case  24 return "2John"
    case  25 return "3John"
    case  26 return "Jude"
    case  27 return "Rev"
    default return "###"
};

declare function local:osisId($nodeId)
{
  local:osisBook($nodeId)
};

declare function local:clause($node)
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
  if (count($node/Node)>1) 
  then
    <wg>
      {  
       attribute class {$node/@Cat},
       $node/Node ! local:node(.)
      }
    </wg>
  else 
    $node/Node ! local:node(.)
};

declare function local:role($node)
{
  <wg>
    {
      attribute class {$node/Node/@Cat},
      attribute role {$node/@Cat },
      $node/Node/Node ! local:node(.)
    }
  </wg>
};

declare function local:word($node)
{
    <w>{ $node/@*, string($node) }</w>
};

declare function local:node($node as element(Node))
{ 
  switch ($node/@Cat)
    case "adj"
    case "adv"
    case "conj"
    case "det"
    case "intj"
    case "noun"
    case "num"
    case "prep"
    case "ptcl"
    case "pron"
    case "verb"
      return local:word($node)
    case "adjp"
    case "advp"
    case "np"
    case "nump"
    case "pp"
    case "vp"
      return local:phrase($node)
    case "S"
    case "IO"
    case "ADV"
    case "O"
    case "O2"
    case "P"
    case "V"
    case "VC"
      return local:role($node)
    case "CL"
      return local:clause($node)
    default
      return <cat>{ $node/@Cat }</cat>
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

<wg class="book">
  {
    for $sentence in //Tree/Node
    return local:sentence($sentence)
  }
</wg>