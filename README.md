maka
==========

maka is a Python module that implements a querier and parser for the Microsoft Academic Knowledge API.
Its classes can be used independently, but it can also be invoked as a command-line tool.

If you'd like to get in touch, email me at gonzalo.huerta  _AT_ uai.cl or ping me [on Twitter](http://twitter.com/gohucan).

Regards,<br>
Gonzalo

Features
--------

* Follows the definitions of entities from the Microsoft site, but also includes human readable format.
* A testing command-line tool that save entries in JSON format. It also support parallel workers.

Examples
--------

The only option so far for the command line script (test.py) is author.

Retrieve the articles written by Einstein:

    $ test.py --author "albert einstein"

License
-------

maka is using the standard [Apache license 2.](http://www.apache.org/licenses/LICENSE-2.0).