
import datetime
from jpype import JClass
from sqlalchemy.engine import default
from sqlalchemy.engine import reflection
from sqlalchemy import BindTyping
from sqlalchemy import exc
from sqlalchemy import pool
from sqlalchemy import schema
from sqlalchemy import select
from sqlalchemy import util
from sqlalchemy import values
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy.sql import compiler
from sqlalchemy.sql import sqltypes
from sqlalchemy.sql import quoted_name
from sqlalchemy import types
from typing import Optional

def _getDictFromList(key, val, theList):
	"""Returns the first dictionary with a matching key value or None."""
	for dict in theList:
		item = dict.get(key)
		if item == val:
			return dict
	return None
	# TODO: update code to use this method, if it's quicker than the filter method.

# List of SQL Standard Keywords...
RESERVED_WORDS_1 = set(
"""ABS ALL ALLOCATE ALTER AND ANY ARE ARRAY AS ASENSITIVE ASYMMETRIC AT ATOMIC
AUTHORIZATION AVG BEGIN BETWEEN BIGINT BINARY BLOB BOOLEAN BOTH BY CALL CALLED
CARDINALITY CASCADED CASE CAST CEIL CEILING CHAR CHAR_LENGTH CHARACTER
CHARACTER_LENGTH CHECK CLOB CLOSE COALESCE COLLATE COLLECT COLUMN COMMIT
COMPARABLE CONDITION CONNECT CONSTRAINT CONVERT CORR CORRESPONDING COUNT
COVAR_POP COVAR_SAMP CREATE CROSS CUBE CUME_DIST CURRENT CURRENT_CATALOG
CURRENT_DATE CURRENT_DEFAULT_TRANSFORM_GROUP CURRENT_PATH CURRENT_ROLE
CURRENT_SCHEMA CURRENT_TIME CURRENT_TIMESTAMP CURRENT_TRANSFORM_GROUP_FOR_TYPE
CURRENT_USER CURSOR CYCLE DATE DAY DEALLOCATE DEC DECIMAL DECLARE DEFAULT
DELETE DENSE_RANK DEREF DESCRIBE DETERMINISTIC DISCONNECT DISTINCT DO DOUBLE
DROP DYNAMIC EACH ELEMENT ELSE ELSEIF END END_EXEC ESCAPE EVERY EXCEPT EXEC
EXECUTE EXISTS EXIT EXP EXTERNAL EXTRACT FALSE FETCH FILTER FIRST_VALUE FLOAT
FLOOR FOR FOREIGN FREE FROM FULL FUNCTION FUSION GET GLOBAL GRANT GROUP
GROUPING HANDLER HAVING HOLD HOUR IDENTITY IN INDICATOR INNER INOUT INSENSITIVE
INSERT INT INTEGER INTERSECT INTERSECTION INTERVAL INTO IS ITERATE JOIN LAG
LANGUAGE LARGE LAST_VALUE LATERAL LEAD LEADING LEAVE LEFT LIKE LIKE_REGEX LN
LOCAL LOCALTIME LOCALTIMESTAMP LOOP LOWER MATCH MAX MAX_CARDINALITY MEMBER
MERGE METHOD MIN MINUTE MOD MODIFIES MODULE MONTH MULTISET NATIONAL NATURAL
NCHAR NCLOB NEW NO NONE NORMALIZE NOT NTH_VALUE NTILE NULL NULLIF NUMERIC
OCCURRENCES_REGEX OCTET_LENGTH OF OFFSET OLD ON ONLY OPEN OR ORDER OUT OUTER
OVER OVERLAPS OVERLAY PARAMETER PARTITION PERCENT_RANK PERCENTILE_CONT
PERCENTILE_DISC PERIOD POSITION POSITION_REGEX POWER PRECISION PREPARE PRIMARY
PROCEDURE RANGE RANK READS REAL RECURSIVE REF REFERENCES REFERENCING REGR_AVGX
REGR_AVGY REGR_COUNT REGR_INTERCEPT REGR_R2 REGR_SLOPE REGR_SXX REGR_SXY
REGR_SYY RELEASE REPEAT RESIGNAL RESULT RETURN RETURNS REVOKE RIGHT ROLLBACK
ROLLUP ROW ROW_NUMBER ROWS SAVEPOINT SCOPE SCROLL SEARCH SECOND SELECT
SENSITIVE SESSION_USER SET SIGNAL SIMILAR SMALLINT SOME SPECIFIC SPECIFICTYPE
SQL SQLEXCEPTION SQLSTATE SQLWARNING SQRT STACKED START STATIC STDDEV_POP
STDDEV_SAMP SUBMULTISET SUBSTRING SUBSTRING_REGEX SUM SYMMETRIC SYSTEM
SYSTEM_USER TABLE TABLESAMPLE THEN TIME TIMESTAMP TIMEZONE_HOUR TIMEZONE_MINUTE
TO TRAILING TRANSLATE TRANSLATE_REGEX TRANSLATION TREAT TRIGGER TRIM TRIM_ARRAY
TRUE TRUNCATE UESCAPE UNDO UNION UNIQUE UNKNOWN UNNEST UNTIL UPDATE UPPER USER
USING VALUE VALUES VAR_POP VAR_SAMP VARBINARY VARCHAR VARYING WHEN WHENEVER
WHERE WHILE WIDTH_BUCKET WINDOW WITH WITHIN WITHOUT YEAR"""
.split())

# List of SQL Keywords Disallowed as HyperSQL Identifiers...
RESERVED_WORDS_2 = set(
"""ALL AND ANY AS AT AVG BETWEEN BOTH BY CALL CASE CAST COALESCE CONVERT
CORRESPONDING COUNT CREATE CROSS CUBE DEFAULT DISTINCT DROP ELSE EVERY EXCEPT
EXISTS FETCH FOR FROM FULL GRANT GROUP GROUPING HAVING IN INNER INTERSECT INTO
IS JOIN LEADING LEFT LIKE MAX MIN NATURAL NOT NULLIF ON OR ORDER OUTER PRIMARY
REFERENCES RIGHT ROLLUP SELECT SET SOME STDDEV_POP STDDEV_SAMP SUM TABLE THEN
TO TRAILING TRIGGER UNION UNIQUE USING VALUES VAR_POP VAR_SAMP WHEN WHERE WITH"""
.split())

# Special Function Keywords...
RESERVED_WORDS_3 = set("CURDATE CURTIME NOW SYSDATE SYSTIMESTAMP TODAY".split())


class _LargeBinary(types.BLOB):
	__visit_name__ = "BLOB"

	def result_processor(self, dialect, coltype):
		def process(value):
			assert repr(value) == "<java object 'org.hsqldb.jdbc.JDBCBlobClient'>" # type check for Java object
			return bytes(value.getBytes(1,int(value.length())))
		return process

class HyperSqlBoolean(types.BOOLEAN):
	__visit_name__ = "BOOLEAN"
	def result_processor(self, dialect, coltype):
		def process(value):
			if value == None:
				return value
			assert str(type(value)) == "<java class 'java.lang.Boolean'>" # type check for Java object
			return bool(value)
		return process

class _TIME_WITH_TIME_ZONE(sqltypes.TIME):
	__visit_name__ = 'TIME'
	render_bind_cast = True

	def __init__(self, timezone: bool = True, precision: Optional[int] = None):
		# Note timezone must be set to True for TIME WITH TIME ZONE.
		"""
		Construct a new :class:`_hsqldb._TIME_WITH_TIME_ZONE`.
		:param timezone: boolean.  Indicates that the TIME type should
		use HyperSQL's ``TIME WITH TIME ZONE`` datatype.
		"""
		# TODO: update description above
		super().__init__(timezone=timezone)

	def bind_processor(self, dialect):
		assert self.timezone == True, "Timezone must be True for type TIME WITH TIME ZONE"

		def process(value):
			""" convert datetime.time to java.time.OffsetTime """
			if value == None:
				return value
			assert isinstance(value, datetime.time), 'Expecting value to be a datetime.time'
			hour = value.hour
			minute = value.minute
			second = value.second
			nano = value.microsecond * 1000
			timedelta = value.tzinfo.utcoffset(None)
			JOffsetTime = JClass('java.time.OffsetTime', False)
			JZoneOffset = JClass('java.time.ZoneOffset')
			return JOffsetTime.of(hour, minute, second, nano, JZoneOffset.ofTotalSeconds(timedelta.seconds))
		return process

class _TIME(sqltypes.TIME):
	__visit_name__ = 'TIME'
	render_bind_cast = True

	# HSQLDB's TIME datatype has a precision setting, but it seems to have no effect,
	# and fractions of a second the underlying java.sql.Time are stored in milliseconds,
	# which is less precise than the microseconds used for datetime.
	# TODO: investigate how other dialects handle fractions of a second for TIME.
	# TODO: impl precision param for hsqldb's TIME class if needed.

	def __init__(self, timezone: bool = False, precision: Optional[int] = None):
		"""
		Construct a new :class:`_hsqldb.TIME`.
		:param timezone: boolean.  Indicates that the TIME type should
		use HyperSQL's ``TIME`` datatype.
		"""
		# TODO: update description above
		super().__init__(timezone=timezone)

	def get_dbapi_type(self, dbapi):
		assert True, 'get_dbapi_type: When does this function get called? '
		return dbapi.TIME
	# TODO: Remove assertion when purpose of get_dbapi_type is understood.

	def bind_processor(self, dialect):
		def process(value):
			assert isinstance(value, datetime.time), 'Expecting a datetime.time object'

			if value.microsecond % 1000 > 0:
				print('# Warning: potential precision loss while converting from microseconds to milliseconds')
			# TODO: How best to show potential precision loss, log warning?

			return dialect.dbapi.Time(
				value.hour,
				value.minute,
				value.second
				)
		return process
		# TODO: test with other timezone / dst combinations, like -4 hrs UTC Atlantic time (Canada), with and without DST.

class INTEGER(sqltypes.INTEGER):
	render_bind_cast = True

	def __init__(self, *args):
		if len(args) > 0:
			breakpoint() #-
		super().__init__(*args)

