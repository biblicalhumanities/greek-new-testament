(:
    This version uses a Saxon collation URI, which may need adjusting.

    It relies on the @normalized attribute, currently in nestle1904 but not SBLBNT.
    It relies on the <w/> element, found in lowfat versions.
:)

declare default collation "http://saxon.sf.net/collation?lang=el;strength=secondary";

<wf>
{
for $w in //w
let $n := $w/@normalized
group by $n
order by $n ascending
return 
	<group>
	 {
	 	attribute form {$n},
	 	attribute count {count($w)}
	 }
	</group>
}
</wf>