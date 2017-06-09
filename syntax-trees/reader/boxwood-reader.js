/* 
    Use lowercase for all book names when looking up.  
    Parser joins preceding numbers to book names.
*/

  var books = {
      "mt" : "Matt",
      "matt" : "Matt",
      "matthew" : "Matt",
      "mk" : "Mark",
      "mr" : "Mark",
      "mrk" : "Mark",
      "mark": "Mark",
      "lk" : "Luke",
      "luk" : "Luke",
      "luke" : "Luke",
      "jn" : "John",
      "jhn" : "John",
      "john" : "John",
      "acts" : "Acts",
      "ro" : "Rom",
      "rm" : "Rom",
      "rom" : "Rom",
      "romans" : "Rom",
      "1co" : "1Cor",
      "1cor" : "1Cor",
      "1corinthians" : "1Cor",
      "2co" : "2Cor",
      "2cor"  : "2Cor",
      "2corinthians"  : "2Cor",
      "ga" : "Gal",
      "gal" : "Gal",
      "galatians" : "Gal",
      "eph" : "Eph",
      "ephes" : "Eph",
      "ephesians" : "Eph",
      "phil" : "Phil",
      "php" : "Phil",
      "philippians" : "Phil",
      "co" : "Col",
      "col" : "Col",
      "colossians" : "Col",
      "1th" : "1Thess",
      "1thes" : "1Thess",
      "1thess" : "1Thess",
      "1thessalonians" : "1Thess",
      "2th"  : "2Thess",
      "2thes"  : "2Thess",
      "2thess"  : "2Thess",
      "2thessalonian" : "2Thess",
      "1ti" : "1Tim",
      "1tim" : "1Tim",
      "1timothy" : "1Tim",
      "2ti" : "2Tim",
      "2tim" : "2Tim",
      "2timothy" : "2Tim",
      "tit" : "Titus",
      "titus" : "Titus",
      "phm" : "Phlm",
      "phlm" : "Phlm",
      "philemon" : "Phlm",
      "he": "Heb",
      "heb": "Heb",
      "hebrews": "Heb",
      "jm" : "Jas",
      "jam" : "Jas",
      "jas" : "Jas",
      "james" : "Jas",
      "1pe" : "1Pet",
      "1pt" : "1Pet",
      "1pet" : "1Pet",
      "1peter" : "1Pet",
      "2pe" : "2Pet",
      "2pt" : "2Pet",
      "2pet" : "2Pet",
      "2peter" : "2Pet",
      "1jo" : "1John",
      "1jn" : "1John",
      "1joh" : "1John",
      "1jhn" : "1John",
      "1john" : "1John",
      "2jo" : "2John",
      "2jn" : "2John",
      "2joh" : "2John",
      "2jhn" : "2John",
      "2john" : "2John",
      "3jo" : "3John",
      "3jn" : "3John",
      "3jon" : "3John",
      "3jhn" : "3John",
      "3john" : "3John",
      "jud" : "Jude",
      "jude" : "Jude",
      "re" : "Rev",
      "rev" : "Rev",
      "revelation" : "Rev",
      "revelations" : "Rev"
  };

  var files = {
      "Matt" : "01-matthew.xml",
      "Mark": "02-mark.xml",
      "Luke" : "03-luke.xml",
      "John" : "04-john.xml",
      "Acts" : "05-acts.xml",
      "Rom" : "06-romans.xml",
      "1Cor" : "07-1corinthians.xml",
      "2Cor"  : "08-2corinthians.xml",
      "Gal" : "09-galatians.xml",
      "Eph" : "10-ephesians.xml",
      "Phil" : "11-philippians.xml",
      "Col" : "12-colossians.xml",
      "1Thess" : "13-1thessalonians.xml",
      "2Thess" : "14-2thessalonians.xml",
      "1Tim" : "15-1timothy.xml",
      "2Tim" : "16-2timothy.xml",
      "Titus" : "17-titus.xml",
      "Phlm" : "18-philemon.xml",
      "Heb": "19-hebrews.xml",
      "Jas" : "20-james.xml",
      "1Pet" : "21-1peter.xml",
      "2Pet" : "22-2peter.xml",
      "1John" : "23-1john.xml",
      "2John" : "24-2john.xml",
      "3John" : "25-3john.xml",
      "Jude" : "26-jude.xml",
      "Rev" : "27-revelation.xml"
  };


function localFile(tokens) {

    // If first token is a number, combine with the second to form book name
    book = (isNaN(tokens[0]) ? tokens[0] : tokens[0]+tokens[1]);
    return files[books[book.toLowerCase()]];
}

function osisId(tokens)
{
    return (isNaN(tokens[0])
	    ? books[tokens[0].toLowerCase()] + "." + tokens.slice(1).join(".")
	    : books[tokens[0]+tokens[1].toLowerCase()] + "." + tokens.slice(2).join("."));
}

function treeFile(passage, version) {
    var trees = "../" + version + "-lowfat/xml/";
    var tokens = passage.split(/[\s,:\.]+/);
    console.log(osisId(tokens));
    return trees + localFile(tokens) + '#' + osisId(tokens);
}

function loadPassage() {
    var passage = document.getElementById("passage").value;

    document.getElementById("display").src = treeFile(passage, "nestle1904");
}

// TODO: set anchor in address bar - http://shorts.jeffkreeftmeijer.com/2014/scroll-to-anchors-in-iframes/#anchor-3
// TODO: let URI parameters load passage - https://www.sitepoint.com/get-url-parameters-with-javascript/