class TIMESTAMP(sqltypes.TIMESTAMP):
	__visit_name__ = 'TIMESTAMP'
	render_bind_cast = True

	def __init__(self, timezone: bool = False, precision: Optional[int] = None):
		"""
		Construct a new :class:`_hsqldb.TIMESTAMP`.
		:param timezone: boolean.  Indicates that the TIMESTAMP type should
		use HyperSQL's ``TIMESTAMP WITH TIME ZONE`` datatype.
		"""
		super().__init__(timezone=timezone)
	# TODO: implement support for 'precision'. Defaults to 6 for timestamps.

	def bind_processor(self, dialect):
		def processor(value):
			if type(value) != datetime.datetime:
				return None
			year = value.year - 1900
			month = value.month - 1
			day = value.day
			hour = value.hour
			minute = value.minute
			second = value.second
			nano = value.microsecond * 1000
			JTimestamp = JClass('java.sql.Timestamp', False)
			return JTimestamp(year, month, day, hour, minute, second, nano)
		return processor

class _TIMESTAMP_WITH_TIME_ZONE(sqltypes.TIMESTAMP):
	__visit_name__ = 'TIMESTAMP'
	render_bind_cast = True

	def __init__(self, timezone: bool = True, precision: Optional[int] = None):
		super().__init__(timezone=timezone)

	def bind_processor(self, dialect):
		def processor(value):
			if type(value) != datetime.datetime:
				return None
			assert isinstance(value, datetime.datetime), 'Expecting a datetime.datetime object'
			year = value.year
			month = value.month
			day = value.day
			hour = value.hour
			minute = value.minute
			second = value.second
			nano = value.microsecond * 1000
			timedelta = value.tzinfo.utcoffset(None)
			JOffsetDateTime = JClass('java.time.OffsetDateTime', False)
			#- https://docs.oracle.com/javase/8/docs/api/java/time/OffsetDateTime.html
			JZoneOffset = JClass('java.time.ZoneOffset')
			#- https://docs.oracle.com/javase/8/docs/api/java/time/ZoneOffset.html
			return JOffsetDateTime.of(year, month, day, hour, minute, second, nano, JZoneOffset.ofTotalSeconds(timedelta.seconds))
		return processor
	# HSQLDB uses java.time.OffsetDateTime to store timestamps with a timezone.
	# This class is required so we can set timezone to True, and have the bind
	# processor return an OffsetDateTime object.

class _Date(sqltypes.Date):
	__visit_name__ = "DATE"
	render_bind_cast = True

	def bind_processor(self, dialect):
		def processor(value):
			assert isinstance(value, datetime.date) or value is None, "_Date bind processor expects datetime.date, datetime.datetime, or None" #-
			if isinstance(value, datetime.date) == False:
				return None
			year = value.year - 1900
			month = value.month - 1
			day = value.day
			JDate = JClass('java.sql.Date')
			return JDate(year, month, day)
		return processor

colspecs = {
	sqltypes.LargeBinary: _LargeBinary,
	sqltypes.Boolean: HyperSqlBoolean,
	sqltypes.Date: _Date,
	sqltypes.DateTime: TIMESTAMP, 	# How to separate TIMESTAMPS with and without timezones?
	sqltypes.Time: _TIME,
	sqltypes.Integer: INTEGER,
}

ischema_names = {
	"BLOB": sqltypes.BLOB,
	"BIGINT": sqltypes.BIGINT,
	"CHARACTER": sqltypes.CHAR,
	"DOUBLE" : sqltypes.DOUBLE,
	"INTEGER": sqltypes.INTEGER,
	"NUMERIC": sqltypes.NUMERIC,
	"VARCHAR": sqltypes.VARCHAR,
	"DATE": _Date,
	"TIME": _TIME,
	"TIME WITH TIME ZONE": _TIME_WITH_TIME_ZONE,
	"TIMESTAMP": TIMESTAMP,
	"TIMESTAMP WITH TIME ZONE": _TIMESTAMP_WITH_TIME_ZONE,
}
  # TODO: ensure class names follow the naming convension

class HyperSqlCompiler(compiler.SQLCompiler):
	has_out_parameters = True

	def delete_extra_from_clause(self, delete_stmt, from_table, extra_froms, from_hints, **kw):
		"""Render the DELETE .. FROM clause. Not currently supported by HSQLDB. """
		raise NotImplementedError(
			"HSQLDB doesn't support multiple tables in DELETE FROM statements",
			"e.g. DELETE FROM t1, t2 WHERE t1.c1 = t2.c1"
		)

	def fetch_clause(self, select, fetch_clause=None, require_offset=False, use_literal_execute_for_simple_int=False, **kw, ):
		raise NotImplementedError('xxx: fetch_clause')

	def for_update_clause(self, select, **kw):
		raise NotImplementedError('xxx: for_update_clause')

	def format_from_hint_text(self, sqltext, table, hint, iscrud):
		raise NotImplementedError('xxx: format_from_hint_text')

	def function_argspec(self, func, **kwargs):
		raise NotImplementedError('xxx: function_argspec')

	def get_crud_hint_text(self, table, text):
		raise NotImplementedError('xxx: get_crud_hint_text')

	def get_cte_preamble(self, recursive):
		raise NotImplementedError('xxx: get_cte_preamble')

	def get_from_hint_text(self, table, text):
		raise NotImplementedError('xxx: get_from_hint_text')

	def get_select_hint_text(self, byfroms):
		raise NotImplementedError('xxx: get_select_hint_text')

	def get(lastrowid, parameters):
		raise NotImplementedError('xxx: get')

	def decorator_disable_bind_casts(f):
		''' A decorator to disable the rendering of casts for bound types. '''
		# Bind typing for this dialect is set to RENDER_CASTS.  Applying this
		# setting causes all bound parameters to be cast, which is not 
		# necessarily what we want. For example HSQLDB will error if we attempt
		# to cast a value on a limit clause.
		def inner_func(*args, **kwargs):
			self = args[0]
			assert isinstance(self, HyperSqlCompiler), 'Decorator can only be used on HyperSqlCompiler methods'

			self.dialect._bind_typing_render_casts = False
			result = f(*args, **kwargs)
			self.dialect._bind_typing_render_casts = True
			return result
		return inner_func
	# TODO: Review code. What's the proper way to define decorators for use with class methods?
	# TODO: Consider in-lining code if it's not used in places other than limit_clause.

	@decorator_disable_bind_casts
	def limit_clause(self, select, **kw):
		# HSQLDB 2.7.2 doesn't support the casting of bound parameters for
		# limit clauses. Use decorator_disable_bind_casts.
		text = ""
		if select._limit_clause is not None:
			text += " \n LIMIT " + self.process(select._limit_clause, **kw)
		if select._offset_clause is not None:
			if select._limit_clause is None:
				text += "\n LIMIT 0"	# For HSQLDB zero means no limit
			text += " OFFSET " + self.process(select._offset_clause, **kw)
		return text

	def render_bind_cast(self, type_, dbapi_type, sqltext):
		return f"""CAST({sqltext} AS {
				self.dialect.type_compiler_instance.process(
					dbapi_type, identifier_preparer=self.preparer
				)})"""

	def returning_clause(self, stmt, returning_cols, *, populate_result_map, **kw, ) -> str:
		raise NotImplementedError('xxx: returning_clause')

	def translate_select_structure(self, select_stmt, **kwargs):
		# HSQLDB 2.7.2 doesn't support direct selections, but we can work
		# around this limitation by using a values clause inside a subquery,
		# e.g. translate 'SELECT ?' to 'SELECT * ( VALUES(?) )'
		froms = self._display_froms_for_select(
			select_stmt, kwargs.get("asfrom", False))
		if len(froms) == 0 and select_stmt._whereclause is None:
			vals = values(*select_stmt.selected_columns).data(
				[tuple([
					c.value
					for c in select_stmt.selected_columns
					])])
			restructured_select = select('*').select_from(vals)
			return restructured_select

		#- Translate... SELECT :param_1 AS anon_1   WHERE EXISTS (SELECT *   FROM stuff   WHERE stuff.data = :data_1)
		#- pytest -rP -x --db hsqldb test/test_suite.py::ExistsTest::test_select_exists_false
		if len(froms) == 0 and select_stmt._whereclause is not None:
			raise NotImplementedError('###: Code for WHERE EXISTS hasn\'t been implemented.')
			# If the error above is raised for something other than WHERE EXISTS,
			# we need to refine the entry to this block. Make a note of it for further investigation.
		return select_stmt

	def update_from_clause(self, update_stmt, from_table, extra_froms, from_hints, **kw):
		raise NotImplementedError('xxx: update_from_clause')

	def update_limit_clause(self, update_stmt):
		raise NotImplementedError('xxx: update_limit_clause')

	def update_tables_clause(self, update_stmt, from_table, extra_froms, **kw):
		raise NotImplementedError('xxx: update_tables_clause')

	def visit_empty_set_expr(self, element_types, **kw):
		raise NotImplementedError('xxx: visit_empty_set_expr')

	def visit_extract(self, extract, **kwargs):
		raise NotImplementedError('xxx: visit_extract')

	def visit_function(self, func, add_to_result_map=None, **kwargs, ) -> str:
		raise NotImplementedError('xxx: visit_function')

	def visit_ilike_case_insensitive_operand(self, element, **kw):
		raise NotImplementedError('xxx: visit_ilike_case_insensitive_operand')

	def visit_ilike_op_binary(self, binary, operator, **kw):
		raise NotImplementedError('xxx: visit_ilike_op_binary')

	def visit_join(self, join, asfrom=False, from_linter=None, **kwargs):
		raise NotImplementedError('xxx: visit_join')

	def visit_mod_binary(self, binary, operator, **kw):
		raise NotImplementedError('xxx: visit_mod_binary')

	def visit_not_ilike_op_binary(self, binary, operator, **kw):
		raise NotImplementedError('xxx: visit_not_ilike_op_binary')

	def visit_not_regexp_match_op_binary(self, binary, operator, **kw):
		raise NotImplementedError('xxx: visit_not_regexp_match_op_binary')

	def visit_regexp_match_op_binary(self, binary, operator, **kw):
		raise NotImplementedError('xxx: visit_regexp_match_op_binary')

	def visit_regexp_replace_op_binary(self, binary, operator, **kw):
		raise NotImplementedError('xxx: visit_regexp_replace_op_binary')

	def visit_rollback_to_savepoint(self, savepoint_stmt, **kw):
		raise NotImplementedError('xxx: visit_rollback_to_savepoint')

	def visit_savepoint(self, savepoint_stmt, **kw):
		raise NotImplementedError('xxx: visit_savepoint')

	def visit_sequence(self, sequence, **kw):
		raise NotImplementedError('xxx: visit_sequence')

	def visit_table_valued_column(self, element, **kw):
		raise NotImplementedError('xxx: visit_table_valued_column')

