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
* Sample command line tools for:
  ** Retrieving the information of an author saving the entries in JSON format. It also support parallel workers.
  ** Testing similarity between two strings

Examples
--------

To run the samples first you need to copy the file env.sample to .env and modify it to add your Microsoft's Cognitive service key. This key is obtained from the azure portal linked to your subscription.
Check [their official site](https://azure.microsoft.com/en-us/try/cognitive-services/) for more information.

Retrieve the articles written by Einstein:

    $ python samples/author.py --author "albert einstein"

Retrieve histograms for (Y)ear and (F)ield of study for Albert Einstein:

    $ python samples/calc_histogram.py -e "Composite(AA.AuN='albert einstein')" -a "Y,F.FN"

Retrieve similarity between two texts:

    $ python samples/similarity.py --s1 "Imagination is more important than knowledge" --s2 "Insanity: doing the same thing over and over again and expecting different results"

License
-------

maka is using the standard [Apache license 2.](http://www.apache.org/licenses/LICENSE-2.0).
