from __future__ import with_statement, unicode_literals, division, print_function

WITH_STATEMENT = with_statement.compiler_flag
UNICODE_LITERALS = unicode_literals.compiler_flag
DIVISION = division.compiler_flag
PRINT_FUNCTION = print_function.compiler_flag

COMPLETE_FUTURE = WITH_STATEMENT | UNICODE_LITERALS | DIVISION | PRINT_FUNCTION