class HyperSqlDDLCompiler(compiler.DDLCompiler):

	def define_constraint_deferrability(self, constraint):
		if constraint.initially is not None:
			raise exc.CompileError("Constraint deferrability is not currently supported")
		return super().define_constraint_deferrability(constraint)
	# "The deferrable characteristic is an optional element of CONSTRAINT definition, not yet supported by HyperSQL."

	def define_constraint_match(self, constraint):
		#- assert constraint.match in ['FULL', 'PARTIAL', 'SIMPLE']
		return compiler.DDLCompiler.define_constraint_match(self, constraint)
	# MATCH is a keyword for HSQLDB, used with FK constraints.
	# See: https://hsqldb.org/doc/2.0/guide/databaseobjects-chapt.html
	# TODO: verify inherited define_constraint_match method works as expected for HSQLDB. If so, delete this override.

	def get_column_specification(self, column, **kwargs):
		"""Builds column DDL."""

		# A column definition consists of a <column name>...
		colspec = self.preparer.format_column(column)

		# and in most cases a <data type> or <domain name>...
		colspec += " " + self.dialect.type_compiler_instance.process(
				column.type, type_expression=column
			)

		# The clauses below are mutually exclusive, but isn't reflected by code logic...
		# 	[ <default clause> | <identity column specification> | <identity column sequence specification> | <generation clause> ]
		# There appears to be a risk we'll end up with colspecs containing conflicting causes.
		# TODO: verify colspecs doesn't contain conflicting causes

		# <default clause>
		default = self.get_column_default_string(column)
		if default is not None:
			colspec += " DEFAULT " + default
		# The value of default should match a <default option>, i.e.
		#	<default option> ::= <literal> | <datetime value function> | USER | CURRENT_USER | CURRENT_ROLE | SESSION_USER | SYSTEM_USER | CURRENT_CATALOG | CURRENT_SCHEMA | CURRENT_PATH | NULL

		# <generation clause> ?
		if column.computed is not None:
			colspec += " " + self.process(column.computed) # See visit_computed_column()

		# <identity column specification>
		if (
			column.identity is not None
			and self.dialect.supports_identity_columns
		):
			colspec += " " + self.process(column.identity) # See compiler.DDLCompiler.visit_identity_column()

		# <update clause> - (seems to be missing in the docs https://hsqldb.org/doc/2.0/guide/databaseobjects-chapt.html)
		# Maybe it's the <on update clause>?
		# "This feature is not part of the SQL Standard and is similar to MySQL's ON UPDATE clause."
		# TODO: implement <update clause>

		# <column constraint definition> ?
		# Constraint definitions are missing here.
		# HSQLDB automatically turns column constraint definitions into table constraint definitions.
		# Perhaps SQLAlchemy defines constraints on tables only?

		# Except for the NOT NULL constraint...
		if not column.nullable and (
			not column.identity or not self.dialect.supports_identity_columns
		):
			# In other words, if not nullable and not an identity column then append...
			colspec += " NOT NULL"

		# <collate clause>
		# TODO: implement collate clause?

		return colspec
	# See 'column definition' in...
	# 	http://www.hsqldb.org/doc/2.0/guide/databaseobjects-chapt.html#dbc_table_creation
	#
	# Except for added comments, the function above is practically identical to the default implementation.
	# TODO: inherit the get_column_specification method from compiler.DDLCompiler

	def get_identity_options(self, identity_options):
		assert identity_options.cache is None, "HSQLDB doesn't support identity_options.cache"
		return compiler.DDLCompiler.get_identity_options(self, identity_options)
	# HSQLDB appears to support most of the identity options found in
	# compiler.DDLCompiler.get_identity_options method, except for "CACHED".
	#
	# See "<common sequence generator options>" under the "CREATE SEQUENCE" section
	# 	https://hsqldb.org/doc/2.0/guide/databaseobjects-chapt.html
	#
	# HSQLDB also has a sequence generator option named 'AS', which doesn't appear
	# to be supported by compiler.DDLCompiler.get_identity_options.
	# TODO:3: implement support for identity_option 'AS'

	def post_create_table(self, table):
		"""Build table-level CREATE options like ON COMMIT and COLLATE."""
		table_opts = []
		opts = table.dialect_options['hsqldb']
		if opts['on_commit']:
			on_commit_options = opts['on_commit'].replace('_', ' ').upper()
			table_opts.append(' ON COMMIT %s' % on_commit_options)
		return ' '.join(table_opts)
	# TODO: Is this the place to implement the <collate clause>?

	def visit_create_table(self, create, **kw):
		table = create.element
		preparer = self.preparer

		text = "\nCREATE "

		if table._prefixes:
			text += " ".join(table._prefixes) + " "
		# TODO: What are table prefixes? Are they similar to hsqldb_type?

		hsqldb_type = table.dialect_options['hsqldb']['type']
		# The line above generates an error... "sqlalchemy.exc.NoSuchModuleError: Can't load plugin: sqlalchemy.dialects:hsqldb"
		# It's because 'hsqldb.jaydebeapi' != 'hsqldb' when attempting to load the library; See: \sqlalchemy\util\langhelpers.py(~362)
		if hsqldb_type is not None:
			text += hsqldb_type + " "
		# TODO: restrict hsqldb_type to valid types, e.g. [MEMORY | CACHED | [GLOBAL] TEMPORARY | TEMP | TEXT ]

		text += "TABLE "
		if create.if_not_exists:
			text += "IF NOT EXISTS "

		text += preparer.format_table(table) + " "

		create_table_suffix = self.create_table_suffix(table)
		if create_table_suffix:
			text += create_table_suffix + " "

		text += "("

		separator = "\n"

		# if only one primary key, specify it along with the column
		first_pk = False
		for create_column in create.columns:
			column = create_column.element
			try:
				processed = self.process(
					create_column, first_pk=column.primary_key and not first_pk
				)
				if processed is not None:
					text += separator
					separator = ", \n"
					text += "\t" + processed
				if column.primary_key:
					first_pk = True
			except exc.CompileError as ce:
				raise exc.CompileError(
					"(in table '%s', column '%s'): %s"
					% (table.description, column.name, ce.args[0])
				) from ce

		const = self.create_table_constraints(
			table,
			_include_foreign_key_constraints=create.include_foreign_key_constraints,  # noqa
		)
		if const:
			text += separator + "\t" + const

		text += "\n)%s\n\n" % self.post_create_table(table)
		return text
		# This method overrides the base method to allow us to specify hsqldb_type,
  		# a table type such as [MEMORY | CACHED | [GLOBAL] TEMPORARY | TEMP | TEXT ]
		# The base method inserts table._prefixes, which hsqldb_type might
		# duplicate the purpose of.
		# TODO: review whether overriding visit_create_table is necessary.

	def visit_computed_column(self, generated, **kw):
		if generated.persisted is False:
			raise exc.CompileError(
				"Virtual computed columns are unsupported."
				"Please set the persisted flag to None or True."
			)
		return "GENERATED ALWAYS AS (%s)" % self.sql_compiler.process(
			generated.sqltext, include_table=False, literal_binds=True
		)

 
	@compiles(schema.CreateIndex, 'hsqldb')
	def _compile_create_index(createIndexObj, compiler, **kw):
		index = createIndexObj.element
		if index.unique == True and False:
			# Unique indexes are deprecated in HSQLDB since version 1.8,
			# so we need to generate DDL for a unique constraint instead.

			uc = UniqueConstraint(index.columns, name=index.name, _column_flag=False)
			raise exc.CompilerError('Unique indexes are deprecated. Use a unique constraint instead.')

			raise NotImplementedError
			return compiler.visit_add_constraint(uc, **kw)

			# index.table.append_constraint(uc)
			return compiler.visit_create_unique_index(index, **kw) # This to create a unique constraint
			# Don't add a UniqueConstraint to the metadata because that could cause other DBMSs to generate a UC.
			return compiler.visit_unique_constraint(index, **kw) #- failed
		else:
			return compiler.visit_create_index(createIndexObj, **kw)

	def visit_create_index(self, create, include_schema=False, include_table_schema=True, **kw):
		index = create.element
		self._verify_index_table(index)
		preparer = self.preparer

		if index.unique == True and False: # temporarily disabled with False
			# Add a table-level UNIQUE constraint...
			table = index.table
			table.indexes.remove(index)
			uc = UniqueConstraint(index.columns, name=index.name)
			table.append_constraint(uc)
			return None
		else:
			if index.name is None:
				raise exc.CompileError("CREATE INDEX requires an index name.")
			text = "CREATE INDEX "
			if create.if_not_exists:
				text += "IF NOT EXISTS "
			text += "%s ON %s (%s)" % (
				self._prepared_index_name(index, include_schema=include_schema),
				preparer.format_table(index.table, use_schema=include_table_schema),
				", ".join(
					self.sql_compiler.process(
						expr, include_table=False, literal_binds=True
					)
					for expr in index.expressions
				),
			)
			return text
			# Support for the ASC|DESC option not implemented because specifying
			# the sort order for indexes has no effect in HSQLDB. The asc_or_desc
   			# column is always set to 'A'.
			# TODO: Is there a case for spoofing the setting, for example to preserve the sort order between DBs?
			# TODO: Consider raising an error when desc() is called. 

	def visit_create_sequence(self, create, **kw):
		prefix = None
		if create.element.data_type is not None:
			data_type = create.element.data_type
			prefix = " AS %s" % self.type_compiler.process(data_type)
		return super().visit_create_sequence(create, prefix=prefix, **kw)

	def visit_drop_column_comment(self, drop, **kw):
		return "COMMENT ON COLUMN %s IS ''" % self.preparer.format_column(
			drop.element, use_table=True
		)
	# COMMENT ON statement only accepts a character string literal, not a NULL,
	# even though an unset comment is initially NULL.
	# TODO: consider updating INFORMATION_SCHEMA.SYSTEM_COLUMNS.REMARKS directly.

	def visit_drop_constraint_comment(self, drop, **kw):
		raise exc.CompileError("Constraint comments are not supported.")
	# HSQLDB doesn't support comments on constraints.

	def visit_drop_constraint(self, drop, **kw):
		constraint = drop.element
		if constraint.name is not None:
			formatted_name = self.preparer.format_constraint(constraint)
		else:
			formatted_name = None

		if formatted_name is None:
			raise exc.CompileError(
				"Can't emit DROP CONSTRAINT for constraint %r; "
				"it has no name" % drop.element
			)
		return "ALTER TABLE %s DROP CONSTRAINT %s %s %s" % (
			self.preparer.format_table(drop.element.table),
			formatted_name,
			"CASCADE" if drop.cascade else "RESTRICT",
		)
	# TODO: verify each kind of constraint is dropped, pk, fk, check, etc.

	def visit_drop_index(self, drop, **kw):
		index = drop.element
		if index.name is None:
			raise exc.CompileError(
				"DROP INDEX requires that the index have a name"
			)
		text = "\nDROP INDEX "
		text += self._prepared_index_name(index, include_schema=True)
		if drop.if_exists:
			text += " IF EXISTS"
		return text
	# "Will not work if the index backs a UNIQUE of FOREIGN KEY constraint".
	# TODO:3: Helpful to raise an exception if the index backs a unique or FK constraint?

	def visit_drop_table_comment(self, drop, **kw):
		return "COMMENT ON TABLE %s IS ''" % self.preparer.format_table(
			drop.element
		)
	# COMMENT ON statement only accepts a character string literal, not a NULL,
	# even though an unset comment is initially NULL.
	# TODO: consider updating INFORMATION_SCHEMA.SYSTEM_TABLES.REMARKS directly.

	def visit_drop_table(self, drop, **kw):
		assert hasattr(drop, 'cascade') == False, "We can make use of drop.cascade if it exist. See comments on visit_drop_table"
		text = "\nDROP TABLE "
		text += self.preparer.format_table(drop.element)
		if drop.if_exists:
			text += "IF EXISTS "
		# text += "CASCADE" if drop.cascade else "RESTRICT", # TODO: enable if drop.cascade exists.
		text += ";"
		return text
	# HSQLDB supports CASCADE when dropping tables...
	#	<drop table statement> ::= DROP TABLE [ IF EXISTS ] <table name> [ IF EXISTS ] <drop behavior>
	#	<drop behavior> ::= CASCADE | RESTRICT -- (I've not verified this particular line in the docs)
	#
	# SQLAlchemy doesn't appear to support CASCADE for dropping tables,
	# although the DDLCompiler.visit_drop_constraint method does support it for constraints.
	#
	# Maybe drop.cascade is only present for certain cases, or specifiable as an additional option?
	# Maybe SQLAlchemy doesn't need drop.cascade on tables?
	# TODO: implement support for drop.cascade on tables, if it's actually needed and doable.

