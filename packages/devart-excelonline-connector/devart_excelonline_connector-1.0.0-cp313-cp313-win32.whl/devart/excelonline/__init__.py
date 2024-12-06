"""
Python Connector for Microsoft Excel Online is a connectivity solution
for accessing Microsoft Excel Online from Python applications to read and
update data. It fully implements the Python DB API 2.0 specification.
The connector is distributed as a wheel package for Windows and Windows
Server.
 
Standard SQL syntax

    The connector fully supports the ANSI SQL standard and lets you execute SQL
    statements against your Microsoft Excel Online data just like you would
    normally work with relational databases. Simple queries are directly converted
    to Microsoft Excel Online API calls and executed on the Microsoft Excel Online
    side.
    Complex queries are transformed into simpler queries, which are then converted
    to Microsoft Excel Online API calls. The embedded SQL engine then processes
    the results in the local cache and applies advanced SQL features from
    the original complex query.

Version: 1.0.0 

Homepage: https://www.devart.com/python/excelonline/
"""
from .excelonline import *
