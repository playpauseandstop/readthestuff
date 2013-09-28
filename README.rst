============
readthestuff
============

Yet another Google Reader alternative built on top of Python.

Requirements
============

* `Python <http://www.python.org/>`_ 2.7
* `Make <http://www.gnu.org/software/make>`_
* `bootstrapper <http://pypi.python.org/pypi/bootstrapper>`_ 0.1.5 or higher
* `PostgreSQL <http://www.postgresql.org/>`_ 9.3 or higher
* `ElasticSearch <http://elasticsearch.org/>`_ 0.10.5 or higher
* `Redis <http://redis.io/>`_ 2.6.16 or higher

License
=======

``readthestuff`` project is licensed under the terms of `BSD License
<https://github.com/playpauseandstop/readthestuff/blob/LICENSE>`_.

Installation
============

First of all you need to create virtual environment for project and install
all Python requirements here. This could be done in different ways, one of
which just run::

    $ make bootstrap

Next, make sure you have `PostgreSQL`_, `ElasticSearch`_ and `Redis`_ installed
in your system and provide URLs for access these services in local settings
as::

    DATABASE_URL = 'postgres://USERNAME:PASSWORD@HOST:PORT/DATABASE'
    ELASTICSEARCH_URL = 'http://URL:9200/'
    REDIS_URL = 'redis://URL:6379/'

And finally, you need to initialize PostgreSQL database. To this, just run::

    $ make initdb

Now you ready to go.

Usage
=====

After installation you could run either development web-server which would be
reloading automatically on file change or Gunicorn web-server, to do this run::

    $ make devserver

or::

    $ make server

Also, you'll need to run RQ worker, as::

    $ make rq

And finally you can check what's what by pointing browser to
``http://localhost:8321``.

Happy testing!