class HyperSqlTypeCompiler(compiler.GenericTypeCompiler):

	def visit_TIMESTAMP(self, type_, **kw):
		if type_.timezone == True:
			return "TIMESTAMP WITH TIME ZONE"
		else:
			return "TIMESTAMP"
	# TODO: timestamp precision

	def visit_datetime(self, type_, **kw):
		return self.visit_TIMESTAMP(type_, **kw)

	def visit_TIME(self, type_, **kw):
		if type_.timezone == True:
			return "TIME WITH TIME ZONE"
		else:
			return "TIME"
	# TODO: time precision

class HyperSqlIdentifierPreparer(compiler.IdentifierPreparer):
	# Reserved words can be a union of sets 1 and 3, or 2 and 3.
	reserved_words = RESERVED_WORDS_1.union(RESERVED_WORDS_3)

	# Identifiers must begin with a letter...
	illegal_initial_characters = {str(dig) for dig in range(0, 10)}.union(['_', '$'])

	def __init__(self, dialect, **kwargs):
		super().__init__(dialect, **kwargs)

	# SQLAlchemy normalises identifiers by converting them to lowercase.
	# HSQLDB normalises them by converting to uppercase, as does Oracle, Firebird and DB2.
	# The format_table function below attempts to force the quoting of table names,
	# which helped solve one test failure but caused another.
	# None of the other dialects attempt to force quoting of table names this way,
	# so my implementation is likely wrong.
	# TODO: re-examine the test that format_table was meant to fix.
	# TODO: remove format_table below. (temporarily renamed format_tableX)
	def format_tableX(self, table, use_schema=True, name=None):
		"""Prepare a quoted table and schema name."""

		if name is None:
			name = table.name

		name = quoted_name(name, True)
		# HSQLDB normally changes table names to uppercase, unless the identifier is double quoted.
		# The line of code above is added to ensure the name is always wrapped in quotes.
		# An alternative solutions might be to ensure the name is converted to uppercase,
		# or maybe there is a configuration setting in HSQLDB or SQLAlchemy that changes the default behaviour. 

		result = self.quote(name)

		effective_schema = self.schema_for_object(table)

		if not self.omit_schema and use_schema and effective_schema:
			result = self.quote_schema(effective_schema) + "." + result
		return result

class HyperSqlExecutionContext(default.DefaultExecutionContext):
	def __init__(self):
		assert False, 'Does a HyperSqlExecutionContext object get instantiated?'
	# TODO: remove __init__ method if this class is never instantiated.

	def create_server_side_cursor(self):
		if self.dialect.supports_server_side_cursors:
			return self._dbapi_connection.cursor() # TODO: are any params required?
		else:
			raise NotImplementedError()
	# TODO: Should this function exist here or in HyperSqlExecutionContext_jaydebeapi?

	def fire_sequence(self, seq, type_):
		"""given a :class:`.Sequence`, invoke it and return the next int value"""
		raise NotImplementedError

	def get_insert_default(self):
		raise NotImplementedError

	def get_lastrowid(self):
		raise NotImplementedError

	def get_out_parameter_values(self, out_param_names):
		# this method should not be called when the compiler has
		# RETURNING as we've turned the has_out_parameters flag set to
		# False.
		if len(out_param_names) > 0:
			breakpoint() # Looking for an example of when this is called.
		# TODO: remove if block when usage of an out param is found and tested.
		assert not self.compiled.returning
		return [
			self.dialect._paramval(self.out_parameters[name])
			for name in out_param_names
		]
	# HSQLDB supports IN, OUT, and INOUT parameters for procedures, so we may
	# need to implement this method. The one above is based on Oracle's.
	# See (https://hsqldb.org/doc/guide/sqlroutines-chapt.html)
	# This method is called when HyperSqlExecutionContext.has_out_parameters
	# is set to True.

