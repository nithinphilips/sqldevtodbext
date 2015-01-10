sqldevtodbext
=============
This is a utility to export your stored `SQL Developer`_ connection profiles to
DbExt_ (a Vim plugin to run SQL) configuration.

It can decrypt any stored passwords from SQL Developer v4 exports.

.. _DbExt: http://www.vim.org/scripts/script.php?script_id=356
.. _SQL Developer: https://oss.oracle.com/sqldeveloper.html

Usage
-----
1. `Export your connection profiles
   <http://www.thatjeffsmith.com/archive/2014/05/migrating-oracle-sql-developer-connections-with-passwords/>`_
2. Encrypt stored passwords it with a master password.
3. Run ``sqldevtodbext`` command on the exported file (assuming the master
   password is ``password``)::

    $ sqldevtodbext -p password /home/nithin/Connections.xml
    "SQL Developer Connection Profile: VM
    let g:dbext_default_profile_VM = 'type=ORA:srvname=(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(Host=localhost)(Port=1521))(CONNECT_DATA=(SID=xe))):user=SCOTT:passwd=$OOper$ecr3t:cmd_terminator=;'

4. Copy to output to your vimrc file.

Limitations
-----------
The tool can only export Oracle connections. Any other database connection
profiles will be ignored.

Installation
------------
Installation from source::

    $ python setup.py install

Now, the ``sqldevtodbext`` command is available::

    $ sqldevtodbext <filename>
    [...]

On Unix-like systems, the installation places a ``sqldevtodbext`` script into a
centralized ``bin`` directory, which should be in your ``PATH``. On Windows,
``sqldevtodbext.exe`` is placed into a centralized ``Scripts`` directory which
should also be in your ``PATH``.


.. "C:\Users\xxx\AppData\Roaming\SQL Developer\system4.0.1.14.48\o.jdeveloper.db.connection.12.1.3.2.41.140207.1351\connections.xml"
