"""
libgentools: A Python library for downloading content from Library Genesis.

    Copyright (C) 2024  David Gaal (gaaldavid@tuta.io)

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.


Classes and exceptions exported by the module:

Classes
    SearchRequest(query): Handles search requests.
    Results(results): Manages search results.

Exceptions
    QueryError: Raised when query is too short.
    FilterError: Raised when an invalid filter is encountered.

Check the documentation for details: https://libgentools.readthedocs.io
"""

from .libgentools import *