class HyperSqlDialect(default.DefaultDialect):
	"""HyperSqlDialect implementation of Dialect"""

	def __init__(self, classpath=None, **kwargs):
		default.DefaultDialect.__init__(self, **kwargs)
		self.classpath = classpath	# A path to the HSQLDB executable jar file.

	name = "hsqldb"

	requires_name_normalize = True
	# Methods 'normalize_name' and 'denormalize_name' are only used if requires_name_normalize = True
	# Like Oracle, HSQLDB identifiers are normalised to uppercase.
	# This setting appears to affect the case of keys in the row _mapping dictionary, (as used in the get_columns function)
	# 	True = lowercase, False = uppercase

	@DeprecationWarning
	@classmethod
	def dbapi(cls):
		"""
		A reference to the DBAPI module object itself. (DEPRECATED)
		It is replaced by import_dbapi, which has been implemented in jaydebeapi.py
		"""
		raise NotImplementedError
	# TODO: remove the deprecated function above.

	statement_compiler = HyperSqlCompiler
	ddl_compiler = HyperSqlDDLCompiler
	type_compiler_cls = HyperSqlTypeCompiler
	preparer = HyperSqlIdentifierPreparer
	execution_ctx_cls = HyperSqlExecutionContext
	supports_alter = True
	max_identifier_length = 128
	supports_server_side_cursors = True
	supports_sane_rowcount = True
	# Some drivers, particularly third party dialects for non-relational databases,
	# may not support _engine.CursorResult.rowcount at all.
	# The _engine.CursorResult.supports_sane_rowcount attribute will indicate this.
	#
	# Like MySql, Oracle, and PG, HSQLDB is a relational database, so I have set it to True.
	# Note that Access and sqlalchemy-jdbcapi have it set to False, reasons unknown.

	supports_sane_multi_rowcount = True
	# For an :ref:`executemany <tutorial_multiple_parameters>` execution,
	# _engine.CursorResult.rowcount may not be available either, which depends
	# highly on the DBAPI module in use as well as configured options.  The
	# attribute _engine.CursorResult.supports_sane_multi_rowcount indicates
	# if this value will be available for the current backend in use.
	#
	# The default is True. Other DBs are set to True. I suspect HSQLDB supports it too, so set it to True.
	# Note that Access and sqlalchemy set it to False, for some reason.

	supports_empty_insert = False
	# Unsure of the correct setting for 'supports_empty_insert'.
	# HSQLDB's INSERT statement can work without specifying columns, and
	# I've got a feeling auto generated values don't always need specifying.
	# The major dialects appear to set it to false, so I've done the same for now.
	# TODO: Confirm the correct setting for supports_empty_insert.

	supports_default_values = True
	supports_default_metavalue = True
	default_metavalue_token = "DEFAULT"
	supports_multivalues_insert = True

	insert_executemany_returning = False
	# RETURNING doesn't appear to be a recognised keyword.

	insert_executemany_returning_sort_by_parameter_order = False
	update_executemany_returning = False
	delete_executemany_returning = False

	use_insertmanyvalues = True
	# This setting likely has no effect for HSQLDB because it doesn't support RETURNING.
	# It can probably be set to either True or False (preferred).
	# However setting attribute 'use_insertmanyvalues_wo_returning' to True implies
	# a different code path is executed, one that doesn't depend on RETURNING.
	# Let's try setting both attributes to True for now and review the decision later.
	# TODO: compare with the generated when both the mentioned attributes are set to False

	use_insertmanyvalues_wo_returning = True
	# See TODO comments on 'use_insertmanyvalues'.

	insertmanyvalues_implicit_sentinel = (compiler.InsertmanyvaluesSentinelOpts.NOT_SUPPORTED)
	# The sentinel tests require 'insert_returning'. Not supported.

	insertmanyvalues_page_size = 0xFFFFFFFF # default value of DefaultDialect is 1000.
	insertmanyvalues_max_parameters = 0xFFFFFFFF # DefaultDialect's value is 32700
	#
	# HSQLDB does not impose limits on the size of databases (rows, columns, etc).
	# Does the VALUES statement limit the number of rows or columns specified?
	# Assuming it doesn't, the limits imposed by insertmanyvalues_page_size
	# and insertmanyvalues_max_parameters can be removed.
	#
	#  TODO: figure out the correct way to specify no limits for insertmanyvalues_page_size and insertmanyvalues_max_parameters.

	preexecute_autoincrement_sequences: False
	# The default value is False. PostgreSQL has it set to true.
	# TODO: verify correct setting for HSQLDB

	insert_returning = False
	update_returning = False
	update_returning_multifrom = False
	delete_returning = False
	delete_returning_multifrom = False
	favor_returning_over_lastrowid = False
	supports_identity_columns = True
	cte_follows_insert = False

	colspecs = colspecs
	ischema_names = ischema_names
	# ischema_names and colspecs are required members on the Dialect class, according to type_migration_guidelines.txt
	# TODO: although ischema_names is a required property of the Dialect class, it doesn't appear to be a property of the interface. Why?

	supports_sequences = True

	sequences_optional: True
	# TODO: verify correct setting for sequences_optional

	default_sequence_base = 0

	supports_native_enum = False
	# "HyperSQL translates MySQL's ENUM data type to VARCHAR with a check constraint on the enum values"

	supports_native_boolean = True
	# HSQLDB's BOOLEAN type conforms to the SQL Standard and represents the values TRUE, FALSE and UNKNOWN"

	supports_native_decimal = True
	supports_native_uuid = True
	returns_native_bytes = True

	construct_arguments = [
		(schema.Index, {}),
		(schema.Table, {
			"type": None,
			"on_commit": None,		# DELETE | PRESERVE | NULL
		})
	]
	# Not yet fully implemented because we don't immediately know what the valid parameters will be.
	# Providing a partial implementation with the expectation that an ArgumentError will be raised
	# when unrecognised parameters are encountered, so we can later fill in the blanks.
	#
	# Example entry...
	# 	(schema.Index, {
	# 		"using": False,
	# 		"where": None,
	# 		"ops": None
	# 	}),
	#
	# TODO: complete construct_arguments

	reflection_options = ()
	# TODO: reflection_options is currently empty. Remove or comment out if unused.

	dbapi_exception_translation_map = {
		# "SomeWarning" : "Warning",
		# "SomeError" : "Error",
		# "" : "InterfaceError",
		# "" : "DatabaseError",
		# "" : "DataError",
		# "" : "OperationalError",
		# "" : "IntegrityError",
		# "" : "InternalError",
		# "" : "ProgrammingError",
		# "" : "NotSupportedError",
	}
	# This dictionary maps DBAPI exceptions to the exceptions of
	# PEP 249 – Python Database API Specification v2.0.
	# See: (https://peps.python.org/pep-0249/#exceptions)
	# In most cases it will be empty apparently.
	# TODO: update dbapi_exception_translation_map as and when dbapi errors are encountered. Remove if not it remains empty.

	supports_comments = True
	# HyperSQL supports comments on tables and columns, possibly in some non-standard way though.
	# TODO: verify the effect of this setting on HSQLDB.

	inline_comments = False
	supports_constraint_comments = False

	supports_statement_cache = False
	# All other dialects set supports_statement_cache to True.
	# A release note indicates it should be set on a dialect, and that there's some check for it.
	# See comments in interfaces.py for more info.
	# It should also be set on derived classes.
	# Excluding it causes test 'test_binary_roundtrip' to fail.
	# Important detail, see: [Engine third-party caching](https://docs.sqlalchemy.org/en/20/core/connections.html#engine-thirdparty-caching)
	# TODO: revise / remove above comments

	bind_typing = BindTyping.RENDER_CASTS
	# bind_typing = BindTyping.NONE
	# When bind_typing is set to render casts it seems every occurance of a
	# bound type is explicitly cast, which is not necessarily what we want.
	# For example, we want to cast bound parameters inside a VALUES clause,
	# but not a LIMIT clause. We want to disable casting for limit clauses.
	# 
	# Internally the dialect property '_bind_typing_render_casts' is checked to
	# determine whether or not to render a cast.
	#
	# (In case you're thinking there's an alternative way to disable casts, by
	# setting bind_typing = BindTyping.NONE for specific clauses, it doesn't
	# work. I've already tried.)
	# 
	# There's more than one way to skin a cat... If we've set bind_typing to
	# NONE instead of RENDER_CASTS, no bound types will be cast and we will
	# then need to enable casting for specific clauses like VALUES.
	#
	# TODO: Is it better to default to BindTyping.RENDER_CASTS or BindTyping.NONE?  Currently undecided.

	is_async = False
	# We'll initially test with is_async set to false, in order to simplify debugging during development.
	# TODO: set is_async to True

	has_terminate = True
	# HSQLDB can terminate sessions or transactions in various ways using
	# statements ALTER SESSION, COMMIT, ROLLBACK, and DISCONNECT.
	# For details see https://hsqldb.org/doc/guide/sessions-chapt.html
	#
	# Is this what 'has_terminate' is used for?  Unsure, so let's set it to true
	# for now and wait for it to fail before attempting to implement support.

	engine_config_types = default.DefaultDialect.engine_config_types.union(
		{
			# "pool_timeout": util.asint,					# DefaultDialect
			# "echo": util.bool_or_str("debug"),			# DefaultDialect
			# "echo_pool": util.bool_or_str("debug"),		# DefaultDialect
			# "pool_recycle": util.asint,					# DefaultDialect
			# "pool_size": util.asint,						# DefaultDialect
			# "max_overflow": util.asint,					# DefaultDialect
			# "future": util.asbool,						# DefaultDialect
			"legacy_schema_aliasing": util.asbool			# mssql dialect - Deprecated and not applicable. Remove.
		}
	)
	# engine_config_types is currently unused. Leaving it here for now as an example in case we need it later.
	# Unsure what its purpose is / how it's used exactly, other than coercing a key's value to a type.
	# TODO: Remove engine_config_types if unused, or remove those commented out.

	label_length = 128
	# Unknown. Will assume label_length is the same value as max_identifier_length for now.
	# TODO: verify correct value for label_length

	supports_simple_order_by_label = True
	# Target database supports ORDER BY <labelname>, where <labelname>
	# refers to a label in the columns clause of the SELECT
	# TODO: can be removed / set to True if supported. Access has it set to False.

	div_is_floordiv: True
	tuple_in_values = True

	def initialize(self, connection):
		super().initialize(connection)
	# Allows dialects to configure options based on server version info or other properties.
	# E.g., self.supports_identity_columns = self.server_version_info >= (10,)

	@reflection.cache
	def get_columns(self, connection, table_name, schema=None, **kw):
		#-table_name = self.denormalize_name(table_name)
		if schema is None:
			schema = self.default_schema_name
		assert schema is not None
		reflectedColumns = []
		query = """
			SELECT
			a.column_name AS "name",
			-- TODO: 'type' has to possible fields, which differ slightly for certain data types. Choose one, remove the other...
			a.type_name AS "type",		-- e.g. VARCHAR
			b.data_type AS "type_b",	-- e.g. CHARACTER VARYING
			-- TODO: 'nullable' has to possible fields, with either YES/NO or 0/1 values. Choose one and remove the other...
			a.nullable AS "nullable_01", -- 0 OR 1
			a.is_nullable AS "nullable_yesno", -- YES or NO
			a.column_def AS "default", -- TODO: What does COLUMN_DEF represent, default value, or definition?
			a.is_autoincrement AS "autoincrement",
			a.remarks AS "comment",
			-- NULL AS "computed", -- TODO: Does HSQLDB have an appropriate field?
			b.is_identity AS "identity",
			-- NULL AS "dialect_options", -- TODO: Does HSQLDB have an appropriate field?
			b.numeric_precision,
			b.numeric_scale,
			b.character_maximum_length
			FROM information_schema.system_columns AS a
			LEFT JOIN information_schema.columns AS b
			ON a.table_name = b.table_name
			AND a.column_name = b.column_name
			AND a.table_schem = b.table_schema
			AND a.table_cat = b.table_catalog -- TODO: Document or fix potential area of failure. Catalogs with duplicate objects.
			WHERE a.table_name = (?)
			AND a.table_schem = (?)
			"""
		cursorResult = connection.exec_driver_sql(query, (
			self.denormalize_name(table_name),
			self.denormalize_name(schema)
			))
		
		rows = cursorResult.all()
		if len(rows) == 0:
			# Tables must have at least one column otherwise they can't exist.
			raise exc.NoSuchTableError(f"{schema}.{table_name}" if schema else table_name)
		
		for row in rows:
			# Note: row._mapping is using column names as keys and not the aliases defined in the query.
			# 		row._mapping keys are lowercase if requires_name_normalize = True, or uppercase if False
			col_name = self.normalize_name(row._mapping['column_name']) # str """column name"""

# TODO: col_name needed normalizing. What other identifiers, PKs, FKs?
			assert row._mapping['type_name'] in ischema_names, "ischema_names is missing a key for datatype %s" % row._mapping['type_name']
			col_type = row._mapping['type_name'] # A String value, e.g. 'INTEGER'; TypeEngine[Any] """column type represented as a :class:`.TypeEngine` instance."""

			col_nullable = bool(row._mapping['nullable']) # bool """boolean flag if the column is NULL or NOT NULL"""
			col_default = row._mapping['column_def'] # Optional[str] """column default expression as a SQL string"""
			col_autoincrement = row._mapping['is_autoincrement'] == 'YES' # NotRequired[bool] """database-dependent autoincrement flag.
			# This flag indicates if the column has a database-side "autoincrement"
			# flag of some kind.   Within SQLAlchemy, other kinds of columns may
			# also act as an "autoincrement" column without necessarily having
			# such a flag on them.
			# See :paramref:`_schema.Column.autoincrement` for more background on "autoincrement".
			col_comment = row._mapping['remarks'] # NotRequired[Optional[str]] """comment for the column, if present. Only some dialects return this key """
			col_computed = None # NotRequired[ReflectedComputed] """indicates that this column is computed by the database. Only some dialects return this key.

			# TODO: The type for identity should be ReflectedIdentity, not a bool.
			col_identity = row._mapping['is_identity'] == 'YES' # NotRequired[ReflectedIdentity] indicates this column is an IDENTITY column. Only some dialects return this key.

			col_dialect_options = None # NotRequired[Dict[str, Any]] Additional dialect-specific options detected for this reflected object

			if col_type == 'NUMERIC':
				col_numeric_precision = row._mapping['numeric_precision']
				col_numeric_scale = row._mapping['numeric_scale']
				col_type = ischema_names.get(col_type)(
					int(col_numeric_precision),
					int(col_numeric_scale)
				)
			elif col_type == 'VARCHAR':
				col_character_maximum_length = row._mapping['character_maximum_length']
				col_type = ischema_names.get(col_type)(
					int(col_character_maximum_length)
				)
			else:
				col_type = ischema_names.get(col_type)()

			reflectedColumns.append({
				'name': col_name,
				'type': col_type,
				'nullable': col_nullable,
				'default': col_default,
				'autoincrement': col_autoincrement,
				'comment': col_comment,
				# 'computed': col_computed, # TODO: computed/generated column
				# 'identity': col_identity, # TODO: identity column
				# 'dialect_options': col_dialect_options
				})
		return reflectedColumns

	# The column tables in INFORMATION_SCHEMA do not have a 'computed' field.
	# Maybe these are referred to as 'generated' columns in HSQLDB?
	# INFORMATION_SCHEMA.COLUMNS has 'IS_GENERATED' and 'GENERATION_EXPRESSION' columns.
	# INFORMATION_SCHEMA.SYSTEM_COLUMNS has an 'IS_GENERATEDCOLUMN' column.
	# TODO: update get_columns to include computed and identity columns.

