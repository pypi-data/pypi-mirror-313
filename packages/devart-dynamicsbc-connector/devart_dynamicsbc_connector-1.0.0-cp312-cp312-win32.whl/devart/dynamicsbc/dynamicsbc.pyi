from typing import Tuple, List, Optional, Any, Dict
import datetime
import array

class description(object):
    """
    The description class describes a column in a rowset returned by the cursor.
    """
    name: str
    """
    The name of the column in the rowset.
    """
    type_code: int
    """
    The database type code that corresponds to the type of the column.
    """
    display_size: int
    """
    The actual length of the column in characters for a character column, `None` otherwise.
    """
    internal_size: int
    """
    The size in bytes used by the connector to store the column data.
    """
    precision: int
    """
    The total number of significant digits for a numeric column, `None` otherwise.
    """
    scale: int
    """
    The number of digits in the fractional part for a numeric column, `None` otherwise.
    """
    null_ok: bool
    """
    `Py_True` if the corresponding database column accepts `NULL` values, `Py_False` otherwise.
    """
    ...

class cursor(object):
    """
    The `cursor` class represents a database cursor, which is used to manage
    the context of fetch operations. This class provides methods for executing SQL
    statements and operating rowsets. Cursors are created using the `cursor()`
    connection method.
    """
    connection: str
    """
    A read-only attribute that specifies the `connection` object
    to which the cursor belongs.
    """
    arraysize: int
    """
    A read/write attribute that specifies the number of rows to fetch at a time
    with the `fetchmany()` method.
    """
    description: Tuple[description]
    """
    A read-only attribute that describes the columns in a rowset returned
    by the cursor.
    """
    rowcount: int
    """
    A read-only attribute that specifies the number of rows that the last
    `execute()` call produced by a `SELECT` statement or affected by `UPDATE` or
    `INSERT` statements.
    """
    rownumber: int
    """
    A read-only attribute that specifies the current 0-based index of the cursor
    in the result set.
    """
    lastrowid: None
    """
    This read-only attribute is provided for compatibility with the DB API 2.0
    specification. It currently returns `None`.
    """
    def setinputsizes(self, sizes: Optional[List[Any] | Tuple[Any]]) -> None:
        """
        Predefines the types of parameters for the further call to the `execute*()`
        method.
        """
        ...
    def execute(self, operation: str, parameters: Optional[List[Any] | Tuple[Any] | Dict[str, Any]]) -> cursor:
        """
        Prepares and executes a database operation.
        """
        ...
    def executemany(self, operation: str, parameters: Optional[List[Any] | Tuple[Any] | Dict[str, Any]]) -> cursor:
        """
        Prepares and executes a batch database operation.
        """
    def fetchone(self) -> Tuple[Any]:
        """
        Fetches the next row of a query result set.
        """
        ...
    def fetchmany(self, size: Optional[int]) -> List[Tuple[Any]]:
        """
        Fetches the next set of rows of a query result.
        """
        ...
    def fetchall(self) -> List[Tuple[Any]]:
        """
        Fetches all remaning rows of a query result.
        """
        ...
    def next(self) -> Tuple[Any]:
        """
        Returns the next row from the currently executed SQL statement.
        """
        ...
    def scroll(value: int, mode: Optional[str]) -> bool:
        """
        Scrolls the cursor in the result set to a new position.
        """
        ...
    def addtypecast(self, column: int | dbtype | str | description | Dict[str, type], python_type: Optional[type]) -> None:
        """
        Defines a data type cast rule to use when fetching data from the cursor.
        """
        ...
    def cleartypecast(self) -> None:
        """
        Removes all data type cast rules defined for the cursor.
        """
        ...
    def close(self) -> None:
        """
        Closes the cursor.
        """
        ...
    def setoutputsize(size: int, column: Optional[int]):
        """
        This method is provided for compatibility with the DB API 2.0 specification.
        It currently does nothing but is safe to call.
        """
        ...

class connection(object):
    """
    The `connection` class encapsulates a database session. It provides methods
    for creating cursors, type casting, and transaction handling. Connections
    are created using the `connect()` module method.
    """
    connectstring: str
    """
    A read-only attribute that returns a string literal of the form
    `"parameter=value;parameter=value"` that contains the parameters
    for the current connection.
    """
    def cursor(self) -> cursor:
        """
        Creates a new cursor object, which is used to manage the context of fetch
        operations.
        """
        ...
    def close(self) -> None:
        """
        Closes the connection.
        """
        ...
    def commit(self) -> None:
        """
        Commits any pending transaction to the database.
        """
        ...
    def rollback(self) -> None:
        """
        Causes the database to roll back any pending transaction.
        """
        ...
    def addtypecast(self, column: int | dbtype | str | description | Dict[str, type], python_type: Optional[type]) -> None:
        """
        Defines a data type cast rule to use when fetching data from the cursor.
        """
        ...
    def cleartypecast(self) -> None:
        """
        Removes all data type cast rules defined for the connection.
        """
        ...

class connection_pool(object):
    """
    Description of the `connection_pool` class is not available yet.
    """
    enabled: bool = False
    """
    Description of the `enabled` attribute is not available yet.
    """
    max_size: int = 1000
    """
    Description of the `max_size` attribute is not available yet.
    """
    min_size: int = 1000
    """
    Description of the `min_size` attribute is not available yet.
    """
    lifetime: int = 0
    """
    Description of the `lifetime` attribute is not available yet.
    """
    validate: bool = False
    """
    Description of the `validate` attribute is not available yet.
    """

