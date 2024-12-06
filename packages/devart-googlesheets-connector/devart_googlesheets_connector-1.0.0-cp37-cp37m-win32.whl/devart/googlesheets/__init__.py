"""
Python Connector for Google Sheets is a connectivity solution for accessing
Google Sheets Customer Engagement (formerly Dynamics CRM) from Python
applications to read and update data. It fully implements the Python DB API
2.0 specification. The connector is distributed as a wheel package for Windows
and Windows Server.
 
Standard SQL syntax

    The connector fully supports the ANSI SQL standard and lets you execute SQL
    statements against your Google Sheets data just like you would normally work
    with relational databases. Simple queries are directly converted to Google
    Sheets API calls and executed on the Google Sheets side.
    Complex queries are transformed into simpler queries, which are then converted
    to Google Sheets API calls. The embedded SQL engine then processes the results
    in the local cache and applies advanced SQL features from the original complex
    query.

Version: 1.0.0 

Homepage: https://www.devart.com/python/googlesheets/
"""
from .googlesheets import *