#i  def get_multi_columns(
	# TODO: for better performance implement get_multi_columns. DefaultDialect's implementation is only adequate for now.

	@reflection.cache
	def get_pk_constraint(self, connection, table_name, schema=None, **kw):
		self._ensure_has_table_connection(connection)
		if schema is None:
			schema = self.default_schema_name
		assert schema is not None
		cursorResult = connection.exec_driver_sql(
		"""SELECT column_name from information_schema.system_primarykeys
		WHERE table_schem = (?) AND table_name = (?)""",
		(self.denormalize_name(schema), self.denormalize_name(table_name)))
		all = cursorResult.scalars().all()
		if len(all) == 0 and self.has_table(connection, table_name, schema) == False:
			raise exc.NoSuchTableError(f"{schema}.{table_name}" if schema else table_name)

		constrained_columns = list(map(self.normalize_name, all))
		return {
			"name": None,
			"constrained_columns": constrained_columns
			#"dialect_options" : NotRequired[Dict[str, Any]] # Additional dialect-specific options detected for this primary key
			}
		# TODO:3: understand why test_get_pk_constraint fails when 'name' is set to pk_name.

#i  def get_multi_pk_constraint(
	# TODO: for better performance implement get_multi_pk_constraint. DefaultDialect's implementation is only adequate for now.

	@reflection.cache
	def get_foreign_keys(self, connection, table_name, schema=None, **kw):
		self._ensure_has_table_connection(connection)
		fktable_schem = schema or self.default_schema_name
		reflectedForeignKeys = []
		query = """
			SELECT
			fk_name,
			fkcolumn_name AS constrained_columns,
			pktable_schem AS referred_schema,
			pktable_name AS referrred_table,
			pkcolumn_name AS referred_columns,
			update_rule,
			delete_rule,
			deferrability
			FROM information_schema.system_crossreference
			WHERE fktable_schem = (?) AND fktable_name = (?)
			ORDER BY key_seq ASC"""
		cursorResult = connection.exec_driver_sql(query,
			(self.denormalize_name(fktable_schem), self.denormalize_name(table_name)))
		
		rows = cursorResult.all()
		if len(rows) == 0 and self.has_table(connection, table_name, schema) == False:
			raise exc.NoSuchTableError(f"{schema}.{table_name}" if schema else table_name)

		for row in rows:
			# Note row._mapping is using column names as keys and not the aliases defined in the query.
			fk_name = self.normalize_name(row._mapping['fk_name'])
			constrained_columns = self.normalize_name(row._mapping['fkcolumn_name'])

			if schema == None:
				referred_schema = None
			else:
				referred_schema = self.normalize_name(row._mapping['pktable_schem'])

			referred_table = self.normalize_name(row._mapping['pktable_name'])
			referred_columns = self.normalize_name(row._mapping['pkcolumn_name'])
			onupdate = row._mapping['update_rule']
			ondelete = row._mapping['delete_rule']
			deferrable = row._mapping['deferrability']
			# The values of UPDATE_RULE, DELETE_RULE, and DEFERRABILITY are all integers.
			# Somewhere as yet undiscovered, they'll probably map to FOREIGN KEY options,
			# such as [ON {DELETE | UPDATE} {CASCADE | SET DEFAULT | SET NULL}]
			# TODO: resolve FK options to strings if required for ReflectedForeignKeys.options

			# Retrieve an existing fk from the list or create a new one...
			# TODO: replace filter with call to _getDictFromList, if faster.
			filtered = tuple(filter(lambda d: 'name' in d and d['name'] == fk_name , reflectedForeignKeys))
			if(len(filtered) > 0):
				fk = filtered[0] # fk found
			else:
				# Create a new fk dictionary.
				# TODO: consider using the default dictionary instead, provided by ReflectionDefaults.foreign_keys, as used by PG and Oracle dialects.
				fk = {
					'name': fk_name, # ReflectedConstraint.name
					'constrained_columns': [],
					'referred_schema': referred_schema,
					'referred_table': referred_table,
					'referred_columns': [],
					'options': {
						'onupdate': onupdate,
						'ondelete': ondelete,
						'deferrable': deferrable # Supported?
						# TODO: Constraint deferrability is currently unsupported by HSQLDB. Exclude 'deferrable' from this line dictionary?
					}
				}
				reflectedForeignKeys.append(fk)
			fk['constrained_columns'].append(constrained_columns)
			fk['referred_columns'].append(referred_columns)
		return reflectedForeignKeys

#i  def get_multi_foreign_keys( # Return information about foreign_keys in all tables in the given ``schema``.
	# TODO: for better performance implement get_multi_foreign_keys. (currently only impl. for Oracle and PostgreSQL dialects)

	@reflection.cache
	def get_table_names(self, connection, schema=None, **kw):
		self._ensure_has_table_connection(connection)
		if schema is None:
			schema = self.default_schema_name
		cursorResult = connection.exec_driver_sql("""
			SELECT table_name FROM information_schema.tables
			WHERE table_schema = (?)
			AND table_type = 'BASE TABLE'
		""", (self.denormalize_name(schema),))
		return list(map(self.normalize_name, cursorResult.scalars().all()))

	@reflection.cache
	def get_temp_table_names(self, connection, schema=None, **kw):
		self._ensure_has_table_connection(connection)
		if schema is None:
			schema = self.default_schema_name
		cursorResult = connection.exec_driver_sql("""
			SELECT table_name FROM information_schema.system_tables
			WHERE table_type = 'GLOBAL TEMPORARY' AND table_schem = (?)
		""", (self.denormalize_name(schema),))
		return cursorResult.scalars().all()
	# HSQLDB supports two types of temporary table, global and local.
	# Are local temporary table names discoverable through INFORMATION_SCHEMA? It seems not.

	@reflection.cache
	def get_view_names(self, connection, schema=None, **kw):
		self._ensure_has_table_connection(connection)
		if schema is None:
			schema = self.default_schema_name
		cursorResult = connection.exec_driver_sql("""
			SELECT table_name FROM information_schema.tables
			WHERE table_schema = (?)
			AND table_type = 'VIEW'
		""",(self.denormalize_name(schema),))
		return list(map(self.normalize_name, cursorResult.scalars().all()))

	@reflection.cache
	def get_materialized_view_names(self, connection, schema=None, **kw):
		raise NotImplementedError()
	# According to Fred Toussi, "HSQLDB does not support materialized views 
	# directly. You can use database triggers to update tables acting as 
	# materialized views."

	@reflection.cache
	def get_sequence_names(self, connection, schema=None, **kw):
		self._ensure_has_table_connection(connection)
		if schema is None:
			schema = self.default_schema_name
		cursorResult = connection.exec_driver_sql("""
			SELECT sequence_name FROM information_schema.sequences
			WHERE sequence_schema = (?)
		""", (self.denormalize_name(schema),))
		return cursorResult.scalars().all()

	@reflection.cache
	def get_temp_view_names(self, connection, schema=None, **kw):
		raise NotImplementedError()
	# According to Claude, HSQLDB doesn't support temporary views.

	@reflection.cache
	def get_schema_names(self, connection, **kw):
		self._ensure_has_table_connection(connection)
		cursorResult = connection.exec_driver_sql("SELECT schema_name FROM information_schema.schemata")
		return list(map(self.normalize_name, cursorResult.scalars().all()))

	@reflection.cache
	def get_view_definition(self, connection, view_name, schema=None, **kw):
		self._ensure_has_table_connection(connection)
		if schema is None:
			schema = self.default_schema_name
		cursorResult = connection.exec_driver_sql("""
			SELECT view_definition FROM information_schema.views
			WHERE table_name = (?)
			AND table_schema = (?)
		""", (self.denormalize_name(view_name), self.denormalize_name(schema)))
		view_def = cursorResult.scalar()
		if view_def:
			return view_def
		else:
			raise exc.NoSuchTableError(f"{schema}.{view_name}" if schema else view_name)

	@reflection.cache
	def get_indexes(self, connection, table_name, schema=None, **kw):
		self._ensure_has_table_connection(connection)
		if schema is None:
			schema = self.default_schema_name
		reflectedIndexList = []
		query = """
			SELECT
			table_schem
			,table_name
			,index_name
			,column_name
			-- expressions
			,non_unique
			-- include_columns
			,asc_or_desc
			--, cst.constraint_name = index_name AS duplicates_constraint
			, cst.constraint_type
			FROM information_schema.system_indexinfo
			LEFT JOIN information_schema.table_constraints cst
			ON index_name = cst.constraint_name
			--AND table_name = cst.table_name
			AND table_schem = cst.table_schema
			WHERE table_schem = (?) AND table_name = (?)
		"""
		# TODO: removed commented out fields from above query.
		cursorResult = connection.exec_driver_sql(query, (self.denormalize_name(schema), self.denormalize_name(table_name)))

		rows = cursorResult.all()
		if len(rows) == 0 and self.has_table(connection, table_name, schema) == False:
			raise exc.NoSuchTableError(f"{schema}.{table_name}" if schema else table_name)
		
		for row in rows:
			index_name = self.normalize_name(row._mapping['index_name'])
			constraint_type = row._mapping['constraint_type'] # PRIMARY KEY | FOREIGN KEY | UNIQUE. If NULL, the index doesn't duplicate a constraint.

			# Primary keys and unique constraints are both unique, so we can simply use the non_unique field here...
			unique = not(row._mapping['non_unique'])

			idx = _getDictFromList('name', index_name, reflectedIndexList)
			if idx == None: # i.e. not already in reflectedIndexList...
				idx = {
					'name': index_name,
					'column_names': [],
					# 'expressions': [], # Not required. Unsuppored by HSQLDB?
					'unique': unique,
					# 'duplicates_constraint': # Not required
					# 'include_columns': None, # Deprecated
					'column_sorting': {}, # Not required
					# 'dialect_options': None # Not required.
				}
				reflectedIndexList.append(idx)

			column_name = self.normalize_name(row._mapping['column_name']) # list; if none, returned in expressions list
			idx['column_names'].append(column_name)

			# expressions = None
			# TODO: Is the expressions list applicable to HSQLDB?

			if constraint_type != None and False: # Temporarily disabled
				# A non-null constraint_type indicates the index and constraint names matched, so...
				idx['duplicates_constraint'] = constraint_name = index_name
			# Indexes that duplicate a constraint should possess the 'duplicates_constraint' key,
			# but Inspector._reflect_indexes excludes such indexes from the Table.indexes collection,
			# which causes ComponentReflectionTest.test_get_unique_constraints_hsqldb to fail.
			# For this reason assignment of the duplicates_constraint key above
   			# has been disabled until the correct solution is known.
			# See JSN_notes.md for more detail.
			# TODO: review 'duplicates_constraint' key and re-enable if appropriate.

			# idx['include_columns'] = # NotRequired[List[str]] # deprecated 2.0

			column_sorting = idx.get('column_sorting')
			assert column_sorting != None, 'column_sorting is None'
			# TODO: remove assertion when done

			asc_or_desc = row._mapping['asc_or_desc'] # Can be 'A', 'D', or null
			if(asc_or_desc == 'A'):
				column_sorting[column_name] = ('asc',)
			asc_or_desc = row._mapping['asc_or_desc']
			if(asc_or_desc == 'D'):
				column_sorting[column_name] = ('desc',)
			# The tuples for each item in the column_sorting dictionary may
			# contain 'asc', 'desc', 'nulls_first', 'nulls_last'.
			# HSQLDB doesn't appear to have a field for nulls first / last,
			# and only ascending ordering has been observed so far.
			assert asc_or_desc == 'A' or asc_or_desc == 'D'
			# TODO: remove the assertion and revise comments above.

			if False:
				# The SYSTEM_INDEXINFO table has a few more columns which
				# haven't been queried for. If these are useful, update the
				# query and they can be added as dialect_options...
				idx['dialect_options'] = {
					'type': row._mapping['TYPE'],
					'ordinal_position': row._mapping['ORDINAL_POSITION'],
					'cardinality': row._mapping['CARDINALITY'],
					'pages': row._mapping['PAGES'],
					'filter_condition': row._mapping['FILTER_CONDITION'],
					'row_cardinality': row._mapping['ROW_CARDINALITY'],
				}
				# TODO: remove this block of code if unused.

		return reflectedIndexList


	# TODO: for better performance implement get_multi_indexes.	

	@reflection.cache
	def get_unique_constraints(self, connection, table_name, schema=None, **kw):
		self._ensure_has_table_connection(connection)
		if schema is None:
			schema = self.default_schema_name
		reflectedUniqueConstraint = []
		query = """
			SELECT constraint_name, column_name FROM information_schema.table_constraints
			JOIN information_schema.system_indexinfo
			ON index_name = constraint_name
			WHERE constraint_type = 'UNIQUE'
			AND table_name = (?)
			AND constraint_schema = (?)
		"""
		cursorResult = connection.exec_driver_sql(query, (self.denormalize_name(table_name), self.denormalize_name(schema)))

		rows = cursorResult.all()
		if len(rows) == 0 and self.has_table(connection, table_name, schema) == False:
			raise exc.NoSuchTableError(f"{schema}.{table_name}" if schema else table_name)
		
		for row in rows:
			ct_name = index_name = self.normalize_name(row._mapping['constraint_name'])
			ct = _getDictFromList('name', ct_name, reflectedUniqueConstraint)
			if ct == None:
				ct = {
					'name': ct_name, # ReflectedConstraint.name
					'column_names': [],
					'duplicates_index': index_name,
					# 'dialect_options': {}
				}
				reflectedUniqueConstraint.append(ct)
			column_name = self.normalize_name(row._mapping['column_name'])
			ct['column_names'].append(column_name)
		return reflectedUniqueConstraint

