# Pebble94464, Copyright 2024
# TODO: clean up and remove anything not hsqldb specific.

from sqlalchemy import and_
from sqlalchemy import bindparam
from sqlalchemy import cast
from sqlalchemy import Computed
from sqlalchemy import delete # jsn
from sqlalchemy import exc
from sqlalchemy import except_
from sqlalchemy import ForeignKey
from sqlalchemy import func
from sqlalchemy import Identity
from sqlalchemy import Index
from sqlalchemy import insert
from sqlalchemy import Integer
from sqlalchemy import literal
from sqlalchemy import literal_column
from sqlalchemy import MetaData
from sqlalchemy import or_
from sqlalchemy import outerjoin
from sqlalchemy import schema
from sqlalchemy import select
from sqlalchemy import Sequence
from sqlalchemy import sql
from sqlalchemy import String
from sqlalchemy import testing
from sqlalchemy import text
from sqlalchemy import type_coerce
from sqlalchemy import TypeDecorator
from sqlalchemy import types as sqltypes
from sqlalchemy import union
# from sqlalchemy.dialects.hsqldb import hsqldb
# from sqlalchemy.dialects.hsqldb import base as hsqldb
from sqlalchemy.engine import default
from sqlalchemy.sql import column
from sqlalchemy.sql import ddl
from sqlalchemy.sql import quoted_name
from sqlalchemy.sql import table
from sqlalchemy.sql.selectable import LABEL_STYLE_TABLENAME_PLUS_COL
from sqlalchemy.testing import assert_raises_message
from sqlalchemy.testing import AssertsCompiledSQL
from sqlalchemy.testing import config # jsn
from sqlalchemy.testing import eq_
from sqlalchemy.testing import fixtures
from sqlalchemy.testing.assertions import eq_ignore_whitespace
from sqlalchemy.testing.schema import Column
from sqlalchemy.testing.schema import Table
from sqlalchemy.types import TypeEngine

class CompileTest(fixtures.TestBase, AssertsCompiledSQL):
	# __dialect__ = "hsqldb"
	__dialect__ = "hsqldb.jaydebeapi" # seems to work, matching registry value in conftest.py

	@testing.skip('hsqldb', reason="Not a real test")
	def test_dummy(self):
		""" This function was used for investigations. It's not a valid test. Can be removed from final release."""
		with config.db.connect() as conn:
			result = conn.execute(text('SELECT * FROM information_schema.system_sessioninfo'))
			for row in result:
				print('  ', repr(row))
				# To display captured standard output, call pytest with the -rP switch, e.g.
				# pytest -rP --db hsqldb0  test/test_compiler.py::CompileTest::test_dummy
		return None
	# TODO: Remove test_dummy from test suite.

	@testing.skip('hsqldb', reason="hsqldb doesn't support DELETE FROM statements with multiple tables specified")
	def test_delete_extra_froms(self):
		t1 = table("t1", column("c1"))
		t2 = table("t2", column("c1"))
		q = delete(t1).where(t1.c.c1 == t2.c.c1)
		self.assert_compile(q, "DELETE FROM t1 FROM t1, t2 WHERE t1.c1 = t2.c1") # The second param is the expected result.
	# TODO: remove

	@testing.skip('hsqldb', reason="hsqldb doesn't support DELETE FROM statements with multiple tables specified")
	def test_delete_extra_froms_alias(self):
		a1 = table("t1", column("c1")).alias("a1")
		t2 = table("t2", column("c1"))
		q = delete(a1).where(a1.c.c1 == t2.c.c1)
		self.assert_compile(q, "DELETE FROM t1 AS a1 FROM t1, t2 WHERE a1.c1 = t2.c1") # ? syntax
	# TODO: remove

	def test_table_options(self):
		m = MetaData()
		t = Table(
			"foo",
			m,
			Column("x", Integer),
			prefixes=["GLOBAL TEMPORARY"],
			#- Should GLOBAL TEMPORARY be specified as a prefix or hsqldb_type? See construct_arguments in base.py
			hsqldb_on_commit="PRESERVE ROWS",
		)
		self.assert_compile(
			schema.CreateTable(t),
			"CREATE GLOBAL TEMPORARY TABLE "
			"foo (x INTEGER) ON COMMIT PRESERVE ROWS",
		)
	#- Based on Oracle's "test_table_options" test.
	#- PostgreSQL has a similar test named "test_create_table_with_oncommit_option", and an additional test for multiple table options.
	#- pytest -rP --db hsqldb0  test/test_compiler.py::CompileTest::test_table_options