class Warning(Exception):
    """
    This exception is raised for important warnings like data truncations while
    inserting, etc. The `Warning` exception is a subclass of the Python
    `Exception` class.
    """
    ...

class Error(Exception): 
    """
    This exception is the base class of all error exceptions. You can use
    it to catch all errors with a single `except` statement. The `Error` exception
    is a subclass of the Python `Exception` class.
    """
    ...

class InterfaceError(Error): 
    """
    This exception is raised for errors that are related to the database interface
    rather than the database itself. The `InterfaceError` exception is a subclass
    of `Error`.
    """
    ...

class DatabaseError(Error): 
    """
    This exception is raised for errors that are related to the database.
    The `DatabaseError` exception is a subclass of `Error`.
    """
    ...

class DataError(DatabaseError): 
    """
    This exception is raised for errors caused by issues with the processed data
    like division by zero, numeric value out of range, etc. The `DataError`
    exception is a subclass of `DatabaseError`.
    """
    ...

class OperationalError(DatabaseError): 
    """
    This exception is raised for errors that are related to the database operation
    and not necessarily under the control of the developer, for example,
    an unexpected disconnect occurs, the data source name isn't found,
    a transaction couldn't be processed, a memory allocation error occurred
    during processing, etc. The OperationalError exception is a subclass
    of `DatabaseError`.
    """
    ...

class IntegrityError(DatabaseError): 
    """
    This exception raised when the relational integrity of the database
    is affected, for example, a foreign key check fails. The `IntegrityError`
    exception is a subclass of `DatabaseError`.
    """
    ...

class InternalError(DatabaseError): 
    """
    This exception is raised when the database encounters an internal error,
    for example, the cursor isn't valid anymore, the transaction is out of sync,
    etc. The `InternalError` exception is a subclass of `DatabaseError`.
    """
    ...

class ProgrammingError(DatabaseError): 
    """
    This exception is raised for programming errors, for example, table not found
    or already exists, syntax error in the SQL statement, wrong number
    of parameters specified, etc. The `ProgrammingError` exception is a subclass
    of `DatabaseError`.
    """
    ...

class NotSupportedError(DatabaseError): 
    """
    This exception is raised when a method or database API isn't supported
    by the database, for example, requesting a `rollback()` on a connection
    that doesn't support transactions or has transactions turned off.
    The `NotSupportedError` exception is a subclass of `DatabaseError`.
    """
    ...

class binary(object):
    """
    This type object describes an object that holds binary data. By default, this
    type object is used to fetch BLOB-based columns from the cursor. You can also
    create a `binary` object using the `Binary()` constructor.
    """
    value: bytes
    """
    A value of type `bytes` that represents binary data. This is a read/write attribute
    that accepts values of type `str`, `bytes`, `bytearray`, `array.array`, and `binary`.
    """

class dbtype(object):
    name: str
    values: Dict[int, str]

apilevel: str = "2.0"
"""
Indicates the DB API level supported by the module. Returns a string value "2.0".
"""

threadsafety: int = 2
"""
Indicates the thread safety level of the module. Returns an integer value `2` that means
that threads may share the module and connections.
"""

paramstyle: str = "named"
"""
Indicates the type of parameter marker formatting expected by the module. 
Returns a string value "named" that means that the module supports named style parameters,
for example, `...WHERE name=:name`.
"""

def connect(connection_string: str, **kwargs: Optional[Any]) -> connection: 
    """
    Creates a new connection to the database.
    """
    ...

def Date(year: int, month: int, day: int) -> datetime.date: 
    """
    Creates an object that holds a date value.
    """
    ...

def Time(hour: int, minute: int, second: int | float, timezone: Optional[datetime.tzinfo]) -> datetime.time:
    """
    Creates an object that holds a time value.
    """
    ...

def Timestamp(year: int, month: int, day: int, hour: Optional[int], minute:Optional[int], second: Optional[int | float], timezone: Optional[datetime.tzinfo]) -> datetime.datetime:
    """
    Creates an object that holds a timestamp value.
    """
    ...

def DateFromTicks(ticks: float) -> datetime.date:
    """
    Creates an object that holds a date value from the given ticks value
    (the number of seconds since the Unix epoch). For more information, see
    the `time` module in the standard Python documentation.
    """
    ...

def TimeFromTicks(ticks: float) -> datetime.time:
    """
    Creates an object that holds a time value from the given ticks value (number
    of seconds since the Unix epoch). For more information, see the `time` module
    in the standard Python documentation.
    """
    ...

def TimestampFromTicks(ticks: float) -> datetime.datetime:
    """
    Creates an object that holds a timestamp value from the given ticks value
    (number of seconds since the Unix epoch). For more information, see the `time`
    module in the standard Python documentation.
    """
    ...

def Binary(value: str | bytes | bytearray | array.array) -> binary:
    """
    Creates an object that holds binary data.
    """
    ...

STRING: dbtype
"""
This type object describes string-based columns in a database.
"""

BINARY: dbtype
"""
This type object describes binary columns in a database.
"""

NUMBER: dbtype
"""
This type object describes numeric columns in a database.
"""

DATETIME: dbtype
"""
This type object describes date/time columns in a database.
"""

ROWID: dbtype
"""
This type object describes the `row id` columns in a database.
"""