#i  def get_multi_unique_constraints(
	# TODO: for better performance implement get_multi_unique_constraints.	

	@reflection.cache
	def get_check_constraints(self, connection, table_name, schema=None, **kw):
		self._ensure_has_table_connection(connection)
		if schema is None:
			schema = self.default_schema_name
		reflectedCheckConstraint = []
		query = """
			SELECT a.constraint_name, b.check_clause FROM information_schema.table_constraints a
			JOIN information_schema.check_constraints b
			ON a.constraint_name = b.constraint_name
			AND a.constraint_schema = b.constraint_schema
			AND a.constraint_catalog = b.constraint_catalog
			WHERE table_name = (?)
			AND table_schema = (?)
		"""
		cursorResult = connection.exec_driver_sql(query, (self.denormalize_name(table_name), self.denormalize_name(schema)))

		rows = cursorResult.all()
		if len(rows) == 0 and self.has_table(connection, table_name, schema) == False:
			raise exc.NoSuchTableError(f"{schema}.{table_name}" if schema else table_name)
		
		for row in rows:
			constraint_name = self.normalize_name(row._mapping['constraint_name'])
			check_clause = self.normalize_name(row._mapping['check_clause'])
			constraint = {
				'name': constraint_name,
				'sqltext': check_clause
			}
			reflectedCheckConstraint.append(constraint)
		return reflectedCheckConstraint

#i  def get_multi_check_constraints(
	# TODO: for better performance implement get_multi_check_constraints.	

	@reflection.cache
	def get_table_options(self, connection, table_name, schema=None, **kw):
		self._ensure_has_table_connection(connection)
		if schema is None:
			schema = self.default_schema_name
		tableOptions = {}
		query = """
			SELECT
			--table_name, 
			table_type, hsqldb_type, commit_action FROM information_schema.system_tables
			WHERE table_name = (?)
			AND table_schem = (?)
			--AND table_cat = 'PUBLIC'
			--AND table_type != 'VIEW'
		"""
		cursorResult = connection.exec_driver_sql(query, (self.denormalize_name(table_name), self.denormalize_name(schema)))
		row = cursorResult.first()
		if not row:
			raise exc.NoSuchTableError(f"{schema}.{table_name}" if schema else table_name)
		assert row is not None, 'Row is None.'

		# table_name = row._mapping['TABLE_NAME']
		table_type = row._mapping['table_type']			# GLOBAL TEMPORARY | more...
		hsqldb_type = row._mapping['hsqldb_type']		# MEMORY | CACHED | TEXT
		on_commit = row._mapping['commit_action']  	# DELETE | PRESERVE | NULL

		# The table type options in HSQLDB are: [MEMORY | CACHED | [GLOBAL] TEMPORARY | TEMP | TEXT ]

		# Table type information is stored in one of two columns depending on the type.
		# All* temporary types are stored as 'GLOBAL TEMPORARY' in the TABLE_TYPE column,
		# while MEMORY, CACHED, and TEXT types are recorded in the HSQLDB_TYPE column.
		# [* Possibly incorrect. Local temporary tables, a.k.a session tables, are not schema objects. See: (https://hsqldb.org/doc/2.0/guide/sessions-chapt.html)]

		_table_type_key_name = 'hsqldb_type'
		# The tableOptions key chosen originally was just 'type', but this
		# results in an error when the options are validated by the
		# DialectKWArgs._validate_dialect_kwargs method, which reports...
		# 	TypeError: Additional arguments should be named <dialectname>_<argument>, got 'type'
		# Changing the key to 'hsqldb_type' appears to fix the issue.

		# Combine type information from two columns into a single key value...
		if table_type.find('TEMP') >= 0:
			# GLOBAL TEMPORARY | TEMPORARY | TEMP
			tableOptions[_table_type_key_name] = table_type
			# TODO: confirm all temporary types are treated as global temporary, and there's no other way to identify the different types of temporary table.
		else:
			# MEMORY | CACHED | TEXT
			tableOptions['%s_%s' % (self.name, 'type')] = hsqldb_type
		
		# TODO: confirm using a single key is the correct approach.
		# TODO: Additional settings for TEXT tables are configured separately. Consider exposing them here.

		if on_commit != None:
			tableOptions['%s_%s' % (self.name, 'on_commit')] = on_commit # DELETE | PRESERVE | NULL

		return tableOptions
		# TODO: Document the TableOptions attributes defined in get_table_options

#i  def get_multi_table_options( # Return a dictionary of options specified when the tables in the given schema were created.
	# TODO: for better performance implement get_multi_table_options.	

	@reflection.cache
	def get_table_comment(self, connection, table_name, schema=None, **kw):
		self._ensure_has_table_connection(connection)
		if schema is None:
			schema = self.default_schema_name
		query = """
			SELECT remarks FROM information_schema.system_tables
			WHERE table_name = (?)
			AND table_schem = (?)
		"""
		cursorResult = connection.exec_driver_sql(query, (self.denormalize_name(table_name), self.denormalize_name(schema)))
		row = cursorResult.first()
		if not row:
			raise exc.NoSuchTableError(f"{schema}.{table_name}" if schema else table_name)
		return {"text": row[0]}

