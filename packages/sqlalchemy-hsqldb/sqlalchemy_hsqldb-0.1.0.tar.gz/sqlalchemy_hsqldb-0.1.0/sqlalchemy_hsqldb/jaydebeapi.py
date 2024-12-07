from .base import HyperSqlDialect
from .base import HyperSqlExecutionContext
from types import ModuleType
from sqlalchemy.engine.url import make_url
from sqlalchemy.engine.url import URL

class HyperSqlExecutionContext_jaydebeapi(HyperSqlExecutionContext):
	pass

class HyperSqlDialect_jaydebeapi(HyperSqlDialect):
	"""HyperSqlDialect implementation of Dialect using JayDeBeApi as the driver."""

	driver = 'jaydebeapi'
	jclassname = 'org.hsqldb.jdbc.JDBCDriver'
	supports_statement_cache = True
	execution_ctx_cls = HyperSqlExecutionContext_jaydebeapi

	def create_connect_args(self, url):
		""" Returns a tuple consisting of a ``(*args, **kwargs)`` suitable to send directly to the dbapi's connect function. """
		# Example in parameter 'url' string:	"hsqldb+jaydebeapi://SA:***@localhost:9001/some_database_name"
		# Example 'jdbc_url' string:			"jdbc:hsqldb:hsql://localhost:9001/some_database_name"

		assert(type(url) is URL)
		url = make_url(url)

		jdbc_url = 'jdbc:hsqldb:hsql://' + url.host
		if url.port != None:
			jdbc_url += ':' + str(url.port)
		jdbc_url += '/' + url.database

		connectionArgs = {
			"jclassname": self.jclassname,
			"url": jdbc_url,
			"driver_args": [url.username, url.password],
			"jars" : self.classpath,
		}
		return ([], connectionArgs)

	@classmethod
	def import_dbapi(cls) -> ModuleType:
		return __import__("jaydebeapi_hsqldb")

dialect = HyperSqlDialect_jaydebeapi

