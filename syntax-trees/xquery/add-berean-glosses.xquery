(:
   This query adds the Berean interlinear glosses into the Nestle 1904 syntax
   trees.  Don't try to use this with other GNTs, it is entirely dependent on
   word order.
:)

let $berean := doc("/Users/jonathan/git/Nestle1904/glosses/berean-interlinear-glosses.xml")

for $file in (
    "01-matthew.xml",
    "02-mark.xml",
    "03-luke.xml",
    "04-john.xml",
    "05-acts.xml",
    "06-romans.xml",
    "07-1corinthians.xml",
    "08-2corinthians.xml",
    "09-galatians.xml",
    "10-ephesians.xml",
    "11-philippians.xml",
    "12-colossians.xml",
    "13-1thessalonians.xml",
    "14-2thessalonians.xml",
    "15-1timothy.xml",
    "16-2timothy.xml",
    "17-titus.xml",
    "18-philemon.xml",
    "19-hebrews.xml",
    "20-james.xml",
    "21-1peter.xml",
    "22-2peter.xml",
    "23-1john.xml",
    "24-2john.xml",
    "25-3john.xml",
    "26-jude.xml",
    "27-revelation.xml"
)
let $tree := doc($file)
for $w in $tree//w
let $gloss := attribute gloss { $berean//w[@osisId = $w/@osisId]/gloss } 
return insert node $gloss into $w