#i  def get_multi_table_comment(
	# TODO: for better performance implement get_multi_table_comment.	

	@reflection.cache
	def has_table(self, connection, table_name, schema=None, **kw):
		self._ensure_has_table_connection(connection)
		if schema is None:
			schema = self.default_schema_name
		assert schema is not None
		cursorResult = connection.exec_driver_sql(
			"""SELECT * FROM information_schema.tables
			WHERE table_schema = (?)
			AND table_name = (?)
			""", (self.denormalize_name(schema), self.denormalize_name(table_name)))
		return cursorResult.first() is not None
	# Tables are identified by catalog, schema, and table name in HSQLDB.
	# It's possible two tables could share matching schema and table names,
	# but in a different catalog, which might break the function above.

	@reflection.cache
	def has_index(self, connection, table_name, index_name, schema=None, **kw):
		self._ensure_has_table_connection(connection)
		if schema is None:
			schema = self.default_schema_name
		query = """
			SELECT COUNT(*) FROM information_schema.system_indexinfo
			WHERE index_name = (?)
			AND table_name = (?)
			AND table_schem = (?)
			LIMIT 1
		"""
		cursorResult = connection.exec_driver_sql(query, (
			self.denormalize_name(index_name),
			self.denormalize_name(table_name),
			self.denormalize_name(schema)
			))
		return cursorResult.scalar() > 0
		# TODO: raise exc.NoSuchTableError when required

	@reflection.cache
	def has_sequence(self, connection, sequence_name, schema=None, **kw):
		self._ensure_has_table_connection(connection)
		if schema is None:
			schema = self.default_schema_name
		query = """
			SELECT COUNT(*) FROM information_schema.sequences
			WHERE sequence_name = '{sequence_name}'
			AND sequence_schema = '{schema}'
			LIMIT 1
		"""
		cursorResult = connection.exec_driver_sql(query, (
			self.denormalize_name(sequence_name),
			self.denormalize_name(schema)
			))
		return cursorResult.scalar() > 0
		# TODO: raise exc.NoSuchTableError when required

	@reflection.cache
	def has_schema(self, connection, schema_name, **kw):
		self._ensure_has_table_connection(connection)
		query = """
			SELECT COUNT(*) FROM information_schema.schemata
			WHERE schema_name = (?)
			--AND catalog_name = 'PUBLIC'
		"""
		cursorResult = connection.exec_driver_sql(query, (self.denormalize_name(schema_name),))
		return cursorResult.scalar() > 0
		# TODO: cater for multiple catalogs

	def _get_server_version_info(self, connection):
		return connection.exec_driver_sql("CALL DATABASE_VERSION()").scalar()

	def _get_default_schema_name(self, connection):
		return connection.exec_driver_sql("VALUES(CURRENT_SCHEMA)").scalar()

	def do_ping(self, dbapi_connection):
		# Temporarily overriding to discover when DefaultDialect.do_ping gets called.
		raise NotImplementedError()
	# TODO: verify DefaultDialect.do_ping works with HSQLDB.

#i  def do_rollback_to_savepoint(
	# TODO: HSQLDB's ROLLBACK [WORK] TO SAVEPOINT has an optional keyword. What is it and does it need implementing?

	def do_begin_twophase(self, connection, xid):
		"""Begin a two phase transaction on the given connection.
		:param connection: a :class:`_engine.Connection`.
		:param xid: xid
		"""
		self.do_begin(connection.connection)

	def do_prepare_twophase(self, connection, xid):
		"""Prepare a two phase transaction on the given connection.
		:param connection: a :class:`_engine.Connection`.
		:param xid: xid
		"""
		pass

	def do_rollback_twophase(self, connection, xid, is_prepared=True, recover=False):
		"""Rollback a two phase transaction on the given connection.
		:param connection: a :class:`_engine.Connection`.
		:param xid: xid
		:param is_prepared: whether or not :meth:`.TwoPhaseTransaction.prepare` was called.
		:param recover: if the recover flag was passed.
		"""
		self.do_rollback(connection.connection)

	def do_commit_twophase(self, connection, xid, is_prepared=True, recover=False): 
		"""Commit a two phase transaction on the given connection.
		:param connection: a :class:`_engine.Connection`.
		:param xid: xid
		:param is_prepared: whether or not
		:meth:`.TwoPhaseTransaction.prepare` was called.
		:param recover: if the recover flag was passed.
		"""
		if not is_prepared:
			self.do_prepare_twophase(connection, xid)
		self.do_commit(connection.connection)

	def do_recover_twophase(self, connection):
		"""Recover list of uncommitted prepared two phase transaction identifiers on the given connection.
		:param connection: a :class:`_engine.Connection`.
		"""
		raise NotImplementedError("Recover two phase query for HyperSqlDialect not implemented.")

# TODO: fully implement and test the five methods above for two-phase transactions. For more info see JSN_notes.md and scratch_twophase.py

	def is_disconnect(self, e, connection, cursor):
		"""Return True if the given DB-API error indicates an invalid connection"""
		if isinstance(e, (
			# self.dbapi.InterfaceError,	# my, pg
			self.dbapi.DatabaseError,
			# self.dbapi.DataError,
			# self.dbapi.OperationalError,	# my
			# self.dbapi.IntegrityError,
			# self.dbapi.InternalError,
			# self.dbapi.ProgrammingError,	# my
			# self.dbapi.NotSupportedError,
			)):
			# TODO: remove any commented out errors above that don't apply.
			return True

		# Log unhandled exceptions...
		if isinstance(e, (self.dbapi.Error, self.dbapi.Warning)): # TODO: remove 'True or'
			print('### repr e:', repr(e))
			print('### repr self.dbapi.Error:', repr(self.dbapi.Error))
			print('### repr self.dbapi.Warning:', repr(self.dbapi.Warning))
			print('### str e:', str(e))
			breakpoint() #-
			raise NotImplementedError("Unhandled exception. Update the method 'HyperSqlDialect.is_disconnect'")
		# TODO: Remove the above test

		return False
	# Unsure which errors are regarded as an 'invalid connection',
	# or what may trigger them, apart from statement 'DISCONNECT'.
	# TODO: remove exploratory code from the is_disconnect function.

	def on_connect_url(self, url):
		from sqlalchemy.engine.url import URL
		isolation_level = url.query.get('isolation_level', None)
		def do_on_connect(conn):
			if isolation_level:
				self.set_isolation_level(conn, isolation_level)
		return do_on_connect

	def on_connect(self):
		def do_on_connect(connection):
			# connection.execute("SET SPECIAL FLAGS etc")
			pass
		return do_on_connect
	# This is used to set dialect-wide per-connection options such as isolation modes, Unicode modes, etc.
	# No event listener is generated if on_connect returns None instead of a callable.
	# TODO: remove on_connect function if unused

	def set_isolation_level(self, dbapi_connection, level):
		if level == "AUTOCOMMIT":
			dbapi_connection.jconn.setAutoCommit(True)
		else:
			dbapi_connection.jconn.setAutoCommit(False)
			# Use a tuple to look up index values for isolation levels...
			index = ('NONE', 'READ UNCOMMITTED', 'READ COMMITTED', 'REPEATABLE READ', 'SERIALIZABLE').index(level) # order critical
			dbapi_connection.jconn.setTransactionIsolation(index)
	# The ordering of isolation levels must match the constants defined in org.hsqldb.jdbc.JDBCConnection
	# The JayDeBeApi Connection object currently lacks an autocommit attribute or setautocommit() method.

	def get_isolation_level(self, dbapi_connection):
		"""Given a DBAPI connection, return its isolation level."""
		with dbapi_connection.cursor() as cursor:
			cursor.execute("CALL SESSION_ISOLATION_LEVEL()") # Returns READ COMMITTED or SERIALIZABLE
			row = cursor.fetchone()
		return row[0].upper()

	def get_default_isolation_level(self, dbapi_connection):
		try:
			with dbapi_connection.cursor() as cursor:
				cursor.execute('CALL DATABASE_ISOLATION_LEVEL()') # Returns READ COMMITTED or SERIALIZABLE
				row = cursor.fetchone()
			return row[0].upper()
		except:
			return 'READ COMMITTED' # HSQLDB's default isolation level
		# DATABASE_ISOLATION_LEVEL() returns the isolation level for all new sessions.
		# SESSION_ISOLATION_LEVEL() returns the level for the current session.
		# Both functions will return the same value on first connection, the point at which get_default_isolation_level is called,
		# so I presume we could use either.
		# However calling get_default_isolation_level again (unsure if this ever happens) after an isolation level has changed
		# will return different values depending on which built-in function was used. We probably want DATABASE_ISOLATION_LEVEL().
		#
		# Should we also be returning AUTOCOMMIT?  I don't currently think so. 

	# Isolation level functions
	# HSQLDB supported isolation levels are documented here - https://hsqldb.org/doc/2.0/guide/sessions-chapt.html
	# 	i.e. READ UNCOMMITTED, READ COMMITTED, REPEATABLE READ and SERIALIZABLE
	# Documentation for members of the Dialect interface can be found here - \sqlalchemy\engine\interfaces.py
	# TODO: Reorder the position of member to match interface.py

	def get_isolation_level_values(self, dbapi_conn):
		return (
			"AUTOCOMMIT",		# HSQLDB supports autocommit.
			"READ UNCOMMITTED", # HSQLDB treats a READ COMMITTED + read only
			"READ COMMITTED",
			"REPEATABLE READ",	# HSQLDB upgrades REPEATABLE READ to SERIALIZABLE
			"SERIALIZABLE"
		)
	# SQLAlchemy treats AUTOCOMMIT like an isolation level.
	# HSQLDB supports AUTOCOMMIT, but how autocommit and isolation levels are set differs.
	# e.g.
	#		SET AUTOCOMMIT FALSE
	#		SET TRANSACTION ISOLATION LEVEL SERIALIZABLE
	#
	# Some logic is surely required to set autocommit or isolation level, but where?
	#
	# Isolation levels and autocommit are separate in HSQLDB, as in MySQL.
	# get_isolation_level_values function for MySQL doesn't include AUTOCOMMIT, although MySQL's base.py describes it as a valid value.
	# MySQL's base.py also says... "For the special AUTOCOMMIT isolation level, DBAPI-specific techniques are used".
	#
	# SQLAlchemy documentation examples show autocommit being set, such as...
	#	with engine.connect() as connection:
	#		connection.execution_options(isolation_level="AUTOCOMMIT")
	#
	# So, where do execution pathS for AUTOCOMMIT and ISOLATION LEVELs diverge?
	# TODO: check the definitions for execution_options function on engine and connection classes.

	supports_schemas = True # Setting 'supports_schemas' to false disables schema level tests.
	# TODO: remove line above, i.e. inherit from DefaultDialect.supports_schemas

	supports_is_distinct_from = True
	# Supported since HSQLDB v2.0

	poolclass = pool.QueuePool
	# QueuePool is the default.
	# Claude says NullPool or StaticPool is suitable for HSQLDB, but Claude's information might be outdated.
	# The Access dialect is using NullPool.
	# poolclass is normally specified as a parameter to create_engine function, e.g.
	#   create_engine("postgresql+psycopg2://scott:tiger@localhost/test", poolclass=NullPool)
	# pool_size for QueuePool can is also specified as a create_engine parameter, e.g.
	#   create_engine("postgresql+psycopg2://me@localhost/mydb", pool_size=20, max_overflow=0)
	# Detailed info on pooling can be found here:   \sqlalchemy\doc\build\core\pooling.rst
	#
	# How is the poolclass assigned to above referenced?
	#   poolclass is returned by the get_pool_class method of the DefaultDialect.
	# TODO: Verify if the above is correct.
	# TODO: find out where the above property is from - it's not part of the Dialect interface.
	#
	# TODO: See if QueuePool works, or use StaticPool instead.

	default_paramstyle = "qmark"

