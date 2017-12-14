declare variable $pos := //parts-of-speech;
declare variable $morph := //morphology;

declare function local:morph-description($tag, $category)
{
   $morph/field[@tag=$category]/value[@tag=$tag]/@summary ! string(.)
};

declare function local:number($morph as xs:string)
{
  let $tag := substring($morph,2,1)
  where $tag != "-"
  return
    attribute number {
      local:morph-description($tag, "number")    
    }
};

declare function local:person($morph as xs:string)
{
  let $tag := substring($morph,1,1)
  where $tag != "-"  
  return
    attribute person {
      tokenize(local:morph-description($tag, "person"))[1]   
    }
};

declare function local:gender($morph as xs:string)
{
  let $tag := substring($morph,6,1)
  where $tag != "-"  
  return
    attribute gender {
      local:morph-description($tag,"gender")      
    }  
};

declare function local:case($morph as xs:string)
{
  let $tag := substring($morph,7,1)
  where $tag != "-"
  return
    attribute case {
      local:morph-description($tag,"case")      
    }
};

declare function local:tense($morph as xs:string)
{
  let $tag := substring($morph,3,1)
  where $tag != "-"
  return
    attribute tense {
      local:morph-description($tag,"tense")  
    }
};

declare function local:voice($morph as xs:string)
{
  let $tag := substring($morph,5,1)
  where $tag != "-"
  return  
    attribute voice {
      local:morph-description($tag,"voice")    
    }
};

declare function local:mood($morph as xs:string)
{
  let $tag := substring($morph,4,1)
  where $tag != "-"
  return  
    attribute mood {
      local:morph-description($tag,"mood")
    }
};

declare function local:degree($morph as xs:string)
{
  let $tag := substring($morph,8,1)
  where $tag != "-"
  return  
    attribute degree {
      local:morph-description($tag,"degree")
    }
};

declare function local:strength($morph as xs:string)
{
  let $tag := substring($morph,9,1)
  where $tag != "-"
  return  
    attribute strength {
      local:morph-description($tag,"strength")
    }
};

declare function local:inflection($morph as xs:string)
{
  let $tag := substring($morph,10,1)
  where $tag != "-"
  return  
    attribute inflection {
      local:morph-description($tag,"inflection")
    }
};

declare function local:morphology($t)
{
  let $morph := string($t/@morphology)
  where $morph
  return (
    $t/@lemma,
    local:number($morph),
    local:person($morph),
    local:gender($morph),
    local:case($morph), 
    local:tense($morph),
    local:voice($morph),
    local:mood($morph),
    local:degree($morph),
    local:strength($morph),
    local:inflection($morph),
    local:information-status($t/@information-status)    
  )
};

declare function local:class($t)
{
  let $description :=  string($pos/value[@tag = $t/@part-of-speech]/@summary)
  let $class :=
    switch ($description)
      case "interrogative adverb" return "adverb"
      case "relative adverb" return "adverb"
      case "common noun" return "noun"
      case "proper noun" return "noun"
      case "cardinal numeral" return "numeral"
      case "ordinal numeral" return "numeral"      
      case "demonstrative pronoun" return "pronoun"
      case "indefinite pronoun" return "pronoun"
      case "interrogative pronoun" return "pronoun"
      case "relative pronoun" return "pronoun"
      case "personal pronoun" return "pronoun"
      case "personal reflexive pronoun" return "pronoun"
      case "possessive pronoun" return "pronoun"
      case "possessive reflexive pronoun" return "pronoun"
      case "reciprocal pronoun" return "pronoun"
      case "" return ()
      default return $description
  let $type :=
    switch ($description)
      case "interrogative adverb" return "interrogative"
      case "relative adverb" return "relative"
      case "common noun" return "common"
      case "proper noun" return "proper"
      case "cardinal numeral" return "cardinal"
      case "ordinal numeral" return "ordinal"      
      case "demonstrative pronoun" return "demonstrative"
      case "indefinite pronoun" return "indefinite"
      case "interrogative pronoun" return "interrogative"
      case "relative pronoun" return "relative"
      case "personal pronoun" return "personal"
      case "personal reflexive pronoun" return "personal relative"
      case "possessive pronoun" return "possessive"
      case "possessive reflexive pronoun" return "possessive reflexive"
      case "reciprocal pronoun" return "reciprocal"
      default return ()  
  return
    (
      $class ! attribute class {$class},
      $type ! attribute type {$type}
    )
};

declare function local:information-status($tis)
{
  attribute information-status { $tis }
};

declare function local:token($t)
{
  <w>
    {
      local:class($t),
      attribute role {$t/@relation},
      local:morphology($t),
      attribute n {$t/@id},
      $t/@head-id ! attribute head-id {$t/@head-id }
    }
    {
      string($t/@form)
    }
  </w>,
  $t/@presentation-after[. != ' '] ! <pc>{normalize-space(.)}</pc>
};


declare function local:unwrap($t, $stok)
{
  let $children :=  $stok[@head-id = $t/@id]
  let $seq := ($children | $t)/.
  return
    if ($children)
    then 
      <wg role="{$t/@relation}" head="{$t/@id}">
        {
          for $s in $seq
          return 
            if ($s is $t)
            then local:token($t)
            else local:unwrap($s, $stok)
        }
      </wg>
    else local:token($t)
};

declare function local:milestone($ms)
{
  let $groups := analyze-string($ms, "(\d+)?(\w+) (\d+)\.(\d+)")//fn:group
  let $name :=
    switch ($groups[@nr="2"])
      case "PHILEM" return "phlm"
      default return $groups[@nr="2"]
  let $first :=
    string-join(($groups[@nr="1"], upper-case(substring($name,1,1)),lower-case(substring($name,2))),"")
  let $osisId := string-join(($first, $groups[@nr="3"], $groups[@nr="4"]),".")
  return
    <milestone unit="verse" id="{$osisId}">{ $osisId }</milestone>    
};

declare function local:lastchild($t)
{
  let $children :=  
    for $c in $t[@head-id = $t/@id]
    order by $c/@id descending
    return $c
  return $children[1]
};

declare function local:sentence($s)
{
  <sentence>
    {
      attribute id { $s/@id }
    }  
    {
      for $ms in distinct-values($s//@citation-part)
      return local:milestone($ms)
    }
    {
      <p>
       {
         string-join( $s//token ! (@form, @presentation-after), "")
       }
      </p>
    }
    {      
      let $stok := $s//token
      for $t in $stok[not(@head-id)]     
      order by local:lastchild($t)
      return local:unwrap($t, $stok)
    }
  </sentence>  
};


<?xml-stylesheet href="treedown.css"?>,
<?xml-stylesheet href="boxwood.css"?>,
<book>
  {
    for $s in //sentence
    return local:sentence($s)
  }
</book>