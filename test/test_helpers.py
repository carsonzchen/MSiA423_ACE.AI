from src.helpers import helpers


def test_formatsql_sqlvar():
    test_sql = "SELECT artist FROM ${var:database} WHERE artist LIKE %Britney%"
    test_sqlvars = dict(database="Tracks")

    answer = "SELECT artist FROM Tracks WHERE artist LIKE %%Britney%%"

    assert helpers.format_sql(test_sql, replace_sqlvar=test_sqlvars) == answer


def test_formatsql_var():
    test_sql = "SELECT artist FROM {database} WHERE artist LIKE %Britney%"
    test_vars = dict(database="Tracks")

    answer = "SELECT artist FROM Tracks WHERE artist LIKE %%Britney%%"

    assert helpers.format_sql(test_sql, replace_var=test_vars) == answer


def test_formatsql_nopython():
    test_sql = "SELECT artist FROM {database} WHERE artist LIKE %Britney%"
    test_vars = dict(database="Tracks")

    answer = "SELECT artist FROM Tracks WHERE artist LIKE %Britney%"

    assert helpers.format_sql(test_sql, replace_var=test_vars, python=False) == answer

