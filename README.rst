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

License
-------
.. code::

    Odel. Tool to upload Data Integrator files to IBM Tririga.
    Copyright (C) 2014 Nithin Philips

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

.. ""
