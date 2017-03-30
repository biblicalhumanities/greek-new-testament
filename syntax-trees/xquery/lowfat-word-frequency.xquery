(:
    This version uses a Saxon collation URI, which may need adjusting.

    It relies on the <w/> element, found in lowfat versions.
:)

declare default collation "http://saxon.sf.net/collation?lang=el;strength=secondary";

<wf>
{
for $w in //w
let $n := normalize-unicode($w/@lemma)
let $class := $w/@class
group by $n, $class
order by $n, $class ascending
let $type := $w[1]/@type
let $gender := $w[1]/@gender
let $strong := $w[1]/@strong
return 
	<word>
	 {
	 	attribute lemma {$n},
	 	attribute class {$class},
	 	attribute count {count($w)},
	 	$type[$class != "verb"] ! attribute type { $type },
	 	$gender[$class="noun"] ! attribute gender { $gender },
	 	$strong ! attribute strong { $strong }
	 }
	</word>
}
</wf>