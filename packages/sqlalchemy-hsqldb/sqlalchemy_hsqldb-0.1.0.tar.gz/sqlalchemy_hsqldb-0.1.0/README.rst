=================
sqlalchemy-hsqldb
=================
SQLAlchemy dialect for HyperSQL 2.0 (HSQLDB)

Description
-----------
The objective of this project is to enable 
`SQLAlchemy <https://www.sqlalchemy.org/>`_ support for
`HyperSQL <https://hsqldb.org/>`_ 2.0 databases (a.k.a. HSQLDB).

As an initial release this version has limitations and still contains much
debug code. However the great news is "It works on my Windows based system",
currently passing about 38 percent of the dialect test suite.
Testing on other environments will follow in due course.

This project depends on a modified version of the
`JayDeBeApi <https://github.com/baztian/jaydebeapi>`_ module to provide
JDBC connectivity and a DB-API 2.0 interface. The module should install itself
automatically. If not, my project can be found here on GitHub:
`jaydebeapi-hsqldb <https://github.com/Pebble94464/jaydebeapi-hsqldb.git>`_

License
-------
sqlalchemy-hsqldb is distributed under the
`MIT license <https://opensource.org/licenses/MIT>`_.

Prerequisites
-------------
You'll need a copy of the Java Runtime Environment (JRE) installed, or Java
Development Kit (JDK).  See: `www.java.com <https://www.java.com/>`_

You'll also need an HyperSQL 2.0 database running as a service, which can be
accessed by specifying a URL (not a file URL). See:
`hsqldb.org <https://hsqldb.org/>`_

Older versions of HyperSQL are not currently supported, including those used by
OpenOffice.org and LibreOffce.  This may change in the future.  However both
applications can be configured relatively easily to connect to a HyperSQL 2.0
database.

Please ensure the architecture of any software components installed match,
including Java and Python environments, HyperSQL, and applications used.
Mixing 32 and 64-bit software is not advised.

Installation
------------

Packages for installing sqlalchemy-hsqldb will soon be available from
`pypi.org <https://pypi.org/>`_
To install sqlalchemy-hsqldb from pypi.org, open a command prompt and type:

.. code-block:: sh

	pip install sqlalchemy-hsqldb

Alternatively the dialect and its driver can be downloaded from the
repositories on GitHub:

* Dialect: `sqlalchemy-hsqldb repository <https://github.com/Pebble94464/sqlalchemy-hsqldb.git>`_
* Driver:  `jaydebeapi-hsqldb repository <https://github.com/Pebble94464/jaydebeapi-hsqldb.git>`_

The driver module probably needs installing before the dialect. Use the
'pip install <path>' syntax to install, where <path> points to where your local
copy is installed.

.. code-block:: sh

	pip install ./jaydebeapi-hsqldb
	pip install ./sqlalchemy-hsqldb

Post-install Configuration
--------------------------
Your system needs to know where the Java Runtime Environment is installed.
If not detected automatically you may need to add 'JAVA_HOME' or 'JRE_HOME'
to your environment variables.

.. code-block:: sh

	set "JAVA_HOME=C:\Program Files\Java\jre-1.8\bin"

The jaydebeapi-hsqldb module also needs to know where HyperSQL's JAR file is
located. At the moment this can be specified using another environment
variable named 'CLASSPATH', (but this method of specifing the location will
likely change in a future release). For example, on Windows...
.. code-block:: sh

	set "CLASSPATH=/some_folder/hsqldb-osgi-jdk8.jar"

Getting Started
---------------
After the dialect and prerequisites have been installed and configured we can
begin writing Python code.  The example below is provided as a minimal example,
designed to get you connected to the database as quickly as possible, but you
will need to update some parameters to match your configuration.

.. code-block:: python

	from sqlalchemy import create_engine

	import os

	# Set 'JAVA_HOME' or 'JRE_HOME' environment variables to the path of your
	# Java installation (this step might not be required)...
	os.environ['JAVA_HOME'] = "C:\\Program Files\\Java\\jre-1.8\\bin"

	# Tell jaydebeapi-hsqldb where your HyperSQL jar file is installed...
	os.environ['CLASSPATH'] = "/PROGS/HSQLDB/hsqldb-osgi-jdk8.jar"

	if __name__ == '__main__':

		# Call SQLAlchemy's create_engine function with your connection string.
		# The basic format is:
		#   <dialect+driver>://<user>:<password>@<hostname>:<port>/<db name>
		engine = create_engine("hsqldb+jaydebeapi://SA:@localhost/db1", echo=True)

		try:
			conn = engine.connect()
			version = engine.dialect._get_server_version_info(conn)
			assert isinstance(version,str) and len(version) > 0, 'Version string is missing.'
			print(f'\nSuccessfully connected!\nHSQLDB version: {version}\n')
			conn.close()
		except Exception as e:
			print(f'\n{repr(e)}\n{str(e)}\n')

If all goes well you should see a success message displayed, otherwise an error
message will provide some hint as to why it's not working.

Known issues
------------

This initial release contains some debug code that will cause execution to
halt. Due to be removed in the next release.

Troubleshooting
---------------

This project was coded and tested on a 64-bit Windows system. It should work on 
other platforms too, but you may find the code examples and docs need adapting.

If you're struggling to get sqlalchemy-hsqldb working here are a few things you can try:

* Avoid mixing 32-bit and 64-bit software components
* If the Java Runtime Environment (JRE) is not automatically detected you may need to add 'JAVA_HOME' or 'JRE_HOME' to your environment variables.
* If using HyperSQL in conjunction with other software such as OpenOffice.org or LibreOffce, verify they're working first.
* If you suspect a permissions issue, try installing and running with an administrator account.
* If you suspect a firewall issue, temporarily disable the firewall to see if this is the case.
* If you suspect some other configuration issue, ensure all paths specified are correct. Use back slashes or forward slashes as appropriate for your OS. Do they need escaping?

* Submit a question via StackOverflow!
	It's quite possible others have already encountered the same issue and SO can
	often provide a quick response. Tag your question with an appropriate tag, such
	as 'sqlalchemy-hsqldb', which I can then monitor.

If you think you've found a bug please feel welcome to submit a report via GitHub:

* `sqlalchemy-hsqldb issues <https://github.com/Pebble94464/sqlalchemy-hsqldb/issues>`_
* `jaydebeapi-hsqldb issues <https://github.com/Pebble94464/jaydebeapi-hsqldb/issues>`_

Changelog
---------
	0.1.0	initial release

