/* 
    Use lowercase for all book names when looking up.  
    Parser joins preceding numbers to book names. */

function localFile(tokens) {
  var books = {
      "mt" : "01-matthew.xml",
      "matt" : "01-matthew.xml",
      "matthew" : "01-matthew.xml",
      "mk" : "02-mark.xml",
      "mr" : "02-mark.xml",
      "mrk" : "02-mark.xml",
      "mark": "02-mark.xml",
      "lk" : "03-luke.xml",
      "luk" : "03-luke.xml",
      "luke" : "03-luke.xml",
      "jn" : "04-john.xml",
      "jhn" : "04-john.xml",
      "john" : "04-john.xml",
      "acts" : "05-acts.xml",
      "ro" : "06-romans.xml",
      "rm" : "06-romans.xml",
      "rom" : "06-romans.xml",
      "romans" : "06-romans.xml",
      "1co" : "07-1corinthians.xml",
      "1cor" : "07-1corinthians.xml",
      "1corinthians" : "07-1corinthians.xml",
      "2co" : "08-2corinthians.xml",
      "2cor"  : "08-2corinthians.xml",
      "2corinthians"  : "08-2corinthians.xml",
      "ga" : "09-galatians.xml",
      "gal" : "09-galatians.xml",
      "galatians" : "09-galatians.xml",
      "eph" : "10-ephesians.xml",
      "ephes" : "10-ephesians.xml",
      "ephesians" : "10-ephesians.xml",
      "phil" : "11-philippians.xml",
      "php" : "11-philippians.xml",
      "philippians" : "11-philippians.xml",
      "co" : "12-colossians.xml",
      "col" : "12-colossians.xml",
      "colossians" : "12-colossians.xml",
      "1th" : "13-1thessalonians.xml",
      "1thes" : "13-1thessalonians.xml",
      "1thess" : "13-1thessalonians.xml",
      "1thessalonians" : "13-1thessalonians.xml",
      "2th"  : "14-2thessalonians.xml",
      "2thes"  : "14-2thessalonians.xml",
      "2thess"  : "14-2thessalonians.xml",
      "2thessalonian" : "14-2thessalonians.xml",
      "1ti" : "15-1timothy.xml",
      "1tim" : "15-1timothy.xml",
      "1timothy" : "15-1timothy.xml",
      "2ti" : "16-2timothy.xml",
      "2tim" : "16-2timothy.xml",
      "2timothy" : "16-2timothy.xml",
      "tit" : "17-titus.xml",
      "titus" : "17-titus.xml",
      "phm" : "18-philemon.xml",
      "philemon" : "18-philemon.xml",
      "he": "19-hebrews.xml",
      "heb": "19-hebrews.xml",
      "hebrews": "19-hebrews.xml",
      "jm" : "20-james.xml",
      "jam" : "20-james.xml",
      "james" : "20-james.xml",
      "1pe" : "21-1peter.xml",
      "1pt" : "21-1peter.xml",
      "1pet" : "21-1peter.xml",
      "1peter" : "21-1peter.xml",
      "2pe" : "22-2peter.xml",
      "2pt" : "22-2peter.xml",
      "2pet" : "22-2peter.xml",
      "2peter" : "22-2peter.xml",
      "1jo" : "23-1john.xml",
      "1jn" : "23-1john.xml",
      "1joh" : "23-1john.xml",
      "1jhn" : "23-1john.xml",
      "1john" : "23-1john.xml",
      "2jo" : "24-2john.xml",
      "2jn" : "24-2john.xml",
      "2joh" : "24-2john.xml",
      "2jhn" : "24-2john.xml",
      "2john" : "24-2john.xml",
      "3jo" : "25-3john.xml",
      "3jn" : "25-3john.xml",
      "3jon" : "25-3john.xml",
      "3jhn" : "25-3john.xml",
      "3john" : "25-3john.xml",
      "jud" : "26-jude.xml",
      "jude" : "26-jude.xml",
      "re" : "27-revelation.xml",
      "rev" : "27-revelation.xml",
      "revelation" : "27-revelation.xml",
      "revelations" : "27-revelation.xml"
  };

    // If first token is a number, combine with the second to form book name
    book = (isNaN(tokens[0]) ? tokens[0] : tokens[0]+tokens[1]);
    return books[book.toLowerCase()];
}

function osisId(tokens)
{
    return (isNaN(tokens[0]) ? tokens.join(".") : tokens[0]+tokens[1]+"."+tokens.slice(2).join("."));
}

function treeFile(passage, version) {
    var trees = "../" + version + "-lowfat/xml/";
    var tokens = passage.split(/[\s,:\.]+/);
    return trees + localFile(tokens) + '#' + osisId(tokens);
}

function loadPassage() {
    var passage = document.getElementById("passage").value;

    document.getElementById("display").src = treeFile(passage, "nestle1904");
}

// TODO: set anchor in address bar - http://shorts.jeffkreeftmeijer.com/2014/scroll-to-anchors-in-iframes/#anchor-3
// TODO: let URI parameters load passage - https://www.sitepoint.com/get-url-parameters-with-javascript/
// TODO: show/hide trees
