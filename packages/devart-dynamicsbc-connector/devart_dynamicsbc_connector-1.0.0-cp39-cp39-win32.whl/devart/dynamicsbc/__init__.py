"""
Python Connector for Dynamics 365 Business Central is a connectivity solution
for accessing Dynamics 365 Business Central from Python applications to read
and update data. It fully implements the Python DB API 2.0 specification.
The connector is distributed as a wheel package for Windows and Windows
Server.
 
Standard SQL syntax

    The connector fully supports the ANSI SQL standard and lets you execute SQL
    statements against your Dynamics 365 Business Central data just like you would
    normally work with relational databases. Simple queries are directly converted
    to Dynamics 365 BC API calls and executed on the Dynamics 365 BC side.
    Complex queries are transformed into simpler queries, which are then converted
    to Dynamics 365 BC API calls. The embedded SQL engine then processes
    the results in the local cache and applies advanced SQL features from
    the original complex query.

Version: 1.0.0 

Homepage: https://www.devart.com/python/dynamicsbc/
"""
from .dynamicsbc import *
