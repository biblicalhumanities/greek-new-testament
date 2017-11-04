# emdros-mql: Script(s) to convert syntax trees to Emdros MQL

https://github.com/biblicalhumanities/greek-new-testament/syntax-trees/emdros-mql/

## What is this?

A script to transform the Hebrew and Greek XML syntax trees from
Global Bible Initiative to Emdros MQL.

## What syntax trees are supported?

At the moment, all Greek and Hebrew syntax trees that come directly
from the Global Bible Initiative are supported.

In this repository, this means:

- https://github.com/biblicalhumanities/greek-new-testament/syntax-trees/nestle1904/
- https://github.com/biblicalhumanities/greek-new-testament/syntax-trees/sblgnt/

## What is Emdros?

Emdros is a text database query and storage engine for annotated text
(text plus information about that text).  For more information, please
see the Emdros home page:

- http://emdros.org/

## Copyright

The GBITrees2MQL.py script is Copyright (C) 2017 by United Bible
Societies.  It has been placed under the MIT License by kind
permission from Dr. Reinier de Blois.

## Authors

The GBITrees2MQL.py script was written by Ulrik Sandborg-Petersen with
assistance from Andi Wu.

## Usage?

```
python GBITrees2MQL.py -o <MQL-output-file> <XML-input-file1> [<XML-input-file2> ...]
```

If the MQL-output-file is called, say, "trees.mql", then two files are
produced:

- trees.mql (contains the data)
- trees.schema.mql (contains the MQL schema)


## Example usage?

```
python GBITrees2MQL.py -o Nestle1904.mql /path/to/Nestle/XML/files/*.xml
```

This would produce Nestle1904.mql (containing the data) and
Nestle1904.schema.mql (containing the MQL schema).

## How to import the data?

For example, given that the Nestle 1904 data has been converted as in
the above example, then this sequence of commands will import the data
into Emdros (provided the mql(1) command is installed in your PATH):

```
$ echo "CREATE DATABASE 'Nestle1904' GO" | mql -b 3
$ mql -b 3 -d Nestle1904 Nestle1904.schema.mql
$ mql -b 3 -d Nestle1904 Nestle1904.mql
$ echo "VACUUM DATABASE ANALYZE GO" | mql -b 3 -d Nestle1904
```

This will import it into the backend "SQLite3" (-b 3).  For other backends, run

```
mql --help
```


## How to report issues?

Please report bugs by creating issues on this github directory.

