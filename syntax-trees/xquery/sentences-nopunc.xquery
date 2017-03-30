(:
    A sentence is not well-defined, and sometimes our analysis
    legimately disagree with a critical edition's punctuation. 
    
    But it's still useful to examine sentences that do not end
    with punctuation.  This generates lists of them.
:)

<wf xmlns:xi="http://www.w3.org/2001/XInclude">
{
for $p in //p,
      $punc in $p ! substring(., string-length(.), 1)
      where not($punc = ( "·", " .", ";", ",",".","—","·",";"))
return $p
}
</wf>
